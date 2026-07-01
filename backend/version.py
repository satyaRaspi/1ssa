APP_NAME = "Shakti Scheme Application Form Data Collection"
APP_VERSION = "1.0.8"
BUILD_NUMBER = "20260701.8"
RELEASE_DATE = "2026-07-01"
DATABASE_ENGINE = "SQLite"
APP_STATUS = "Prototype"
RELEASE_NOTES = [
    "Fixed empty tooltip boxes by hiding information icons when no help text exists.",
    "Added automatic Kannada-name suggestion from the English name while keeping the Kannada field editable.",
    "Changed eligibility proof capture to separate front-page and back-page JPG-only uploads."
]
VERSION_HISTORY = [
    {
        "version": "1.0.8",
        "build": "20260701.8",
        "release_date": "2026-07-01",
        "title": "Kannada Name and Proof Upload Refinement Release",
        "changes": [
            "Fixed blank tooltip boxes by trimming and validating tooltip text before display.",
            "Added automatic Kannada-name suggestion when the English name is entered; the Kannada field remains editable.",
            "Split eligibility proof upload into Proof Front Page and Proof Back Page fields.",
            "Restricted eligibility proof uploads to JPG/JPEG files in frontend and backend validation.",
            "Added database columns for proof_front_file_path and proof_back_file_path while keeping legacy proof_file_path compatibility."
        ]
    },
    {
        "version": "1.0.6",
        "build": "20260701.6",
        "release_date": "2026-07-01",
        "title": "Backend Environment Repair Release",
        "changes": [
            "Automatically detects an incomplete backend virtual environment and recreates it once.",
            "Added --reset-env startup option for deleting and rebuilding backend/.venv.",
            "Improved error messages for missing .venv/bin/python and related startup issues.",
            "Updated footer, settings, backend API, README and changelog to v1.0.6."
        ]
    },
    {
        "version": "1.0.5",
        "build": "20260701.5",
        "release_date": "2026-07-01",
        "title": "Tooltip UI Cleanup Release",
        "changes": [
            "Converted visible explanatory notes into compact information icons with hover/focus tooltips.",
            "Moved field hints, AI recommendation explanations, catalogue descriptions, settings notes and default admin guidance behind the ⓘ control.",
            "Improved catalogue cards to remain clickable while supporting information tooltips."
        ]
    },
    {
        "version": "1.0.4",
        "build": "20260701.4",
        "release_date": "2026-07-01",
        "title": "AI Scheme Selection, Photo Capture and User Management Release",
        "changes": [
            "Added local AI-style scheme/pass recommendation rules to show only valid pass types for the selected scheme.",
            "Automatically selects the recommended pass type and validity when the scheme changes.",
            "Validity end date is auto-calculated from the selected start date and requested validity.",
            "Age is calculated from date of birth and shown as a read-only field.",
            "Citizen photograph can now be uploaded or captured from camera on the new application form.",
            "Scheme and pass master tiles are clickable and open detailed information panels.",
            "Added user management with Admin, Data Entry Operator, Approver and Viewer roles.",
            "Improved mobile phone layout, navigation and form usability."
        ]
    },
    {
        "version": "1.0.3",
        "build": "20260701.3",
        "release_date": "2026-07-01",
        "title": "Footer Version Details Release",
        "changes": [
            "Added a full-width footer on every page with version, build, release date, database, and status.",
            "Expanded the left sidebar footer to show complete version metadata.",
            "Added bilingual labels for database, status, and footer product text.",
            "Updated backend version API, VERSION.json, README, and CHANGELOG to v1.0.3."
        ]
    },
    {
        "version": "1.0.2",
        "build": "20260701.2",
        "release_date": "2026-07-01",
        "title": "Startup Stability Release",
        "changes": [
            "Removed package-lock.json from the distribution to avoid private build-registry URLs on user machines.",
            "Pinned React and Vite dependencies to stable public versions.",
            "Added .npmrc with public npm registry, audit disabled, funding disabled, and progress disabled.",
            "Updated start_dev.py with npm timeout, clearer error message, --skip-install, --backend-only, --frontend-only, and --npm-timeout options."
        ]
    },
    {
        "version": "1.0.1",
        "build": "20260701.1",
        "release_date": "2026-07-01",
        "title": "Versioning Release",
        "changes": [
            "Application version shown in sidebar, header, settings, and README.",
            "Backend exposes /api/version and /api/version-history.",
            "Frontend package version updated to 1.0.1.",
            "CHANGELOG and VERSION metadata files added."
        ]
    },
    {
        "version": "1.0.0",
        "build": "20260701.0",
        "release_date": "2026-07-01",
        "title": "Initial Prototype",
        "changes": [
            "Bilingual Kannada and English citizen application form.",
            "SQLite-backed schemes, passes, categories, applications, proof upload, search, and statistics.",
            "Clean left-side menu layout for demo and review."
        ]
    }
]


def version_payload():
    return {
        "app_name": APP_NAME,
        "version": APP_VERSION,
        "build": BUILD_NUMBER,
        "release_date": RELEASE_DATE,
        "database": DATABASE_ENGINE,
        "status": APP_STATUS,
        "release_notes": RELEASE_NOTES,
    }
