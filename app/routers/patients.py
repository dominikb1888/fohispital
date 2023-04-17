import os
import json

from fastapi import APIRouter, HTTPException

from fhir.resources.patient import Patient
from fhir.resources.fhirtypes import PatientType

from typing import Any
from pydantic import BaseModel, ValidationError

router = APIRouter()



def load_patients():
    patients = []
    for root, dirs, files in os.walk("./app/routers", topdown=False):
        for name in files:
             if name.endswith(".json"):
                 with open(os.path.join(root, name)) as f:
                     # Import as valid FHIR Resource
                     try:
                        print(f.name)
                        patient = Patient.parse_file(f.name)
                        print(" --- OK --- ")
                        patients.append(patient)
                     except ValidationError as e:
                        print(e)


    return patients


@router.get("/patients/", tags=["patients"], response_model=list[PatientType])
async def read_patients() -> Any:
    patients = load_patients()
    return patients

@router.get("/patients/{patient_id}", tags=["patients"], response_model=PatientType)
async def read_patient(patient_id: str)  -> Any:
    patients = load_patients()
    patient = [patient for patient in patients if patient_id == patient.id]
    if len(patient) != 1:
        raise HTTPException(status_code=404, detail="Item not found")

    return patient[0]

@router.post("/patients/", tags=["patients"], response_model=PatientType)
async def create_patient(patient: PatientType)  -> Any:
    with open(f"app/routers/fhir_resources/{patient.id}.json", 'x', encoding='utf-8') as f:
        json.dump(json.loads(patient.json()), f, ensure_ascii=False, indent=4)

    return patient
