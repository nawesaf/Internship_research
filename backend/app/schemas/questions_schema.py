from typing import Literal

from pydantic import BaseModel, Field

from app.schemas.matching_schema import MatchingResult


class ChatMessage(BaseModel):
    role: Literal["user", "assistant"]
    content: str


class AnalysisSession(BaseModel):
    analysis_id: str
    cv_text: str
    offer_text: str
    matching_result: MatchingResult

    messages: list[ChatMessage] = Field(default_factory=list)