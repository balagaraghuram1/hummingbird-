from src.agents.diagnosis_agent import DiagnosisAgent


def test_diagnosis_agent() -> None:
    output = DiagnosisAgent().run(["fever", "cough"])
    assert "fever" in output

