from fastapi import FastAPI
import os
import json
import sys

app = FastAPI()


@app.get("/")
async def root():

    files = os.listdir('fhir_resources')

    patients = []
    for filename in files:
        with open(f"fhir_resources/{filename}") as file:
            patients.append(json.load(file))

    return patients

@app.post("/patients/create")
async def patient_create(jsonData):
    # How to secure our open "post box"?
    # Check for valid json
    print(jsonData, file=sys.stderr)
    try:
        patient = json.load(jsonData)
    except ValueError as err:
        return False

    # TODO: Check header for the right Content-Type: application/json+fhir

    file_id = len(os.listdir('fhir_resources')) + 1
    filename = f"patient_{file_id}.json"

    with open(filename, 'w') as file:
        json.dump(patient, file)

    return 'OK'


# Agenda:

# 1. Play with the data locally. Access it, use it, filter it, display
# 2. Adapt our server to send and accept valid JSON FHIR data
