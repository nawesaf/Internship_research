from app.schemas.matching_schema import (
    LLMMatchingAnalysis,
    MatchingBreakdown,
)
from app.services.openrouter_matching_service import (
    calculate_total_score,
)


def test_calculate_total_score():
    analysis = LLMMatchingAnalysis(
        breakdown=MatchingBreakdown(
            technical_skills=30,
            relevant_experience=20,
            projects=10,
            education=8,
            constraints=7,
        ),
        matched_skills=["Python", "FastAPI"],
        missing_skills=["Docker"],
        explanation="Correspondance correcte.",
    )

    score = calculate_total_score(analysis)

    assert score == 75