# Changelog

## 1.0.10 - 2026-07-01

- Packaged latest build as Git-ready and Railway-ready for `satyaRaspi/1ssa`.
- Added `GIT_STEPS.md` with exact commands for pushing to GitHub.
- Updated `DEPLOYMENT.md` and `README.md` to use `satyaRaspi/1ssa`.
- Confirmed deployment assets are present: `Dockerfile`, `railway.json`, `.gitignore`, and `.dockerignore`.

## v1.0.9 - GitHub and Railway Deployment Release

Build: 20260701.9  
Release Date: 2026-07-01

### Added

- Railway-ready `Dockerfile` for single-service deployment.
- `railway.json` using Dockerfile builder, `/health` health check, and restart policy.
- Same-origin API support for deployed frontend.
- FastAPI static serving for the built React frontend from `frontend/dist`.
- `SHAKTI_DB_PATH` and `SHAKTI_UPLOAD_DIR` environment variable support for persistent Railway volume usage.
- `.gitignore` and `.dockerignore` for clean GitHub and Docker builds.
- `DEPLOYMENT.md` with GitHub and Railway steps for the `satyaraspi` account.

### Notes

- The app can now be deployed as one Railway service.
- For persistent SQLite data and uploaded citizen/proof photos, mount a Railway volume at `/data`.

## v1.0.8 - Kannada Name and Proof Upload Refinement Release

- Fixed blank tooltip boxes by trimming and validating tooltip text before display.
- Added automatic Kannada-name suggestion when the English name is entered; the Kannada field remains editable.
- Split eligibility proof upload into Proof Front Page and Proof Back Page fields.
- Restricted eligibility proof uploads to JPG/JPEG files in frontend and backend validation.
- Added database columns for `proof_front_file_path` and `proof_back_file_path` while keeping legacy `proof_file_path` compatibility.

## v1.0.6 - Backend Environment Repair Release

- Automatically detects an incomplete backend virtual environment and recreates it once.
- Added `--reset-env` startup option for deleting and rebuilding `backend/.venv`.
- Improved error messages for missing `.venv/bin/python` and related startup issues.

## v1.0.5 - Tooltip UI Cleanup Release

- Converted visible explanatory notes into compact information icons with hover/focus tooltips.
- Moved field hints, AI recommendation explanations, catalogue descriptions, settings notes and default admin guidance behind the ⓘ control.
- Improved catalogue cards to remain clickable while supporting information tooltips.

## v1.0.4 - AI Scheme Selection, Photo Capture and User Management Release

- Added local AI-style scheme/pass recommendation rules to show only valid pass types for the selected scheme.
- Automatically selects the recommended pass type and validity when the scheme changes.
- Validity end date is auto-calculated from the selected start date and requested validity.
- Age is calculated from date of birth and shown as a read-only field.
- Citizen photograph can now be uploaded or captured from camera on the new application form.
- Scheme and pass master tiles are clickable and open detailed information panels.
- Added user management with Admin, Data Entry Operator, Approver and Viewer roles.
- Improved mobile phone layout, navigation and form usability.

## v1.0.3 - Footer Version Details Release

- Added a full-width footer on every page with version, build, release date, database, and status.
- Expanded the left sidebar footer to show complete version metadata.
- Added bilingual labels for database, status, and footer product text.

## v1.0.2 - Startup Stability Release

- Removed generated `package-lock.json` to avoid private build-registry URLs on user machines.
- Pinned React and Vite dependencies to stable public versions.
- Added `.npmrc` with public npm registry, audit disabled, funding disabled, and progress disabled.
- Updated `start_dev.py` with npm timeout, clearer error message, `--skip-install`, `--backend-only`, `--frontend-only`, and `--npm-timeout` options.

## v1.0.1 - Versioning Release

- Application version shown in sidebar, header, settings, and README.
- Backend exposes `/api/version` and `/api/version-history`.
- Frontend package version updated to `1.0.1`.
- CHANGELOG and VERSION metadata files added.

## v1.0.0 - Initial Prototype

- Bilingual Kannada and English citizen application form.
- SQLite-backed schemes, passes, categories, applications, proof upload, search, and statistics.
- Clean left-side menu layout for demo and review.
