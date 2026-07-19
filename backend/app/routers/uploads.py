import uuid
from pathlib import Path

from fastapi import APIRouter, File, HTTPException, UploadFile

router = APIRouter()

UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)


@router.post("/cv")
async def upload_cv(
    cv_file: UploadFile = File(...),
):
    if cv_file.content_type != "application/pdf":
        raise HTTPException(
            status_code=415,
            detail="Le CV doit être un fichier PDF.",
        )

    session_id = str(uuid.uuid4())

    session_directory = UPLOAD_DIR / session_id
    session_directory.mkdir()

    cv_path = session_directory / "cv.pdf"

    content = await cv_file.read()
    cv_path.write_bytes(content)

    await cv_file.close()
    # pour l'instant, les fichiers sont stockés dans le dossier uploads, 
    # mais on pourrait envisager de les stocker dans un stockage cloud ou une 
    # base de données à l'avenir.

    return {
        "session_id": session_id,
        "filename": cv_file.filename,
    }


@router.post("/offer/{session_id}")
async def upload_offer(
    session_id: str,
    offer_file: UploadFile = File(...),
):
    if offer_file.content_type != "application/pdf":
        raise HTTPException(
            status_code=415,
            detail="L'offre doit être un fichier PDF.",
        )

    session_directory = UPLOAD_DIR / session_id

    if not session_directory.exists():
        raise HTTPException(
            status_code=404,
            detail="Session introuvable.",
        )

    offer_path = session_directory / "offer.pdf"

    content = await offer_file.read()
    offer_path.write_bytes(content)

    await offer_file.close()

    return {
        "session_id": session_id,
        "filename": offer_file.filename,
    }