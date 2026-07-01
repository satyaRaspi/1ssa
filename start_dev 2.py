#!/usr/bin/env python3
"""Start the Shakti Scheme prototype backend and frontend.

This helper creates the Python virtual environment, installs backend dependencies,
installs frontend dependencies when needed, and starts both servers.

v1.0.2 adds safer npm handling so startup does not hang silently when registry,
proxy, or lock-file issues occur.
"""
import argparse
import json
import os
import platform
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
BACKEND = ROOT / "backend"
FRONTEND = ROOT / "frontend"
VENV = BACKEND / ".venv"
VERSION_FILE = ROOT / "VERSION.json"


def read_version():
    fallback = {"version": "1.0.2", "build": "20260701.2", "database": "SQLite"}
    try:
        return {**fallback, **json.loads(VERSION_FILE.read_text(encoding="utf-8"))}
    except Exception:
        return fallback


APP_META = read_version()
APP_VERSION = APP_META["version"]
BUILD_NUMBER = APP_META["build"]


def npm_cmd():
    return "npm.cmd" if platform.system().lower().startswith("win") else "npm"


def python_bin():
    if platform.system().lower().startswith("win"):
        return VENV / "Scripts" / "python.exe"
    return VENV / "bin" / "python"


def run(cmd, cwd=None, timeout=None, env=None, friendly_name=None):
    label = friendly_name or " ".join(map(str, cmd))
    print(f"> {' '.join(map(str, cmd))}", flush=True)
    try:
        subprocess.run(
            cmd,
            cwd=str(cwd) if cwd else None,
            env=env,
            check=True,
            timeout=timeout,
        )
    except subprocess.TimeoutExpired as exc:
        raise RuntimeError(
            f"{label} took too long and was stopped. This is usually an npm registry, proxy, DNS, or network issue."
        ) from exc
    except subprocess.CalledProcessError as exc:
        raise RuntimeError(f"{label} failed with exit code {exc.returncode}.") from exc


def ensure_node_available():
    if not shutil.which(npm_cmd()):
        raise RuntimeError("npm was not found. Please install Node.js LTS, then run this script again.")
    run([npm_cmd(), "--version"], cwd=FRONTEND, timeout=20, friendly_name="npm version check")


def ensure_backend(skip_install=False):
    if not VENV.exists():
        run([sys.executable, "-m", "venv", str(VENV)], cwd=BACKEND, timeout=120, friendly_name="Python virtual environment creation")

    py = python_bin()
    if not skip_install:
        run([str(py), "-m", "pip", "install", "--upgrade", "pip"], cwd=BACKEND, timeout=180, friendly_name="pip upgrade")
        run([str(py), "-m", "pip", "install", "-r", "requirements.txt"], cwd=BACKEND, timeout=240, friendly_name="backend dependency install")
    return py


def frontend_ready():
    vite_bin = FRONTEND / "node_modules" / ".bin" / ("vite.cmd" if platform.system().lower().startswith("win") else "vite")
    return (FRONTEND / "node_modules").exists() and vite_bin.exists()


def ensure_frontend(skip_install=False, npm_timeout=180):
    ensure_node_available()
    if skip_install:
        print("Skipping frontend dependency install because --skip-install was supplied.", flush=True)
        return
    if frontend_ready():
        print("Frontend dependencies already installed. Skipping npm install.", flush=True)
        return

    # package-lock.json is intentionally not shipped in v1.0.2 because older builds
    # accidentally carried non-public registry URLs. npm will generate a local lock.
    lock_file = FRONTEND / "package-lock.json"
    if lock_file.exists():
        print("Removing existing package-lock.json to avoid stale/private registry URLs.", flush=True)
        lock_file.unlink()

    env = {
        **os.environ,
        "NPM_CONFIG_REGISTRY": "https://registry.npmjs.org/",
        "NPM_CONFIG_AUDIT": "false",
        "NPM_CONFIG_FUND": "false",
        "NPM_CONFIG_PROGRESS": "false",
        "NPM_CONFIG_UPDATE_NOTIFIER": "false",
    }
    run(
        [npm_cmd(), "install", "--no-audit", "--no-fund", "--loglevel=warn"],
        cwd=FRONTEND,
        env=env,
        timeout=npm_timeout,
        friendly_name="frontend npm install",
    )


def main():
    parser = argparse.ArgumentParser(description="Start the Shakti Scheme Application prototype.")
    parser.add_argument("--skip-install", action="store_true", help="Do not run pip install or npm install; start using existing dependencies.")
    parser.add_argument("--backend-only", action="store_true", help="Start only the backend API.")
    parser.add_argument("--frontend-only", action="store_true", help="Start only the frontend UI.")
    parser.add_argument("--npm-timeout", type=int, default=180, help="Seconds to wait for npm install before stopping it. Default: 180.")
    args = parser.parse_args()

    try:
        if args.frontend_only:
            ensure_frontend(skip_install=args.skip_install, npm_timeout=args.npm_timeout)
            print(f"\nStarting frontend v{APP_VERSION} on http://localhost:5173\n", flush=True)
            subprocess.run([npm_cmd(), "run", "dev"], cwd=str(FRONTEND), check=True, env={**os.environ, "VITE_API_BASE": "http://localhost:8000"})
            return

        py = ensure_backend(skip_install=args.skip_install)
        if args.backend_only:
            print(f"\nStarting backend v{APP_VERSION} on http://localhost:8000\n", flush=True)
            subprocess.run([str(py), "-m", "uvicorn", "main:app", "--reload", "--port", "8000"], cwd=str(BACKEND), check=True)
            return

        ensure_frontend(skip_install=args.skip_install, npm_timeout=args.npm_timeout)
        # Avoid recursive wait loop by using a small supervision loop here.
        backend_cmd = [str(py), "-m", "uvicorn", "main:app", "--reload", "--port", "8000"]
        frontend_cmd = [npm_cmd(), "run", "dev"]
        print(f"\nShakti Scheme Application v{APP_VERSION} · Build {BUILD_NUMBER}", flush=True)
        print("Starting backend on http://localhost:8000", flush=True)
        print("Starting frontend on http://localhost:5173\n", flush=True)
        backend = subprocess.Popen(backend_cmd, cwd=str(BACKEND))
        frontend = subprocess.Popen(frontend_cmd, cwd=str(FRONTEND), env={**os.environ, "VITE_API_BASE": "http://localhost:8000"})
        try:
            while True:
                backend_code = backend.poll()
                frontend_code = frontend.poll()
                if backend_code is not None:
                    frontend.terminate()
                    raise RuntimeError(f"Backend stopped with exit code {backend_code}.")
                if frontend_code is not None:
                    backend.terminate()
                    raise RuntimeError(f"Frontend stopped with exit code {frontend_code}.")
                try:
                    backend.wait(timeout=1)
                except subprocess.TimeoutExpired:
                    pass
        except KeyboardInterrupt:
            print("\nStopping servers...", flush=True)
            backend.terminate()
            frontend.terminate()
    except RuntimeError as exc:
        print(f"\nERROR: {exc}", file=sys.stderr)
        print("\nSuggested fix for npm install issues:", file=sys.stderr)
        print("  cd frontend", file=sys.stderr)
        print("  rm -f package-lock.json", file=sys.stderr)
        print("  npm config set registry https://registry.npmjs.org/", file=sys.stderr)
        print("  npm install --no-audit --no-fund --loglevel=verbose", file=sys.stderr)
        print("  npm run dev", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
