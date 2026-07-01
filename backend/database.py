import hashlib
import os
import sqlite3
from pathlib import Path
from typing import Any, Dict, List, Optional

BASE_DIR = Path(__file__).resolve().parent
# Railway/Docker production deployments can set these to a mounted volume, for example:
# SHAKTI_DB_PATH=/data/shakti_applications.db
# SHAKTI_UPLOAD_DIR=/data/uploads
DB_PATH = Path(os.getenv("SHAKTI_DB_PATH", str(BASE_DIR / "shakti_applications.db"))).resolve()
DB_PATH.parent.mkdir(parents=True, exist_ok=True)
UPLOAD_DIR = Path(os.getenv("SHAKTI_UPLOAD_DIR", str(BASE_DIR / "uploads"))).resolve()
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

SCHEMES = [
    ("shakti", "Shakti Scheme", "ಶಕ್ತಿ ಯೋಜನೆ", "Free bus travel for women in eligible non-AC government buses across Karnataka.", "ಕರ್ನಾಟಕದ ಅರ್ಹ non-AC ಸರ್ಕಾರಿ ಬಸ್ಸುಗಳಲ್ಲಿ ಮಹಿಳೆಯರಿಗೆ ಉಚಿತ ಪ್ರಯಾಣ."),
    ("student_free", "Student Free Bus Pass Scheme", "ವಿದ್ಯಾರ್ಥಿ ಉಚಿತ ಬಸ್ ಪಾಸ್ ಯೋಜನೆ", "Free or subsidized travel for school and college students.", "ಶಾಲೆ ಮತ್ತು ಕಾಲೇಜು ವಿದ್ಯಾರ್ಥಿಗಳಿಗೆ ಉಚಿತ ಅಥವಾ ರಿಯಾಯಿತಿ ಪ್ರಯಾಣ."),
    ("bmtc_student", "BMTC Student Pass", "ಬಿಎಂಟಿಸಿ ವಿದ್ಯಾರ್ಥಿ ಪಾಸ್", "Annual student travel pass through approved channels.", "ಅಂಗೀಕೃತ ವ್ಯವಸ್ಥೆಯ ಮೂಲಕ ವಾರ್ಷಿಕ ವಿದ್ಯಾರ್ಥಿ ಪ್ರಯಾಣ ಪಾಸ್."),
    ("monthly", "Monthly Bus Pass", "ಮಾಸಿಕ ಬಸ್ ಪಾಸ್", "Unlimited monthly travel for daily commuters.", "ನಿತ್ಯ ಪ್ರಯಾಣಿಕರಿಗೆ ಮಾಸಿಕ ಅನಿಯಮಿತ ಪ್ರಯಾಣ."),
    ("daily", "Daily Pass", "ದೈನಂದಿನ ಪಾಸ್", "One-day unlimited BMTC travel pass.", "ಒಂದು ದಿನದ ಅನಿಯಮಿತ ಬಿಎಂಟಿಸಿ ಪ್ರಯಾಣ ಪಾಸ್."),
    ("vajra", "Vajra Pass", "ವಜ್ರ ಪಾಸ್", "Pass for AC Vajra buses and lower eligible services.", "ಎಸಿ ವಜ್ರ ಬಸ್ ಮತ್ತು ಅರ್ಹ ಕಡಿಮೆ ವರ್ಗದ ಸೇವೆಗಳ ಪಾಸ್."),
    ("vayu_vajra", "Vayu Vajra Service", "ವಾಯು ವಜ್ರ ಸೇವೆ", "Airport bus service between Bengaluru city and the airport.", "ಬೆಂಗಳೂರು ನಗರ ಮತ್ತು ವಿಮಾನ ನಿಲ್ದಾಣದ ನಡುವಿನ ವಿಮಾನ ನಿಲ್ದಾಣ ಬಸ್ ಸೇವೆ."),
    ("shakti_smart", "Shakti Smart Card / NFC Card", "ಶಕ್ತಿ ಸ್ಮಾರ್ಟ್ ಕಾರ್ಡ್ / ಎನ್‌ಎಫ್‌ಸಿ ಕಾರ್ಡ್", "Smart card for women passengers under Shakti scheme.", "ಶಕ್ತಿ ಯೋಜನೆಯಡಿ ಮಹಿಳಾ ಪ್ರಯಾಣಿಕರಿಗೆ ಸ್ಮಾರ್ಟ್ ಕಾರ್ಡ್."),
    ("ncmc", "NCMC Card System", "ಎನ್‌ಸಿಎಂಸಿ ಕಾರ್ಡ್ ವ್ಯವಸ್ಥೆ", "Common mobility card usable for bus and metro travel.", "ಬಸ್ ಮತ್ತು ಮೆಟ್ರೋ ಪ್ರಯಾಣಕ್ಕೆ ಬಳಸಬಹುದಾದ ಸಾಮಾನ್ಯ ಮೊಬಿಲಿಟಿ ಕಾರ್ಡ್."),
    ("qr_ticketing", "Digital QR Ticketing", "ಡಿಜಿಟಲ್ ಕ್ಯೂಆರ್ ಟಿಕೆಟ್", "QR code and UPI-based digital ticketing.", "ಕ್ಯೂಆರ್ ಕೋಡ್ ಮತ್ತು ಯುಪಿಐ ಆಧಾರಿತ ಡಿಜಿಟಲ್ ಟಿಕೆಟ್ ವ್ಯವಸ್ಥೆ."),
    ("electric_bus", "Electric Bus Programme", "ವಿದ್ಯುತ್ ಬಸ್ ಕಾರ್ಯಕ್ರಮ", "Electric bus services and related programme enrolment.", "ವಿದ್ಯುತ್ ಬಸ್ ಸೇವೆಗಳು ಮತ್ತು ಸಂಬಂಧಿತ ಕಾರ್ಯಕ್ರಮ ನೋಂದಣಿ."),
    ("senior", "Senior Citizen Concession", "ಹಿರಿಯ ನಾಗರಿಕ ರಿಯಾಯಿತಿ", "Concession benefits for eligible senior citizens.", "ಅರ್ಹ ಹಿರಿಯ ನಾಗರಿಕರಿಗೆ ರಿಯಾಯಿತಿ ಪ್ರಯೋಜನಗಳು."),
    ("corporate", "Employee / Corporate Pass Program", "ಉದ್ಯೋಗಿ / ಕಾರ್ಪೊರೇಟ್ ಪಾಸ್ ಕಾರ್ಯಕ್ರಮ", "Company-supported passes for employees.", "ಕಂಪನಿಗಳಿಂದ ಉದ್ಯೋಗಿಗಳಿಗೆ ನೀಡುವ ಪ್ರಯಾಣ ಪಾಸ್."),
    ("premium_suburban", "Premium Suburban Services", "ಪ್ರೀಮಿಯಂ ಉಪನಗರ ಸೇವೆಗಳು", "Premium suburban service passes including Vajra Vistara where applicable.", "ವಜ್ರ ವಿಸ್ತಾರ ಸೇರಿದಂತೆ ಅನ್ವಯವಾಗುವ ಪ್ರೀಮಿಯಂ ಉಪನಗರ ಸೇವೆಗಳ ಪಾಸ್."),
]

PASS_TYPES = [
    ("one_day", "One Day Travel", "ಒಂದು ದಿನದ ಪ್ರಯಾಣ", "Unlimited travel for one day on eligible BMTC buses."),
    ("weekly", "Weekly Pass", "ವಾರದ ಪಾಸ್", "Valid for 7 days on selected services."),
    ("monthly", "Monthly Pass", "ಮಾಸಿಕ ಪಾಸ್", "Unlimited monthly travel for regular passengers."),
    ("ordinary", "Ordinary Bus Pass", "ಸಾಮಾನ್ಯ ಬಸ್ ಪಾಸ್", "Valid only for normal non-AC buses."),
    ("suvarna", "Suvarna Pass", "ಸುವರ್ಣ ಪಾಸ್", "Valid for Suvarna services and ordinary buses."),
    ("vajra", "Vajra Pass", "ವಜ್ರ ಪಾಸ್", "For AC Vajra buses and lower-category buses."),
    ("vayu_vajra", "Vayu Vajra Pass", "ವಾಯು ವಜ್ರ ಪಾಸ್", "Special pass for airport buses."),
    ("student", "Student Pass", "ವಿದ್ಯಾರ್ಥಿ ಪಾಸ್", "Discount or free pass for school and college students."),
    ("shakti_smart", "Shakti Smart Card", "ಶಕ್ತಿ ಸ್ಮಾರ್ಟ್ ಕಾರ್ಡ್", "Free travel card for women under Karnataka Shakti Scheme."),
    ("senior", "Senior Citizen Pass", "ಹಿರಿಯ ನಾಗರಿಕ ಪಾಸ್", "Concession pass for eligible senior citizens."),
    ("ncmc", "NCMC Smart Card", "ಎನ್‌ಸಿಎಂಸಿ ಸ್ಮಾರ್ಟ್ ಕಾರ್ಡ್", "Rechargeable smart mobility card usable for BMTC and metro."),
    ("corporate", "Corporate Pass", "ಕಾರ್ಪೊರೇಟ್ ಪಾಸ್", "Passes provided through companies for employees."),
    ("integrated", "Integrated Metro + BMTC Pass", "ಮೆಟ್ರೋ + ಬಿಎಂಟಿಸಿ ಸಂಯೋಜಿತ ಪಾಸ್", "Combined travel pass for BMTC buses and Namma Metro."),
    ("institutional", "Group / Institutional Pass", "ಗುಂಪು / ಸಂಸ್ಥೆಯ ಪಾಸ್", "Special passes for schools, colleges, and organizations."),
    ("tour_event", "Tour / Special Event Pass", "ಪ್ರವಾಸ / ವಿಶೇಷ ಕಾರ್ಯಕ್ರಮ ಪಾಸ್", "Special pass for tour or event-based travel."),
]

CATEGORIES = [
    ("woman", "Woman Passenger", "ಮಹಿಳಾ ಪ್ರಯಾಣಿಕರು"),
    ("student", "Student", "ವಿದ್ಯಾರ್ಥಿ"),
    ("senior", "Senior Citizen", "ಹಿರಿಯ ನಾಗರಿಕ"),
    ("disabled", "Person with Disability", "ವಿಕಲಚೇತನರು"),
    ("armed_forces", "Armed Forces / Ex-Servicemen", "ಸಶಸ್ತ್ರ ಪಡೆ / ಮಾಜಿ ಸೈನಿಕರು"),
    ("corporate", "Corporate Employee", "ಕಾರ್ಪೊರೇಟ್ ಉದ್ಯೋಗಿ"),
    ("institution", "Institution / Group", "ಸಂಸ್ಥೆ / ಗುಂಪು"),
    ("general", "General Citizen", "ಸಾಮಾನ್ಯ ನಾಗರಿಕ"),
    ("other", "Other", "ಇತರೆ"),
]

# Local AI-style recommendation rules used by the UI and backend. This keeps the prototype
# explainable and offline while behaving like an assisted selection engine.
SCHEME_PASS_RULES: Dict[str, Dict[str, Any]] = {
    "shakti": {
        "default_pass_type": "shakti_smart",
        "allowed_pass_types": ["shakti_smart", "ordinary"],
        "default_validity": "Annual",
        "eligible_categories": ["woman"],
        "service_scope": "Non-AC government buses across Karnataka, subject to scheme rules.",
        "ai_reason": "Selected because Shakti applies primarily to women passengers using eligible non-AC services.",
    },
    "student_free": {
        "default_pass_type": "student",
        "allowed_pass_types": ["student", "institutional"],
        "default_validity": "Academic Year",
        "eligible_categories": ["student"],
        "service_scope": "School/college commute routes, subject to student eligibility and institution proof.",
        "ai_reason": "Selected because student proof and institution details are required for student benefit validation.",
    },
    "bmtc_student": {
        "default_pass_type": "student",
        "allowed_pass_types": ["student"],
        "default_validity": "Academic Year",
        "eligible_categories": ["student"],
        "service_scope": "BMTC annual student travel pass.",
        "ai_reason": "Mapped to Student Pass because it is an annual student travel product.",
    },
    "monthly": {
        "default_pass_type": "monthly",
        "allowed_pass_types": ["monthly", "ordinary", "suvarna", "vajra", "integrated", "ncmc"],
        "default_validity": "Monthly",
        "eligible_categories": ["general", "woman", "senior", "disabled", "armed_forces"],
        "service_scope": "Daily commuter travel for selected service class.",
        "ai_reason": "Mapped to monthly validity because the selected scheme is meant for regular commuters.",
    },
    "daily": {
        "default_pass_type": "one_day",
        "allowed_pass_types": ["one_day", "tour_event"],
        "default_validity": "One Day",
        "eligible_categories": ["general", "woman", "student", "senior"],
        "service_scope": "One-day unlimited travel on eligible services.",
        "ai_reason": "Mapped to one-day validity because this scheme is meant for same-day travel.",
    },
    "vajra": {
        "default_pass_type": "vajra",
        "allowed_pass_types": ["vajra", "monthly", "ncmc"],
        "default_validity": "Monthly",
        "eligible_categories": ["general", "corporate", "senior"],
        "service_scope": "AC Vajra buses and lower eligible service categories.",
        "ai_reason": "Selected because Vajra service requires an AC-compatible pass type.",
    },
    "vayu_vajra": {
        "default_pass_type": "vayu_vajra",
        "allowed_pass_types": ["vayu_vajra", "one_day", "ncmc"],
        "default_validity": "One Day",
        "eligible_categories": ["general", "corporate"],
        "service_scope": "Airport bus service between Bengaluru and Kempegowda International Airport.",
        "ai_reason": "Selected because airport bus products require Vayu Vajra-compatible pass types.",
    },
    "shakti_smart": {
        "default_pass_type": "shakti_smart",
        "allowed_pass_types": ["shakti_smart"],
        "default_validity": "Annual",
        "eligible_categories": ["woman"],
        "service_scope": "Smart card/NFC token for Shakti women passenger eligibility.",
        "ai_reason": "Selected because the smart card product is specific to Shakti Scheme beneficiaries.",
    },
    "ncmc": {
        "default_pass_type": "ncmc",
        "allowed_pass_types": ["ncmc", "integrated", "monthly"],
        "default_validity": "5 Years",
        "eligible_categories": ["general", "woman", "student", "senior", "corporate"],
        "service_scope": "Rechargeable common mobility card usable for supported bus and metro services.",
        "ai_reason": "Selected because NCMC is a stored-value mobility card with longer card validity.",
    },
    "qr_ticketing": {
        "default_pass_type": "one_day",
        "allowed_pass_types": ["one_day", "weekly", "monthly", "tour_event"],
        "default_validity": "One Day",
        "eligible_categories": ["general", "woman", "student", "senior"],
        "service_scope": "QR/UPI-based digital ticket or digital pass validity.",
        "ai_reason": "Selected because QR ticketing can be issued for short-duration digital validity.",
    },
    "electric_bus": {
        "default_pass_type": "monthly",
        "allowed_pass_types": ["one_day", "weekly", "monthly", "ncmc"],
        "default_validity": "Monthly",
        "eligible_categories": ["general", "woman", "student", "senior", "corporate"],
        "service_scope": "Electric bus routes and services based on selected route/service class.",
        "ai_reason": "Selected because electric fleet services may use daily, weekly, monthly or smart mobility products.",
    },
    "senior": {
        "default_pass_type": "senior",
        "allowed_pass_types": ["senior", "ordinary", "monthly"],
        "default_validity": "Annual",
        "eligible_categories": ["senior"],
        "service_scope": "Concession benefits for eligible senior citizens.",
        "ai_reason": "Selected because age/category proof is required for senior citizen concession.",
    },
    "corporate": {
        "default_pass_type": "corporate",
        "allowed_pass_types": ["corporate", "vajra", "monthly", "integrated", "ncmc"],
        "default_validity": "Monthly",
        "eligible_categories": ["corporate"],
        "service_scope": "Employer-sponsored employee commute products.",
        "ai_reason": "Selected because employer details are required for corporate pass issuance.",
    },
    "premium_suburban": {
        "default_pass_type": "vajra",
        "allowed_pass_types": ["vajra", "suvarna", "monthly", "integrated", "corporate"],
        "default_validity": "Monthly",
        "eligible_categories": ["general", "corporate"],
        "service_scope": "Premium suburban services including Vajra Vistara where applicable.",
        "ai_reason": "Selected because premium suburban routes require premium or integrated service products.",
    },
}

PASS_VALIDITY_RULES: Dict[str, Dict[str, Any]] = {
    "one_day": {"options": ["One Day"], "default": "One Day", "days": 1, "explain": "End date remains the same as the start date."},
    "weekly": {"options": ["Weekly"], "default": "Weekly", "days": 7, "explain": "End date is calculated as 7 calendar days including the start date."},
    "monthly": {"options": ["Monthly"], "default": "Monthly", "months": 1, "explain": "End date is calculated as one calendar month minus one day."},
    "ordinary": {"options": ["Monthly", "Annual"], "default": "Monthly", "months": 1, "explain": "Ordinary pass normally uses monthly or annual validity."},
    "suvarna": {"options": ["Monthly", "Annual"], "default": "Monthly", "months": 1, "explain": "Suvarna pass validity follows selected monthly or annual cycle."},
    "vajra": {"options": ["Monthly", "Quarterly", "Annual"], "default": "Monthly", "months": 1, "explain": "Vajra pass validity is calculated from the selected AC pass cycle."},
    "vayu_vajra": {"options": ["One Day", "Monthly"], "default": "One Day", "days": 1, "explain": "Airport service can be issued as a trip/day pass or monthly pass."},
    "student": {"options": ["Academic Year", "Annual"], "default": "Academic Year", "months": 12, "explain": "Student pass uses academic-year/annual validity."},
    "shakti_smart": {"options": ["Annual", "5 Years"], "default": "Annual", "years": 1, "explain": "Shakti smart card defaults to annual validation and can support longer card validity."},
    "senior": {"options": ["Annual", "5 Years"], "default": "Annual", "years": 1, "explain": "Senior citizen concession is normally validated annually or periodically."},
    "ncmc": {"options": ["5 Years", "Custom"], "default": "5 Years", "years": 5, "explain": "NCMC is a smart mobility card with longer card validity."},
    "corporate": {"options": ["Monthly", "Quarterly", "Annual"], "default": "Monthly", "months": 1, "explain": "Corporate pass follows employer-approved validity cycle."},
    "integrated": {"options": ["Monthly", "Quarterly", "Annual"], "default": "Monthly", "months": 1, "explain": "Integrated BMTC + Metro pass follows a selected commuter cycle."},
    "institutional": {"options": ["Weekly", "Monthly", "Academic Year"], "default": "Monthly", "months": 1, "explain": "Institution/group pass validity depends on group usage period."},
    "tour_event": {"options": ["One Day", "Weekly", "Custom"], "default": "One Day", "days": 1, "explain": "Tour/event passes are short-duration passes."},
}

USER_ROLES = ["Admin", "Data Entry Operator", "Approver", "Viewer"]


def get_connection() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def rows_to_dicts(rows: List[sqlite3.Row]) -> List[Dict[str, Any]]:
    return [dict(row) for row in rows]


def ensure_column(cur: sqlite3.Cursor, table: str, column: str, definition: str) -> None:
    columns = [row[1] for row in cur.execute(f"PRAGMA table_info({table})").fetchall()]
    if column not in columns:
        cur.execute(f"ALTER TABLE {table} ADD COLUMN {column} {definition}")


def hash_password(password: str) -> str:
    salt = os.urandom(16).hex()
    digest = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt.encode("utf-8"), 120_000).hex()
    return f"pbkdf2_sha256${salt}${digest}"


def init_db() -> None:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS schemes (
            code TEXT PRIMARY KEY,
            name_en TEXT NOT NULL,
            name_kn TEXT NOT NULL,
            description_en TEXT,
            description_kn TEXT
        )
    """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS pass_types (
            code TEXT PRIMARY KEY,
            name_en TEXT NOT NULL,
            name_kn TEXT NOT NULL,
            description_en TEXT
        )
    """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS categories (
            code TEXT PRIMARY KEY,
            name_en TEXT NOT NULL,
            name_kn TEXT NOT NULL
        )
    """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS applications (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            application_no TEXT UNIQUE NOT NULL,
            created_at TEXT NOT NULL,
            status TEXT NOT NULL DEFAULT 'Draft',
            scheme_code TEXT NOT NULL,
            pass_type_code TEXT NOT NULL,
            validity_type TEXT,
            validity_start TEXT,
            validity_end TEXT,
            name_en TEXT NOT NULL,
            name_kn TEXT,
            age INTEGER,
            date_of_birth TEXT,
            gender TEXT,
            category_code TEXT,
            category_other TEXT,
            mobile TEXT,
            email TEXT,
            aadhaar_number TEXT,
            aadhaar_name TEXT,
            aadhaar_dob TEXT,
            aadhaar_gender TEXT,
            five_guarantee_application_no TEXT,
            address_line_1 TEXT,
            address_line_2 TEXT,
            district TEXT,
            taluk TEXT,
            city TEXT,
            pincode TEXT,
            proof_type TEXT,
            proof_reference_no TEXT,
            proof_file_path TEXT,
            proof_front_file_path TEXT,
            proof_back_file_path TEXT,
            citizen_photo_path TEXT,
            institution_name TEXT,
            employer_name TEXT,
            route_preference TEXT,
            service_preference TEXT,
            consent_data_use INTEGER DEFAULT 0,
            consent_aadhaar_verification INTEGER DEFAULT 0,
            consent_terms INTEGER DEFAULT 0,
            remarks TEXT
        )
    """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            full_name TEXT NOT NULL,
            role TEXT NOT NULL,
            mobile TEXT,
            email TEXT,
            password_hash TEXT NOT NULL,
            is_active INTEGER NOT NULL DEFAULT 1,
            created_at TEXT NOT NULL
        )
    """)
    ensure_column(cur, "applications", "citizen_photo_path", "TEXT")
    ensure_column(cur, "applications", "proof_front_file_path", "TEXT")
    ensure_column(cur, "applications", "proof_back_file_path", "TEXT")
    cur.executemany("INSERT OR REPLACE INTO schemes VALUES (?, ?, ?, ?, ?)", SCHEMES)
    cur.executemany("INSERT OR REPLACE INTO pass_types VALUES (?, ?, ?, ?)", PASS_TYPES)
    cur.executemany("INSERT OR REPLACE INTO categories VALUES (?, ?, ?)", CATEGORIES)
    existing_admin = cur.execute("SELECT id FROM users WHERE username = ?", ("Admin",)).fetchone()
    if not existing_admin:
        cur.execute(
            """
            INSERT INTO users (username, full_name, role, mobile, email, password_hash, is_active, created_at)
            VALUES (?, ?, ?, ?, ?, ?, 1, datetime('now'))
            """,
            ("Admin", "System Administrator", "Admin", "", "", hash_password("admin123")),
        )
    conn.commit()
    conn.close()


def fetch_all(table: str) -> List[Dict[str, Any]]:
    allowed = {"schemes", "pass_types", "categories", "applications"}
    if table not in allowed:
        raise ValueError("Invalid table")
    conn = get_connection()
    rows = conn.execute(f"SELECT * FROM {table}").fetchall()
    conn.close()
    return rows_to_dicts(rows)


def create_application(data: Dict[str, Any]) -> Dict[str, Any]:
    conn = get_connection()
    cur = conn.cursor()
    columns = list(data.keys())
    placeholders = ",".join(["?"] * len(columns))
    sql = f"INSERT INTO applications ({','.join(columns)}) VALUES ({placeholders})"
    cur.execute(sql, [data[col] for col in columns])
    conn.commit()
    app_id = cur.lastrowid
    row = conn.execute("SELECT * FROM applications WHERE id = ?", (app_id,)).fetchone()
    conn.close()
    return dict(row)


def list_applications(search: Optional[str] = None, status: Optional[str] = None) -> List[Dict[str, Any]]:
    conn = get_connection()
    sql = """
        SELECT a.*, s.name_en AS scheme_name_en, s.name_kn AS scheme_name_kn,
               p.name_en AS pass_name_en, p.name_kn AS pass_name_kn,
               c.name_en AS category_name_en, c.name_kn AS category_name_kn
        FROM applications a
        LEFT JOIN schemes s ON a.scheme_code = s.code
        LEFT JOIN pass_types p ON a.pass_type_code = p.code
        LEFT JOIN categories c ON a.category_code = c.code
        WHERE 1=1
    """
    params: List[Any] = []
    if search:
        like = f"%{search}%"
        sql += " AND (a.application_no LIKE ? OR a.name_en LIKE ? OR a.mobile LIKE ? OR a.five_guarantee_application_no LIKE ?)"
        params.extend([like, like, like, like])
    if status:
        sql += " AND a.status = ?"
        params.append(status)
    sql += " ORDER BY a.id DESC"
    rows = conn.execute(sql, params).fetchall()
    conn.close()
    return rows_to_dicts(rows)


def get_application(app_id: int) -> Optional[Dict[str, Any]]:
    conn = get_connection()
    row = conn.execute("SELECT * FROM applications WHERE id = ?", (app_id,)).fetchone()
    conn.close()
    return dict(row) if row else None


def stats() -> Dict[str, Any]:
    conn = get_connection()
    total = conn.execute("SELECT COUNT(*) AS count FROM applications").fetchone()["count"]
    users_total = conn.execute("SELECT COUNT(*) AS count FROM users").fetchone()["count"]
    by_status = rows_to_dicts(conn.execute("SELECT status, COUNT(*) AS count FROM applications GROUP BY status").fetchall())
    by_scheme = rows_to_dicts(conn.execute("""
        SELECT s.name_en AS scheme, COUNT(a.id) AS count
        FROM schemes s LEFT JOIN applications a ON a.scheme_code = s.code
        GROUP BY s.code ORDER BY count DESC, s.name_en
    """).fetchall())
    by_category = rows_to_dicts(conn.execute("""
        SELECT c.name_en AS category, COUNT(a.id) AS count
        FROM categories c LEFT JOIN applications a ON a.category_code = c.code
        GROUP BY c.code ORDER BY count DESC, c.name_en
    """).fetchall())
    conn.close()
    return {"total": total, "users_total": users_total, "by_status": by_status, "by_scheme": by_scheme, "by_category": by_category}


def list_users(search: Optional[str] = None) -> List[Dict[str, Any]]:
    conn = get_connection()
    sql = "SELECT id, username, full_name, role, mobile, email, is_active, created_at FROM users WHERE 1=1"
    params: List[Any] = []
    if search:
        like = f"%{search}%"
        sql += " AND (username LIKE ? OR full_name LIKE ? OR role LIKE ? OR mobile LIKE ? OR email LIKE ?)"
        params.extend([like, like, like, like, like])
    sql += " ORDER BY id DESC"
    rows = conn.execute(sql, params).fetchall()
    conn.close()
    return rows_to_dicts(rows)


def create_user(data: Dict[str, Any]) -> Dict[str, Any]:
    role = data.get("role") or "Data Entry Operator"
    if role not in USER_ROLES:
        role = "Data Entry Operator"
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        """
        INSERT INTO users (username, full_name, role, mobile, email, password_hash, is_active, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, datetime('now'))
        """,
        (
            data["username"].strip(),
            data["full_name"].strip(),
            role,
            data.get("mobile", ""),
            data.get("email", ""),
            hash_password(data.get("password") or "ChangeMe@123"),
            1 if data.get("is_active", True) in [True, 1, "1", "true", "on"] else 0,
        ),
    )
    conn.commit()
    user_id = cur.lastrowid
    row = conn.execute("SELECT id, username, full_name, role, mobile, email, is_active, created_at FROM users WHERE id = ?", (user_id,)).fetchone()
    conn.close()
    return dict(row)


def update_user(user_id: int, data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    allowed = {"full_name", "role", "mobile", "email", "is_active"}
    assignments = []
    params: List[Any] = []
    for key in allowed:
        if key in data:
            value = data[key]
            if key == "role" and value not in USER_ROLES:
                continue
            if key == "is_active":
                value = 1 if value in [True, 1, "1", "true", "on"] else 0
            assignments.append(f"{key} = ?")
            params.append(value)
    if data.get("password"):
        assignments.append("password_hash = ?")
        params.append(hash_password(data["password"]))
    if not assignments:
        return get_user(user_id)
    params.append(user_id)
    conn = get_connection()
    conn.execute(f"UPDATE users SET {', '.join(assignments)} WHERE id = ?", params)
    conn.commit()
    row = conn.execute("SELECT id, username, full_name, role, mobile, email, is_active, created_at FROM users WHERE id = ?", (user_id,)).fetchone()
    conn.close()
    return dict(row) if row else None


def get_user(user_id: int) -> Optional[Dict[str, Any]]:
    conn = get_connection()
    row = conn.execute("SELECT id, username, full_name, role, mobile, email, is_active, created_at FROM users WHERE id = ?", (user_id,)).fetchone()
    conn.close()
    return dict(row) if row else None
