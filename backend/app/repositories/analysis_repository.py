from uuid import uuid4

from app.schemas.analysis_schema import AnalysisSession, ChatMessage
from app.schemas.matching_schema import MatchingResult


# Stockage temporaire en RAM.
_analyses: dict[str, AnalysisSession] = {}


def create_analysis_session(
    cv_text: str,
    offer_text: str,
    matching_result: MatchingResult,
) -> AnalysisSession:
    analysis_id = str(uuid4())

    session = AnalysisSession(
        analysis_id=analysis_id,
        cv_text=cv_text,
        offer_text=offer_text,
        matching_result=matching_result,
    )

    _analyses[analysis_id] = session

    return session


def get_analysis_session(
    analysis_id: str,
) -> AnalysisSession | None:
    return _analyses.get(analysis_id)


def add_message(
    analysis_id: str,
    message: ChatMessage,
) -> None:
    session = get_analysis_session(analysis_id)

    if session is None:
        raise ValueError("Analyse introuvable")

    session.messages.append(message)