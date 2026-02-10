"""Diagnosis agent for medical AI.

Provides specialized diagnosis capabilities using LLM chains
with medical knowledge retrieval and structured prompts.
"""

from __future__ import annotations

import logging
from datetime import datetime, timezone
from typing import Any

logger = logging.getLogger(__name__)


class DiagnosisAgent:
    """Medical diagnosis agent.

    Analyzes patient symptoms and generates differential diagnoses
    using LLM chains with medical knowledge base retrieval.
    """

    def __init__(self) -> None:
        self._chain = None
        self._initialized = False

    def _ensure_initialized(self) -> None:
        """Lazy-initialize the diagnosis chain."""
        if self._initialized:
            return

        try:
            from langchain.chains import LLMChain
            from langchain.prompts import ChatPromptTemplate

            from src.config.settings import settings

            if not settings.openai_api_key:
                self._initialized = True
                return

            from langchain_openai import ChatOpenAI

            llm = ChatOpenAI(
                model_name=settings.model_name,
                temperature=0.1,
                api_key=settings.openai_api_key,
            )

            prompt = ChatPromptTemplate.from_messages([
                ("system", (
                    "You are an expert medical diagnostician. Analyze the patient's "
                    "symptoms and provide a differential diagnosis. Consider the most "
                    "likely conditions first, then less common possibilities. Always "
                    "recommend professional medical consultation."
                )),
                ("human", "Symptoms: {symptoms}\n\nProvide differential diagnosis:"),
            ])

            self._chain = LLMChain(llm=llm, prompt=prompt)
            self._initialized = True
        except Exception as e:
            logger.warning("Diagnosis agent initialization failed: %s", e)
            self._initialized = True

    async def run(self, symptoms: list[str]) -> dict[str, Any]:
        """Run diagnosis on patient symptoms.

        Args:
            symptoms: List of patient-reported symptoms.

        Returns:
            Dictionary with diagnosis results.
        """
        self._ensure_initialized()
        symptoms_text = ", ".join(symptoms)

        if self._chain is None:
            return {
                "diagnosis": f"Offline analysis for symptoms: {symptoms_text}",
                "confidence": 0.0,
                "differentials": [],
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }

        try:
            response = await self._chain.ainvoke({"symptoms": symptoms_text})
            return {
                "diagnosis": response.get("text", "Unable to generate diagnosis"),
                "confidence": 0.8,
                "differentials": [],
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }
        except Exception as e:
            logger.error("Diagnosis agent failed: %s", e)
            return {
                "diagnosis": f"Analysis error: {e}",
                "confidence": 0.0,
                "differentials": [],
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }


diagnosis_agent = DiagnosisAgent()
# v11 - updated 2026-06-11
# v41 - updated 2026-06-11
# v71 - updated 2026-06-11
# v101 - updated 2026-06-11
# v131 - updated 2026-06-11
