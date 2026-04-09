from fastapi import FastAPI

app = FastAPI()

@app.get("/diagnose/{symptom}")
async def diagnose(symptom: str):
    return {"diagnosis": "Sample diagnosis for " + symptom}

@app.get("/treat/{diagnosis}")
async def treat(diagnosis: str):
    return {"treatment": "Sample treatment for " + diagnosis}

# Add more medical endpoints as needed
