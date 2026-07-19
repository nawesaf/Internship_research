from io import BytesIO

from pypdf import PdfReader


def extract_pdf_text(file_content: bytes) -> str:
    pdf_stream = BytesIO(file_content)
    reader = PdfReader(pdf_stream)

    pages_text = [
        page.extract_text() or ""
        for page in reader.pages
    ]

    text = "\n".join(pages_text).strip()

    if not text:
        raise ValueError(
            "Aucun texte n'a pu être extrait du PDF."
        )

    return text