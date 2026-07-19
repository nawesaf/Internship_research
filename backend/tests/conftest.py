from collections.abc import Generator
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from app.main import app


@pytest.fixture
def client() -> Generator[TestClient, None, None]:
    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture
def cv_pdf_path() -> Path:
    return Path("tests/files/cv_test.pdf")


@pytest.fixture
def offer_pdf_path() -> Path:
    return Path("tests/files/offer_test.pdf")