import base64
import json
import re
import uuid
from datetime import datetime
from pathlib import Path
from typing import Optional

from fastapi import FastAPI, File, Form, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from database import (
    PASS_VALIDITY_RULES,
    SCHEME_PASS_RULES,
    UPLOAD_DIR,
    USER_ROLES,
    create_application,
    create_user,
    fetch_all,
    get_application,
    init_db,
    list_applications,
    list_users,
    stats,
    update_user,
)
from version import APP_VERSION, VERSION_HISTORY, version_payload

app = FastAPI(title="Shakti Scheme Application Data Collection API", version=APP_VERSION)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

init_db()
app.mount("/uploads", StaticFiles(directory=str(UPLOAD_DIR)), name="uploads")

REQUIRED_FIELDS = ["scheme_code", "pass_type_code", "name_en", "gender", "category_code", "mobile"]


def save_upload(file: UploadFile, prefix: str) -> Optional[str]:
    if not file or not file.filename:
        return None
    safe_name = Path(file.filename).name.replace(" ", "_")
    stored_name = f"{prefix}_{uuid.uuid4().hex[:8]}_{safe_name}"
    stored_path = UPLOAD_DIR / stored_name
    return str(stored_path), f"/uploads/{stored_name}"


def is_jpg_upload(file: UploadFile) -> bool:
    if not file or not file.filename:
        return True
    filename = Path(file.filename).name.lower()
    has_jpg_extension = filename.endswith(".jpg") or filename.endswith(".jpeg")
    has_jpg_content_type = (file.content_type or "").lower() in {"image/jpeg", "image/pjpeg", ""}
    return has_jpg_extension and has_jpg_content_type


async def save_jpg_upload(file: Optional[UploadFile], prefix: str, label: str) -> Optional[str]:
    if not file or not file.filename:
        return None
    if not is_jpg_upload(file):
        raise HTTPException(status_code=400, detail=f"{label} must be a JPG file only.")
    saved = save_upload(file, prefix)
    if not saved:
        return None
    stored_path, public_path = saved
    content = await file.read()
    Path(stored_path).write_bytes(content)
    return public_path


def save_data_url(data_url: str, prefix: str) -> Optional[str]:
    if not data_url:
        return None
    match = re.match(r"^data:image/(png|jpeg|jpg|webp);base64,(.+)$", data_url)
    if not match:
        return None
    ext = "jpg" if match.group(1) in ["jpeg", "jpg"] else match.group(1)
    try:
        content = base64.b64decode(match.group(2), validate=True)
    except Exception:
        return None
    stored_name = f"{prefix}_{uuid.uuid4().hex[:8]}_camera.{ext}"
    stored_path = UPLOAD_DIR / stored_name
    stored_path.write_bytes(content)
    return f"/uploads/{stored_name}"


@app.get("/health")
def health():
    return {"status": "ok", **version_payload()}


@app.get("/api/version")
def version():
    return version_payload()


@app.get("/api/version-history")
def version_history():
    return {"history": VERSION_HISTORY}


@app.get("/api/master-data")
def master_data():
    return {
        "schemes": fetch_all("schemes"),
        "pass_types": fetch_all("pass_types"),
        "categories": fetch_all("categories"),
        "pass_rules": SCHEME_PASS_RULES,
        "pass_validity_rules": PASS_VALIDITY_RULES,
        "user_roles": USER_ROLES,
        "version": APP_VERSION,
        "release_info": version_payload(),
    }


@app.get("/api/scheme-pass-rules")
def scheme_pass_rules():
    return {"pass_rules": SCHEME_PASS_RULES, "pass_validity_rules": PASS_VALIDITY_RULES}


@app.get("/api/schemes")
def schemes():
    return fetch_all("schemes")


@app.get("/api/pass-types")
def pass_types():
    return fetch_all("pass_types")


@app.get("/api/categories")
def categories():
    return fetch_all("categories")


@app.post("/api/applications")
async def submit_application(
    data_json: str = Form(...),
    proof_file: Optional[UploadFile] = File(default=None),
    proof_front_file: Optional[UploadFile] = File(default=None),
    proof_back_file: Optional[UploadFile] = File(default=None),
    citizen_photo_file: Optional[UploadFile] = File(default=None),
):
    try:
        payload = json.loads(data_json)
    except json.JSONDecodeError as exc:
        raise HTTPException(status_code=400, detail="Invalid application JSON") from exc

    missing = [field for field in REQUIRED_FIELDS if not payload.get(field)]
    if missing:
        raise HTTPException(status_code=422, detail={"missing_fields": missing})

    now = datetime.utcnow()
    application_no = payload.get("application_no") or f"SHAKTI-{now.strftime('%Y%m%d')}-{uuid.uuid4().hex[:6].upper()}"
    proof_path = None
    proof_front_path = None
    proof_back_path = None
    citizen_photo_path = None

    if proof_file and proof_file.filename:
        # Backward compatibility for v1.0.6 and older packages that submitted one proof file.
        proof_path = await save_jpg_upload(proof_file, application_no, "Proof upload")
        proof_front_path = proof_path

    if proof_front_file and proof_front_file.filename:
        proof_front_path = await save_jpg_upload(proof_front_file, f"{application_no}_PROOF_FRONT", "Proof front page")

    if proof_back_file and proof_back_file.filename:
        proof_back_path = await save_jpg_upload(proof_back_file, f"{application_no}_PROOF_BACK", "Proof back page")

    if citizen_photo_file and citizen_photo_file.filename:
        saved = save_upload(citizen_photo_file, f"{application_no}_PHOTO")
        if saved:
            stored_path, citizen_photo_path = saved
            content = await citizen_photo_file.read()
            Path(stored_path).write_bytes(content)
    elif payload.get("citizen_photo_data_url"):
        citizen_photo_path = save_data_url(payload.get("citizen_photo_data_url"), f"{application_no}_PHOTO")

    allowed_fields = {
        "status", "scheme_code", "pass_type_code", "validity_type", "validity_start", "validity_end",
        "name_en", "name_kn", "age", "date_of_birth", "gender", "category_code", "category_other",
        "mobile", "email", "aadhaar_number", "aadhaar_name", "aadhaar_dob", "aadhaar_gender",
        "five_guarantee_application_no", "address_line_1", "address_line_2", "district", "taluk", "city", "pincode",
        "proof_type", "proof_reference_no", "institution_name", "employer_name", "route_preference",
        "service_preference", "consent_data_use", "consent_aadhaar_verification", "consent_terms", "remarks"
    }
    clean_payload = {key: payload.get(key) for key in allowed_fields if key in payload}
    clean_payload.update({
        "application_no": application_no,
        "created_at": now.isoformat(timespec="seconds") + "Z",
        "proof_file_path": proof_path or proof_front_path,
        "proof_front_file_path": proof_front_path,
        "proof_back_file_path": proof_back_path,
        "citizen_photo_path": citizen_photo_path,
        "status": payload.get("status") or "Submitted",
    })

    for consent_key in ["consent_data_use", "consent_aadhaar_verification", "consent_terms"]:
        clean_payload[consent_key] = 1 if clean_payload.get(consent_key) in [True, "true", "1", 1, "on"] else 0

    try:
        created = create_application(clean_payload)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Could not save application: {exc}") from exc
    return created


@app.get("/api/applications")
def applications(search: Optional[str] = None, status: Optional[str] = None):
    return list_applications(search=search, status=status)


@app.get("/api/applications/{app_id}")
def application_detail(app_id: int):
    record = get_application(app_id)
    if not record:
        raise HTTPException(status_code=404, detail="Application not found")
    return record


@app.get("/api/stats")
def application_stats():
    return stats()


@app.get("/api/users")
def users(search: Optional[str] = None):
    return list_users(search=search)


@app.post("/api/users")
def add_user(payload: dict):
    missing = [field for field in ["username", "full_name", "role", "password"] if not payload.get(field)]
    if missing:
        raise HTTPException(status_code=422, detail={"missing_fields": missing})
    try:
        return create_user(payload)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Could not create user: {exc}") from exc


@app.patch("/api/users/{user_id}")
def edit_user(user_id: int, payload: dict):
    updated = update_user(user_id, payload)
    if not updated:
        raise HTTPException(status_code=404, detail="User not found")
    return updated
