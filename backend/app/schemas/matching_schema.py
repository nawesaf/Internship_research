from pydantic import BaseModel, ConfigDict, Field


class MatchingBreakdown(BaseModel):
    model_config = ConfigDict(extra="forbid")

    technical_skills: int = Field(ge=0, le=40)
    relevant_experience: int = Field(ge=0, le=25)
    projects: int = Field(ge=0, le=15)
    education: int = Field(ge=0, le=10)
    constraints: int = Field(ge=0, le=10)


class LLMMatchingAnalysis(BaseModel):
    model_config = ConfigDict(extra="forbid")

    breakdown: MatchingBreakdown
    matched_skills: list[str]
    missing_skills: list[str]
    explanation: str


class MatchingResult(LLMMatchingAnalysis):
    score: int = Field(ge=0, le=100)