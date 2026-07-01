# Shakti Scheme Application Form Data Collection

Version: 1.0.2
Build: 20260701.2
Release Date: 2026-07-01

A bilingual Kannada + English prototype for collecting citizen applications for Karnataka transport schemes, passes, category eligibility, Aadhaar details, 5 Guarantee Scheme Application Number, proof details, and consent.

## Included

- Python FastAPI backend
- React + NodeJS frontend
- SQLite database
- Left-side menu layout
- Kannada and English language toggle
- Scheme and pass master data cleaned from the provided list
- Citizen application form
- Category and proof capture
- Aadhaar and 5 Guarantee Scheme fields
- Proof document upload field
- Application register with search
- Statistics page
- Version badge, version API, release history, CHANGELOG, and VERSION.json
- Hardened npm startup handling to prevent silent install hangs

## Run the full app

```bash
python3 start_dev.py
```

Then open:

- Frontend: http://localhost:5173
- Backend health: http://localhost:8000/health
- Version API: http://localhost:8000/api/version
- Version history: http://localhost:8000/api/version-history

## Manual run

Backend:

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

Frontend:

```bash
cd frontend
rm -f package-lock.json
npm config set registry https://registry.npmjs.org/
npm install --no-audit --no-fund
npm run dev
```

## Versioning

The prototype now carries versioning in four places:

- UI sidebar and header badge
- Settings page release history
- Backend `/api/version` and `/api/version-history` endpoints
- `VERSION.json` and `CHANGELOG.md` files

For every future change, update `backend/version.py`, `frontend/package.json`, `VERSION.json`, and `CHANGELOG.md`, then package the ZIP using the same version number.

## Production hardening required

This is a working prototype. Before production use, add encryption for Aadhaar and proof documents, role-based access control, audit logs, API authentication, consent lifecycle management, backup policy, data retention rules, file malware scanning, and a production database such as PostgreSQL.


## Fix for npm install hanging

v1.0.2 removes the generated `package-lock.json` because the earlier build could include private registry URLs from the packaging environment. The frontend now uses pinned public packages and a `.npmrc` file pointing to the public npm registry.

If npm still appears stuck, run:

```bash
cd frontend
rm -f package-lock.json
npm config set registry https://registry.npmjs.org/
npm cache verify
npm install --no-audit --no-fund --loglevel=verbose
npm run dev
```

You can also start without reinstalling dependencies once `node_modules` exists:

```bash
python3 start_dev.py --skip-install
```
