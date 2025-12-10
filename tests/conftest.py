"""Pytest configuration and fixtures.

Provides shared test fixtures for the test suite.
"""

from __future__ import annotations

import pytest
from fastapi.testclient import TestClient

from src.main import app


@pytest.fixture
def client() -> TestClient:
    """Create a test client for the FastAPI application.

    Returns:
        TestClient instance for making HTTP requests.
    """
    return TestClient(app)


@pytest.fixture
def sample_symptoms() -> list[str]:
    """Provide sample symptoms for testing.

    Returns:
        List of common symptom strings.
    """
    return ["fever", "cough", "fatigue", "headache"]


@pytest.fixture
def sample_diagnosis() -> str:
    """Provide a sample diagnosis for testing.

    Returns:
        Sample diagnosis string.
    """
    return "Upper respiratory infection, likely viral etiology"


@pytest.fixture
def sample_lab_results() -> dict[str, float]:
    """Provide sample lab results for testing.

    Returns:
        Dictionary of test names to values.
    """
    return {
        "hemoglobin": 14.2,
        "white_blood_cells": 7.5,
        "platelets": 250,
        "glucose": 95,
        "creatinine": 0.9,
    }
