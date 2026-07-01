# Changelog

## v1.0.8 — 2026-07-01

- Fixed macOS/Python 3.13 startup failure when `python -m venv` fails during `ensurepip`.
- Added `--use-system-python` startup option to bypass `.venv`.
- Added automatic system-Python fallback when virtual environment creation fails.
- Changed backend requirement from `uvicorn[standard]` to lightweight `uvicorn` to avoid unnecessary native dependency issues.
- Updated startup error messages with clearer Mac commands.

## v1.0.7 — 2026-07-01
- Fixed empty/blank tooltip boxes by suppressing the information control when no tooltip text is available.
- Added automatic Kannada-name suggestion from the English name.
- Kept the Kannada name field editable for manual corrections.
- Replaced the single eligibility proof upload with separate Proof Front Page and Proof Back Page uploads.
- Restricted eligibility proof uploads to JPG/JPEG files in the frontend and backend.
- Added database migration columns for `proof_front_file_path` and `proof_back_file_path` while preserving legacy compatibility.

## v1.0.6 — 2026-07-01
- Added automatic backend virtual environment repair for missing `.venv/bin/python` on macOS.
- Added `--reset-env` startup option to delete and recreate the backend Python environment.
- Improved startup diagnostics for broken virtual environments.

## v1.0.5 — 2026-07-01
- Converted visible explanatory notes into compact ⓘ tooltip controls.
- Added tooltip support for field hints, AI recommendation guidance, scheme/pass descriptions, settings guidance and default admin note.
- Kept labels and data visible while reducing clutter on desktop and mobile screens.
- Updated version metadata to Build 20260701.5.

## v1.0.4 — 2026-07-01

AI scheme selection, photo capture, clickable catalogue, user management and mobile UI release.

- Added local AI-style scheme/pass recommendation rules.
- On selecting a scheme, the form now shows only appropriate pass types.
- Recommended pass type is automatically selected when the scheme changes.
- Validity requested is now driven by the selected pass type.
- Validity end date is calculated automatically after selecting the validity start date.
- Age is calculated from Date of Birth and shown as a read-only field.
- Added citizen photograph upload and camera capture in the New Application form.
- Scheme and pass tiles are clickable and open a detailed information panel.
- Added user management with Admin, Data Entry Operator, Approver and Viewer roles.
- Added default prototype admin user creation: `Admin / admin123`.
- Improved mobile phone layout, horizontal menu, sticky action area, and catalogue detail modal.
- Updated backend version API, frontend package version, `VERSION.json`, README files, and release history.

## v1.0.3 — 2026-07-01

Footer version details release.

- Added a full-width footer on every page with version, build number, release date, database, and application status.
- Expanded the left sidebar footer to show complete version metadata.
- Added bilingual footer labels for English and Kannada UI modes.
- Updated `backend/version.py`, `frontend/package.json`, `VERSION.json`, README files, and release history.

## v1.0.2 — 2026-07-01

- Fixed npm install startup hang risk caused by stale/private registry URLs in the generated lock file.
- Removed `frontend/package-lock.json` from the packaged distribution.
- Added `frontend/.npmrc` pointing to the public npm registry and disabling audit/fund/progress during install.
- Pinned frontend packages to public stable versions: React 18.2.0, React DOM 18.2.0, and Vite 5.4.11.
- Updated `start_dev.py` with timeout-based npm install, clearer diagnostics, `--skip-install`, `--backend-only`, `--frontend-only`, and `--npm-timeout`.

## v1.0.1 — 2026-07-01

Versioning release.

- Added visible version number in the sidebar footer.
- Added version badge in the top header.
- Added version details and release history in Settings.
- Added backend `/api/version` and `/api/version-history` endpoints.
- Added `VERSION.json` for deployment and support reference.
- Updated frontend package version to 1.0.1.

## v1.0.0 — 2026-07-01

Initial prototype.

- Kannada + English citizen application form.
- Scheme/pass/category master data.
- Aadhaar and 5 Guarantee Scheme Application No. capture.
- Proof type, proof reference, and proof upload.
- Application register with search.
- Statistics dashboard.
- SQLite database for prototype use.
