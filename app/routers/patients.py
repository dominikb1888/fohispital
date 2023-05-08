import os
import json

from fastapi import APIRouter, HTTPException

from fhir.resources.patient import Patient
from fhir.resources.fhirtypes import PatientType

from typing import Any
from pydantic import BaseModel, ValidationError
from database import r

router = APIRouter()

def load_patients():
    patient_ids = r.keys('patient*')
    return [patient.decode() for patient in r.mget(patient_ids)]

# READ
@router.get("/patients/", tags=["patients"], response_model=list[PatientType])
async def read_patients() -> Any:
    patients = load_patients()
    return patients

@router.get("/patients/{patient_id}", tags=["patients"], response_model=PatientType)
async def read_patient(patient_id: str)  -> Any:
    key = f"patient:{patient_id}"
    patient = r.get(key)
    if patient is None:
        raise HTTPException(status_code=404, detail="Item not found")
    else:
        return patient.decode()

# CREATE
@router.post("/patients/", tags=["patients"], response_model=PatientType)
async def create_patient(patient: PatientType)  -> Any:
    # TODO: Autocreate unique id
    unique_id = 1249934 #r.execute_command('UUID')
    patient.id = unique_id # does this data conform to FHIR?
    redis_key = f"patient:{unique_id}"
    r.set(redis_key, patient)
    return patient

# UPDATE

# DELETE
