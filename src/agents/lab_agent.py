"""Lab analysis agent for medical AI.

Interprets laboratory test results and identifies
abnormal values with clinical significance.
"""

from __future__ import annotations

import logging
from datetime import datetime, timezone
from typing import Any

logger = logging.getLogger(__name__)

REFERENCE_RANGES = {
    "hemoglobin": {"male": (13.5, 17.5), "female": (12.0, 16.0), "unit": "g/dL"},
    "white_blood_cells": {"range": (4.5, 11.0), "unit": "K/uL"},
    "platelets": {"range": (150, 400), "unit": "K/uL"},
    "glucose": {"range": (70, 100), "unit": "mg/dL"},
    "creatinine": {"range": (0.6, 1.2), "unit": "mg/dL"},
    "cholesterol_total": {"range": (0, 200), "unit": "mg/dL"},
    "ldl": {"range": (0, 100), "unit": "mg/dL"},
    "hdl": {"range": (40, 60), "unit": "mg/dL"},
    "triglycerides": {"range": (0, 150), "unit": "mg/dL"},
    "tsh": {"range": (0.4, 4.0), "unit": "mIU/L"},
    "hemoglobin_a1c": {"range": (4.0, 5.7), "unit": "%"},
}


class LabAgent:
    """Laboratory results analysis agent.

    Interprets lab results, identifies abnormal values,
    and provides clinical significance assessments.
    """

    def __init__(self) -> None:
        self._chain = None
        self._initialized = False

    def _ensure_initialized(self) -> None:
        """Lazy-initialize the lab analysis chain."""
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
                    "You are an expert clinical laboratory scientist. Analyze the "
                    "lab results, identify abnormal values, assess clinical significance, "
                    "and recommend follow-up tests if needed. Be precise and evidence-based."
                )),
                ("human", "Lab results:\n{results}\n\nProvide analysis:"),
            ])

            self._chain = LLMChain(llm=llm, prompt=prompt)
            self._initialized = True
        except Exception as e:
            logger.warning("Lab agent initialization failed: %s", e)
            self._initialized = True

    def _check_references(self, results: dict[str, Any]) -> list[dict[str, Any]]:
        """Check lab values against reference ranges.

        Args:
            results: Dictionary of test names to values.

        Returns:
            List of abnormal values with details.
        """
        abnormal = []
        for test_name, value in results.items():
            if not isinstance(value, (int, float)):
                continue

            ref = REFERENCE_RANGES.get(test_name.lower())
            if ref is None:
                continue

            if "range" in ref:
                low, high = ref["range"]
            elif "male" in ref and "female" in ref:
                low, high = ref["male"]
            else:
                continue

            if value < low or value > high:
                status = "low" if value < low else "high"
                abnormal.append({
                    "test": test_name,
                    "value": value,
                    "reference_range": f"{low}-{high} {ref.get('unit', '')}",
                    "status": status,
                })

        return abnormal

    async def run(self, results: dict[str, Any]) -> dict[str, Any]:
        """Analyze laboratory test results.

        Args:
            results: Dictionary of test names to values.

        Returns:
            Dictionary with analysis and abnormal values.
        """
        self._ensure_initialized()
        abnormal = self._check_references(results)

        if self._chain is None:
            analysis_parts = []
            if abnormal:
                analysis_parts.append(f"Found {len(abnormal)} abnormal values:")
                for a in abnormal:
                    analysis_parts.append(
                        f"  - {a['test']}: {a['value']} ({a['status']}, "
                        f"ref: {a['reference_range']})"
                    )
            else:
                analysis_parts.append("All values within reference ranges.")

            return {
                "analysis": "\n".join(analysis_parts),
                "abnormal_values": abnormal,
                "total_tests": len(results),
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }

        try:
            results_text = "\n".join(f"{k}: {v}" for k, v in results.items())
            response = await self._chain.ainvoke({"results": results_text})
            return {
                "analysis": response.get("text", "Unable to analyze results"),
                "abnormal_values": abnormal,
                "total_tests": len(results),
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }
        except Exception as e:
            logger.error("Lab agent failed: %s", e)
            return {
                "analysis": f"Analysis error: {e}",
                "abnormal_values": abnormal,
                "total_tests": len(results),
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }


lab_agent = LabAgent()
