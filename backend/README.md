# Backend

Version: 1.0.8  
Build: 20260701.8

FastAPI backend for the Shakti Scheme Application prototype.

## Version endpoints

- `/health` returns status and version metadata.
- `/api/version` returns current version metadata.
- `/api/version-history` returns release history.

## Business-rule endpoints

- `/api/master-data` returns schemes, pass types, categories, user roles, scheme/pass rules, and validity rules.
- `/api/scheme-pass-rules` returns the local AI-style recommendation and validity rule set.

## User management endpoints

- `GET /api/users`
- `POST /api/users`
- `PATCH /api/users/{user_id}`

Run with:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

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


v1.0.8 adds safer startup handling for macOS/Python 3.13 virtual environment failures.
