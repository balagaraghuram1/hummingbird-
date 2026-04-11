class DiagnosisAgent:
    def run(self, symptoms: list[str]) -> str:
        return f"Differential diagnosis for: {', '.join(symptoms)}"

