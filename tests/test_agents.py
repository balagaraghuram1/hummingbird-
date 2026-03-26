"""Tests for AI agents.

Tests the diagnosis, treatment, and lab agents.
"""

from __future__ import annotations

from unittest.mock import AsyncMock, patch

import pytest

from src.agents.diagnosis_agent import DiagnosisAgent
from src.agents.treatment_agent import TreatmentAgent
from src.agents.lab_agent import LabAgent


class TestDiagnosisAgent:
    """Tests for the diagnosis agent."""

    def test_agent_initializes(self) -> None:
        agent = DiagnosisAgent()
        assert agent is not None

    @pytest.mark.asyncio
    async def test_run_returns_diagnosis(self) -> None:
        agent = DiagnosisAgent()
        agent._initialized = True
        agent._chain = None

        result = await agent.run(["fever", "cough"])
        assert "diagnosis" in result
        assert "timestamp" in result
        assert "confidence" in result

    @pytest.mark.asyncio
    async def test_run_with_single_symptom(self) -> None:
        agent = DiagnosisAgent()
        agent._initialized = True
        agent._chain = None

        result = await agent.run(["headache"])
        assert result["diagnosis"] is not None


class TestTreatmentAgent:
    """Tests for the treatment agent."""

    def test_agent_initializes(self) -> None:
        agent = TreatmentAgent()
        assert agent is not None

    @pytest.mark.asyncio
    async def test_run_returns_treatment(self) -> None:
        agent = TreatmentAgent()
        agent._initialized = True
        agent._chain = None

        result = await agent.run("Common cold")
        assert "treatment_plan" in result
        assert "timestamp" in result


class TestLabAgent:
    """Tests for the lab agent."""

    def test_agent_initializes(self) -> None:
        agent = LabAgent()
        assert agent is not None

    @pytest.mark.asyncio
    async def test_run_returns_analysis(self) -> None:
        agent = LabAgent()
        agent._initialized = True
        agent._chain = None

        result = await agent.run({"hemoglobin": 14.2, "glucose": 95})
        assert "analysis" in result
        assert "abnormal_values" in result

    def test_check_references_normal(self) -> None:
        agent = LabAgent()
        abnormal = agent._check_references({"hemoglobin": 14.2})
        assert len(abnormal) == 0

    def test_check_references_abnormal(self) -> None:
        agent = LabAgent()
        abnormal = agent._check_references({"hemoglobin": 8.0})
        assert len(abnormal) == 1
        assert abnormal[0]["status"] == "low"

    def test_check_references_high(self) -> None:
        agent = LabAgent()
        abnormal = agent._check_references({"glucose": 200})
        assert len(abnormal) == 1
        assert abnormal[0]["status"] == "high"
# v30 - updated 2026-06-11
# v60 - updated 2026-06-11
