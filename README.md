# Shakti Scheme Application Form Data Collection

Version: 1.0.8  
Build: 20260701.8  
Release Date: 2026-07-01

A bilingual Kannada + English prototype for collecting citizen applications for Karnataka transport schemes, passes, category eligibility, Aadhaar details, 5 Guarantee Scheme Application Number, proof details, citizen photograph, consent, and user-managed back-office operations.

## Included

- Python FastAPI backend
- React + NodeJS frontend
- SQLite database
- Left-side menu layout with mobile optimized navigation
- Kannada and English language toggle
- Scheme and pass master data cleaned from the provided list
- AI-assisted scheme/pass recommendation rules
- Only appropriate pass types shown for the selected scheme
- Recommended pass type and validity automatically selected
- Validity end date calculated automatically from start date and requested validity
- DOB-based age calculation with read-only age field
- Citizen application form
- Citizen photograph upload or camera capture
- Category and proof capture
- Aadhaar and 5 Guarantee Scheme fields
- Eligibility proof upload split into front-page and back-page JPG-only fields
- Application register with search
- Clickable scheme/pass catalogue tiles with detailed information
- User management with Admin, Data Entry Operator, Approver, and Viewer roles
- Statistics page
- Footer version details, version badge, version API, release history, CHANGELOG, and VERSION.json
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


## v1.0.8 update

This release includes the latest form refinements requested for field usability and document control:

- Empty/blank tooltip boxes are suppressed. Information icons appear only when tooltip text exists.
- Kannada name is automatically suggested when the English name is entered. The Kannada field remains editable, so the operator can correct or replace the suggestion.
- Eligibility proof upload is split into two separate files:
  - Proof Front Page
  - Proof Back Page
- Eligibility proof files are restricted to JPG/JPEG only in both frontend and backend validation.
- SQLite schema now stores `proof_front_file_path` and `proof_back_file_path` while keeping legacy `proof_file_path` compatibility.

## v1.0.6 update

This release fixes the macOS startup issue where `backend/.venv` exists but `backend/.venv/bin/python` is missing. The startup script now detects an incomplete backend virtual environment, recreates it once automatically, and also supports:

```bash
python3 start_dev.py --reset-env
```

All earlier features remain included: tooltip-based clean UI, AI-assisted scheme/pass selection, automatic validity calculation, DOB-based read-only age, citizen photo upload/camera capture, clickable scheme/pass tiles, user management, and mobile phone optimization.

## Demo user

A default demo admin user is created when the database is initialized:

```text
Username: Admin
Password: admin123
```

This is for prototype use only. Change it before production use.

## Versioning

The prototype carries versioning in these places:

- UI footer, sidebar, and header badge
- Settings page release history
- Backend `/api/version` and `/api/version-history` endpoints
- `VERSION.json` and `CHANGELOG.md` files

For every future change, update `backend/version.py`, `frontend/package.json`, `VERSION.json`, and `CHANGELOG.md`, then package the ZIP using the same version number.

## Fix for npm install hanging

v1.0.2 removed the generated `package-lock.json` because an earlier build could include private registry URLs from the packaging environment. The frontend uses pinned public packages and a `.npmrc` file pointing to the public npm registry.

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

## Production hardening required

This is a working prototype. Before production use, add encryption for Aadhaar and proof documents, encryption for citizen photographs, role-based access control, API authentication, audit logs, consent lifecycle management, backup policy, data retention rules, file malware scanning, secure object storage, and a production database such as PostgreSQL.

### Backend virtual environment repair

If startup reports that `backend/.venv/bin/python` is missing, run:

```bash
python3 start_dev.py --reset-env
```

Or manually delete the broken environment and restart:

```bash
rm -rf backend/.venv
python3 start_dev.py
```
