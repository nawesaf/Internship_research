from app.services.pdf_extractor import extract_pdf_text


def test_extract_pdf_text(cv_pdf_path):
    content = cv_pdf_path.read_bytes()

    text = extract_pdf_text(content)

    assert isinstance(text, str)
    assert text.strip()
    assert "Python" in text