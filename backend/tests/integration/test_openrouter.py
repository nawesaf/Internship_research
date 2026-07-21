import os

import pytest

from app.services.openrouter.openrouter_matching_service import (
    analyze_cv_offer,
)


@pytest.mark.integration
@pytest.mark.anyio
async def test_real_openrouter_analysis():
    if not os.getenv("OPENROUTER_API_KEY"):
        pytest.skip("OPENROUTER_API_KEY absente")

    result = await analyze_cv_offer(
        cv_text="""
        Étudiant ingénieur.
        Compétences : Python, FastAPI et scikit-learn.
        """,
        offer_text="""
        Recherche stagiaire Python connaissant FastAPI.
        Docker est apprécié.
        """,
    )

    assert 0 <= result.score <= 100
    assert result.explanation