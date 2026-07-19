from app.schemas.matching_schema import (
    MatchingBreakdown,
    MatchingResult,
)


async def fake_analyze_cv_offer(
    cv_text: str,
    offer_text: str,
) -> MatchingResult:
    return MatchingResult(
        score=75,
        breakdown=MatchingBreakdown(
            technical_skills=30,
            relevant_experience=20,
            projects=10,
            education=8,
            constraints=7,
        ),
        matched_skills=["Python", "FastAPI"],
        missing_skills=["Docker"],
        explanation="Résultat simulé pour le test.",
    )


def test_matching_unknown_session(client):
    response = client.post(
        "/api/match/session-inexistante"
    )

    assert response.status_code == 404