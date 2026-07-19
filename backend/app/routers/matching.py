from pathlib import Path

from app.schemas.matching_schema import MatchingResult
from fastapi import APIRouter, HTTPException

from app.services.matching_service import calculate_matching_score
from app.services.pdf_extractor import extract_pdf_text

router = APIRouter()

UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

@router.post(
    "/{session_id}",
    response_model=MatchingResult,
)
async def match_cv_with_offer(session_id: str):
    session_directory = UPLOAD_DIR / session_id

    cv_path = session_directory / "cv.pdf"
    offer_path = session_directory / "offer.pdf"

    if not cv_path.exists():
        raise HTTPException(
            status_code=404,
            detail="CV introuvable.",
        )

    if not offer_path.exists():
        raise HTTPException(
            status_code=404,
            detail="Offre introuvable.",
        )

    cv_text = extract_pdf_text(cv_path.read_bytes())
    offer_text = extract_pdf_text(offer_path.read_bytes())

    score = calculate_matching_score(
        cv_text=cv_text,
        offer_text=offer_text,
    )

    return {
        "session_id": session_id,
        "score": score,
    }