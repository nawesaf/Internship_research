from backend.tests.unit.test_matching_service import test_calculate_total_score


def test_complete_matching_flow(
    client,
    cv_pdf_path,
    offer_pdf_path,
    monkeypatch,
):
    monkeypatch.setattr(
        "app.routers.matching.analyze_cv_offer",
        test_calculate_total_score,
    )

    with cv_pdf_path.open("rb") as cv_pdf:
        cv_response = client.post(
            "/api/uploads/cv",
            files={
                "cv_file": (
                    "cv.pdf",
                    cv_pdf,
                    "application/pdf",
                )
            },
        )

    assert cv_response.status_code == 200
    session_id = cv_response.json()["session_id"]

    with offer_pdf_path.open("rb") as offer_pdf:
        offer_response = client.post(
            f"/api/uploads/offer/{session_id}",
            files={
                "offer_file": (
                    "offer.pdf",
                    offer_pdf,
                    "application/pdf",
                )
            },
        )

    assert offer_response.status_code == 200

    match_response = client.post(
        f"/api/match/{session_id}"
    )

    assert match_response.status_code == 200

    data = match_response.json()

    assert data["score"] == 75
    assert data["matched_skills"] == [
        "Python",
        "FastAPI",
    ]
    assert data["missing_skills"] == ["Docker"]