from app.schemas.matching_schema import MatchingResult
from app.services.openrouter.openrouter_matching_service import analyze_cv_offer


async def calculate_matching_score(
    cv_text: str | None = None,
    offer_text: str | None = None,
) -> MatchingResult:
    if not cv_text or not offer_text:
        raise ValueError(
            "Le CV et l'offre ne peuvent pas être vides.",
        )

    try:
        return await analyze_cv_offer(
            cv_text=cv_text,
            offer_text=offer_text,
        )
    except ValueError:
        raise
    except RuntimeError:
        raise
    except Exception as error:
        raise RuntimeError(
            "L'analyse OpenRouter a échoué."
        ) from error