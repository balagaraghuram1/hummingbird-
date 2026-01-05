"""Treatment agent for medical AI.

Generates personalized treatment plans based on diagnoses
using LLM chains with medical guidelines.
"""

from __future__ import annotations

import logging
from datetime import datetime, timezone
from typing import Any

logger = logging.getLogger(__name__)


class TreatmentAgent:
    """Medical treatment plan agent.

    Generates comprehensive treatment plans based on diagnoses,
    including medications, lifestyle changes, and follow-up.
    """

    def __init__(self) -> None:
        self._chain = None
        self._initialized = False

    def _ensure_initialized(self) -> None:
        """Lazy-initialize the treatment chain."""
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
                temperature=0.2,
                api_key=settings.openai_api_key,
            )

            prompt = ChatPromptTemplate.from_messages([
                ("system", (
                    "You are an expert medical treatment planner. Based on the "
                    "diagnosis, provide a comprehensive treatment plan including: "
                    "1) Medications with dosages, 2) Lifestyle modifications, "
                    "3) Follow-up schedule, 4) Red flags to watch for. "
                    "Always emphasize this is AI guidance, not medical advice."
                )),
                ("human", "Diagnosis: {diagnosis}\n\nProvide treatment plan:"),
            ])

            self._chain = LLMChain(llm=llm, prompt=prompt)
            self._initialized = True
        except Exception as e:
            logger.warning("Treatment agent initialization failed: %s", e)
            self._initialized = True

    async def run(self, diagnosis: str) -> dict[str, Any]:
        """Generate treatment plan for a diagnosis.

        Args:
            diagnosis: Medical diagnosis string.

        Returns:
            Dictionary with treatment recommendations.
        """
        self._ensure_initialized()

        if self._chain is None:
            return {
                "treatment_plan": f"General guidance for: {diagnosis}",
                "medications": [],
                "lifestyle_changes": [],
                "follow_up": "Consult your healthcare provider",
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }

        try:
            response = await self._chain.ainvoke({"diagnosis": diagnosis})
            return {
                "treatment_plan": response.get("text", "Unable to generate treatment plan"),
                "medications": [],
                "lifestyle_changes": [],
                "follow_up": "Follow up with your healthcare provider",
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }
        except Exception as e:
            logger.error("Treatment agent failed: %s", e)
            return {
                "treatment_plan": f"Treatment generation error: {e}",
                "medications": [],
                "lifestyle_changes": [],
                "follow_up": "Consult your healthcare provider",
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }


treatment_agent = TreatmentAgent()
# v12 - updated 2026-06-11
