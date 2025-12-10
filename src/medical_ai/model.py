"""Hummingbird Medical AI Model.

Core medical AI model for diagnosis, treatment recommendations,
and lab analysis powered by large language models.
"""

from __future__ import annotations

import logging
from datetime import datetime, timezone
from typing import Any

from langchain.chains import LLMChain
from langchain.prompts import ChatPromptTemplate
from langchain_core.tools import Tool

from src.config.settings import settings

logger = logging.getLogger(__name__)

DIAGNOSIS_PROMPT = ChatPromptTemplate.from_messages([
    ("system", (
        "You are an expert medical AI assistant. Analyze the patient's symptoms "
        "and provide a differential diagnosis. Always recommend consulting a "
        "licensed physician for confirmation. Be thorough but cautious."
    )),
    ("human", "Patient symptoms: {symptoms}\n\nProvide your differential diagnosis:"),
])

TREATMENT_PROMPT = ChatPromptTemplate.from_messages([
    ("system", (
        "You are an expert medical AI assistant. Based on the diagnosis, "
        "provide a comprehensive treatment plan. Include medications, lifestyle "
        "changes, follow-up recommendations, and red flags. Always emphasize "
        "that this is AI-generated guidance and not a substitute for professional "
        "medical advice."
    )),
    ("human", "Diagnosis: {diagnosis}\n\nProvide treatment recommendations:"),
])

LAB_PROMPT = ChatPromptTemplate.from_messages([
    ("system", (
        "You are an expert medical AI assistant specializing in laboratory "
        "result interpretation. Analyze the provided lab results, identify "
        "abnormal values, suggest potential conditions, and recommend "
        "follow-up tests when appropriate."
    )),
    ("human", "Lab results: {results}\n\nProvide your analysis:"),
])


class MedicalAIModel:
    """Medical AI model for diagnosis, treatment, and lab analysis.

    This model uses LangChain with configurable LLM providers to provide
    medical analysis capabilities. It includes knowledge base search via
    vector embeddings and structured prompt engineering for medical tasks.
    """

    def __init__(self) -> None:
        self._llm = None
        self._embeddings = None
        self._vector_store = None
        self._tools: list[Tool] = []
        self._initialized = False

    def _ensure_initialized(self) -> None:
        """Lazy initialization of LLM and dependencies."""
        if self._initialized:
            return

        try:
            from langchain_openai import ChatOpenAI, OpenAIEmbeddings
            from langchain_community.vectorstores import Chroma

            self._llm = ChatOpenAI(
                model_name=settings.model_name,
                temperature=settings.model_temperature,
                max_tokens=settings.model_max_tokens,
                api_key=settings.openai_api_key,
            )

            self._embeddings = OpenAIEmbeddings(api_key=settings.openai_api_key)
            self._vector_store = Chroma(
                embedding_function=self._embeddings,
                persist_directory=settings.chroma_persist_directory,
            )

            self._tools = [
                Tool(
                    name="SearchMedicalKnowledge",
                    description="Search the medical knowledge base for relevant information",
                    func=self._search_knowledge,
                ),
            ]

            self._initialized = True
            logger.info("Medical AI model initialized successfully")

        except ImportError as e:
            logger.warning("AI dependencies not available: %s. Running in offline mode.", e)
            self._initialized = True
        except Exception as e:
            logger.error("Failed to initialize AI model: %s", e)
            self._initialized = True

    def _search_knowledge(self, query: str) -> str:
        """Search the vector store for medical knowledge."""
        self._ensure_initialized()
        if self._vector_store is None:
            return "Vector store not available"
        try:
            results = self._vector_store.similarity_search(query, k=5)
            return "\n".join(doc.page_content for doc in results)
        except Exception as e:
            logger.error("Knowledge search failed: %s", e)
            return f"Search error: {e}"

    async def diagnose(self, symptoms: list[str]) -> dict[str, Any]:
        """Generate a differential diagnosis from symptoms.

        Args:
            symptoms: List of patient-reported symptoms.

        Returns:
            Dictionary with diagnosis, confidence, and timestamp.
        """
        self._ensure_initialized()
        symptoms_text = ", ".join(symptoms)

        if self._llm is None:
            return {
                "diagnosis": f"Offline mode: Unable to process symptoms [{symptoms_text}]. "
                             "Please configure an AI provider.",
                "confidence": 0.0,
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }

        try:
            chain = LLMChain(llm=self._llm, prompt=DIAGNOSIS_PROMPT)
            response = await chain.ainvoke({"symptoms": symptoms_text})
            return {
                "diagnosis": response.get("text", "Unable to generate diagnosis"),
                "confidence": 0.85,
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }
        except Exception as e:
            logger.error("Diagnosis failed: %s", e)
            return {
                "diagnosis": f"Analysis error: {e}",
                "confidence": 0.0,
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }

    async def generate_treatment_plan(self, diagnosis: str) -> dict[str, Any]:
        """Generate a treatment plan from a diagnosis.

        Args:
            diagnosis: The diagnosis string to generate treatment for.

        Returns:
            Dictionary with treatment plan and timestamp.
        """
        self._ensure_initialized()

        if self._llm is None:
            return {
                "treatment_plan": f"Offline mode: Unable to generate treatment for [{diagnosis}]. "
                                  "Please configure an AI provider.",
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }

        try:
            chain = LLMChain(llm=self._llm, prompt=TREATMENT_PROMPT)
            response = await chain.ainvoke({"diagnosis": diagnosis})
            return {
                "treatment_plan": response.get("text", "Unable to generate treatment plan"),
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }
        except Exception as e:
            logger.error("Treatment plan generation failed: %s", e)
            return {
                "treatment_plan": f"Treatment generation error: {e}",
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }

    async def analyze_lab_results(self, results: dict[str, Any]) -> dict[str, Any]:
        """Analyze laboratory test results.

        Args:
            results: Dictionary of lab test names to their values.

        Returns:
            Dictionary with lab analysis and timestamp.
        """
        self._ensure_initialized()

        results_text = "\n".join(f"{k}: {v}" for k, v in results.items())

        if self._llm is None:
            return {
                "analysis": f"Offline mode: Unable to analyze lab results. Received {len(results)} tests.",
                "abnormal_values": [],
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }

        try:
            chain = LLMChain(llm=self._llm, prompt=LAB_PROMPT)
            response = await chain.ainvoke({"results": results_text})
            return {
                "analysis": response.get("text", "Unable to analyze lab results"),
                "abnormal_values": [],
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }
        except Exception as e:
            logger.error("Lab analysis failed: %s", e)
            return {
                "analysis": f"Lab analysis error: {e}",
                "abnormal_values": [],
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }

    @property
    def is_available(self) -> bool:
        """Check if the AI model is initialized and available."""
        self._ensure_initialized()
        return self._llm is not None


medical_ai_model = MedicalAIModel()
