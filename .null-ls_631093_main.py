from fastapi import FastAPI
import os
import json

app = FastAPI()


@app.get("/")
async def root():

    files = os.listdir('fhir_resources')

    patients = []
    for filename in files:
        with open(f"fhir_resources/{filename}") as file:
            patients.append(json.load(file))

    return patients

@app.post("/patients/create"):
async def patient_create():
    pass

# Agenda:

# 1. Play with the data locally. Access it, use it, filter it, display
# 2. Adapt our server to send and accept valid JSON FHIR data
