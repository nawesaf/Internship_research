from fastapi import APIRouter, HTTPException

router = APIRouter(prefix="/analyses", tags=["questions"])


@router.post(
    "/{session_id}/questions",
    response_model=QuestionResponse,
)
async def ask_question(
    session_id: str,
    request: QuestionRequest,
) -> QuestionResponse:
    analysis = analysis_repository.get(session_id)

    if analysis is None:
        raise HTTPException(
            status_code=404,
            detail="Analyse introuvable",
        )

    answer = await answer_question(
        cv_text=analysis.cv_text,
        offer_text=analysis.offer_text,
        matching_analysis=analysis.result.model_dump_json(),
        question=request.question,
    )

    return QuestionResponse(answer=answer)