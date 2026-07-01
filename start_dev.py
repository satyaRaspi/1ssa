#!/usr/bin/env python3
"""Start the Shakti Scheme prototype backend and frontend.

v1.0.8 adds a safer macOS/Python 3.13 startup path. If Python virtual
environment creation fails because ensurepip is broken, the script can fall
back to the current system Python and install backend packages in the user's
site-packages instead of stopping.
"""
import argparse
import json
import os
import platform
import shutil
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent
BACKEND = ROOT / "backend"
FRONTEND = ROOT / "frontend"
VENV = BACKEND / ".venv"
VERSION_FILE = ROOT / "VERSION.json"


def read_version():
    fallback = {"version": "1.0.8", "build": "20260701.8", "database": "SQLite", "status": "Prototype"}
    try:
        return {**fallback, **json.loads(VERSION_FILE.read_text(encoding="utf-8"))}
    except Exception:
        return fallback


APP_META = read_version()
APP_VERSION = APP_META["version"]
BUILD_NUMBER = APP_META["build"]


def npm_cmd():
    return "npm.cmd" if platform.system().lower().startswith("win") else "npm"


def venv_python_bin():
    if platform.system().lower().startswith("win"):
        return VENV / "Scripts" / "python.exe"
    return VENV / "bin" / "python"


def run(cmd, cwd=None, timeout=None, env=None, friendly_name=None, check=True):
    label = friendly_name or " ".join(map(str, cmd))
    print(f"> {' '.join(map(str, cmd))}", flush=True)
    try:
        return subprocess.run(
            [str(x) for x in cmd],
            cwd=str(cwd) if cwd else None,
            env=env,
            check=check,
            timeout=timeout,
        )
    except FileNotFoundError as exc:
        missing = exc.filename or cmd[0]
        raise RuntimeError(
            f"{label} could not start because this file was not found: {missing}. "
            "This usually means the virtual environment is incomplete/corrupted or the command is not installed."
        ) from exc
    except subprocess.TimeoutExpired as exc:
        raise RuntimeError(
            f"{label} took too long and was stopped. This is usually a registry, proxy, DNS, or network issue."
        ) from exc
    except subprocess.CalledProcessError as exc:
        raise RuntimeError(f"{label} failed with exit code {exc.returncode}.") from exc


def run_allow_fail(cmd, cwd=None, timeout=None, env=None, friendly_name=None):
    label = friendly_name or " ".join(map(str, cmd))
    print(f"> {' '.join(map(str, cmd))}", flush=True)
    try:
        return subprocess.run(
            [str(x) for x in cmd],
            cwd=str(cwd) if cwd else None,
            env=env,
            check=False,
            timeout=timeout,
        )
    except FileNotFoundError as exc:
        missing = exc.filename or cmd[0]
        print(f"WARNING: {label} could not start because {missing} was not found.", flush=True)
        return None
    except subprocess.TimeoutExpired:
        print(f"WARNING: {label} timed out.", flush=True)
        return None


def ensure_node_available():
    if not shutil.which(npm_cmd()):
        raise RuntimeError("npm was not found. Please install Node.js LTS, then run this script again.")
    run([npm_cmd(), "--version"], cwd=FRONTEND, timeout=20, friendly_name="npm version check")


def remove_venv():
    if VENV.exists():
        print("Removing existing backend virtual environment...", flush=True)
        shutil.rmtree(VENV)


def can_import_backend_modules(py_cmd):
    test_code = "import fastapi, uvicorn, multipart, pydantic; print('backend dependencies ok')"
    result = run_allow_fail([py_cmd, "-c", test_code], cwd=BACKEND, timeout=20, friendly_name="backend dependency import check")
    return bool(result and result.returncode == 0)


def install_backend_requirements(py_cmd, use_user=False):
    pip_probe = run_allow_fail([py_cmd, "-m", "pip", "--version"], cwd=BACKEND, timeout=30, friendly_name="pip check")
    if not pip_probe or pip_probe.returncode != 0:
        raise RuntimeError(
            "pip is not available for the selected Python. On macOS, run: python3 -m ensurepip --upgrade "
            "or install Python from python.org/Homebrew, then try again."
        )

    if not use_user:
        run([py_cmd, "-m", "pip", "install", "--upgrade", "pip"], cwd=BACKEND, timeout=180, friendly_name="pip upgrade")
        run([py_cmd, "-m", "pip", "install", "-r", "requirements.txt"], cwd=BACKEND, timeout=240, friendly_name="backend dependency install")
    else:
        print("Using system Python fallback; installing backend packages with --user.", flush=True)
        # Do not force pip self-upgrade in system/user mode; it often requires permissions and is not required.
        run([py_cmd, "-m", "pip", "install", "--user", "-r", "requirements.txt"], cwd=BACKEND, timeout=300, friendly_name="backend dependency install using system Python")


def create_backend_venv(reset=False):
    if reset:
        remove_venv()

    py = venv_python_bin()
    if VENV.exists() and py.exists():
        return str(py)

    if VENV.exists() and not py.exists():
        print("Backend virtual environment is incomplete. Recreating it once...", flush=True)
        remove_venv()

    print("Creating backend virtual environment...", flush=True)
    result = run_allow_fail([sys.executable, "-m", "venv", str(VENV)], cwd=BACKEND, timeout=180, friendly_name="Python virtual environment creation")
    if result and result.returncode == 0 and py.exists():
        return str(py)

    # venv can fail on macOS/Python 3.13 when ensurepip is damaged. Try one repair mode.
    print("WARNING: Standard virtual environment creation failed. Trying --without-pip repair mode...", flush=True)
    remove_venv()
    result = run_allow_fail([sys.executable, "-m", "venv", "--without-pip", str(VENV)], cwd=BACKEND, timeout=180, friendly_name="Python virtual environment creation without pip")
    if result and result.returncode == 0 and py.exists():
        # Try to bootstrap pip inside the venv. If this fails, caller can still fall back.
        pip_bootstrap = run_allow_fail([str(py), "-m", "ensurepip", "--upgrade", "--default-pip"], cwd=BACKEND, timeout=180, friendly_name="venv pip bootstrap")
        if pip_bootstrap and pip_bootstrap.returncode == 0:
            return str(py)

    return None


def ensure_backend(skip_install=False, reset_env=False, use_system_python=False, allow_system_fallback=True):
    if use_system_python:
        py = sys.executable
        if not skip_install:
            install_backend_requirements(py, use_user=True)
        return py

    py = create_backend_venv(reset=reset_env)
    if py:
        if not skip_install:
            install_backend_requirements(py, use_user=False)
        return py

    if not allow_system_fallback:
        raise RuntimeError(
            "Python virtual environment creation failed. Your Python install may have a broken ensurepip module. "
            "Run with --use-system-python or repair/reinstall Python."
        )

    print("\nWARNING: Virtual environment could not be created because Python ensurepip failed.", flush=True)
    print("Falling back to the current system Python for this prototype run.", flush=True)
    py = sys.executable
    if not skip_install:
        install_backend_requirements(py, use_user=True)
    elif not can_import_backend_modules(py):
        print("WARNING: --skip-install was used, but backend packages are not importable in system Python.", flush=True)
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


def start_backend(py):
    return subprocess.Popen([str(py), "-m", "uvicorn", "main:app", "--reload", "--port", "8000"], cwd=str(BACKEND))


def main():
    parser = argparse.ArgumentParser(description="Start the Shakti Scheme Application prototype.")
    parser.add_argument("--skip-install", action="store_true", help="Do not run pip install or npm install; start using existing dependencies.")
    parser.add_argument("--backend-only", action="store_true", help="Start only the backend API.")
    parser.add_argument("--frontend-only", action="store_true", help="Start only the frontend UI.")
    parser.add_argument("--npm-timeout", type=int, default=180, help="Seconds to wait for npm install before stopping it. Default: 180.")
    parser.add_argument("--reset-env", action="store_true", help="Delete and recreate the backend Python virtual environment before starting.")
    parser.add_argument("--use-system-python", action="store_true", help="Bypass backend .venv and use the current Python with --user package installs.")
    parser.add_argument("--no-system-fallback", action="store_true", help="Fail instead of falling back to system Python when venv creation fails.")
    args = parser.parse_args()

    try:
        if args.frontend_only:
            ensure_frontend(skip_install=args.skip_install, npm_timeout=args.npm_timeout)
            print(f"\nStarting frontend v{APP_VERSION} on http://localhost:5173\n", flush=True)
            subprocess.run([npm_cmd(), "run", "dev"], cwd=str(FRONTEND), check=True, env={**os.environ, "VITE_API_BASE": "http://localhost:8000"})
            return

        py = ensure_backend(
            skip_install=args.skip_install,
            reset_env=args.reset_env,
            use_system_python=args.use_system_python,
            allow_system_fallback=not args.no_system_fallback,
        )
        if args.backend_only:
            print(f"\nStarting backend v{APP_VERSION} on http://localhost:8000\n", flush=True)
            subprocess.run([str(py), "-m", "uvicorn", "main:app", "--reload", "--port", "8000"], cwd=str(BACKEND), check=True)
            return

        ensure_frontend(skip_install=args.skip_install, npm_timeout=args.npm_timeout)
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
                time.sleep(1)
        except KeyboardInterrupt:
            print("\nStopping servers...", flush=True)
            backend.terminate()
            frontend.terminate()
    except RuntimeError as exc:
        print(f"\nERROR: {exc}", file=sys.stderr)
        print("\nRecommended macOS/Python 3.13 workaround:", file=sys.stderr)
        print("  rm -rf backend/.venv", file=sys.stderr)
        print("  python3 start_dev.py --use-system-python", file=sys.stderr)
        print("\nIf your Python is healthy, you can still use:", file=sys.stderr)
        print("  python3 start_dev.py --reset-env", file=sys.stderr)
        print("\nSuggested fix for npm install issues:", file=sys.stderr)
        print("  cd frontend", file=sys.stderr)
        print("  rm -f package-lock.json", file=sys.stderr)
        print("  npm config set registry https://registry.npmjs.org/", file=sys.stderr)
        print("  npm install --no-audit --no-fund --loglevel=verbose", file=sys.stderr)
        print("  npm run dev", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
