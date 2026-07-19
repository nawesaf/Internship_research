def test_upload_cv(client, cv_pdf_path):
    with cv_pdf_path.open("rb") as pdf:
        response = client.post(
            "/api/uploads/cv",
            files={
                "cv_file": (
                    "cv_test.pdf",
                    pdf,
                    "application/pdf",
                )
            },
        )

    assert response.status_code == 200

    data = response.json()

    assert "session_id" in data
    assert data["filename"] == "cv_test.pdf"


def test_upload_cv_rejects_text_file(client):
    response = client.post(
        "/api/uploads/cv",
        files={
            "cv_file": (
                "cv.txt",
                b"Ce fichier n'est pas un PDF.",
                "text/plain",
            )
        },
    )

    assert response.status_code == 415


def test_upload_offer_rejects_unknown_session(
    client,
    offer_pdf_path,
):
    with offer_pdf_path.open("rb") as pdf:
        response = client.post(
            "/api/uploads/offer/session-inexistante",
            files={
                "offer_file": (
                    "offer_test.pdf",
                    pdf,
                    "application/pdf",
                )
            },
        )

    assert response.status_code == 404
    assert response.json() == {
        "detail": "Session introuvable."
    }