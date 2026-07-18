import os
import uuid
from fastapi import APIRouter, UploadFile, File

router = APIRouter()

UPLOAD_DIR = "./uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/upload")
async def upload_files(
    cv_file: UploadFile = File(...),
    offer_file: UploadFile = File(...),
):
    session_id = str(uuid.uuid4())

    cv_path = f"{UPLOAD_DIR}/{session_id}_cv_{cv_file.filename}"
    offer_path = f"{UPLOAD_DIR}/{session_id}_offer_{offer_file.filename}"

    with open(cv_path, "wb") as f:
        f.write(await cv_file.read())

    with open(offer_path, "wb") as f:
        f.write(await offer_file.read())

    return {
        "session_id": session_id,
        "cv_path": cv_path,
        "offer_path": offer_path,
    }