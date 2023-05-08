import os
import json

from fastapi import APIRouter, HTTPException

from fhir.resources.related_person import RelatedPerson
from fhir.resources.fhirtypes import RelatedPersonType

from typing import Any
from pydantic import BaseModel, ValidationError
from database import r

router = APIRouter()

def load_related_person():
    related_person_ids = r.keys('related_person*')
    return [patient.decode() for patient in r.mget(related_person_ids)]

# READ
@router.get("/related_person/", tags=["related_person"], response_model=list[RelatedPersonType])
async def read_related_persons() -> Any:
    related_persons = load_related_persons()
    return related_persons

@router.get("/related_persons/{patient_id}", tags=["related_persons"], response_model=RelatedPersonType)
async def read_related_persons(related_person_id: str)  -> Any:
    key = f"patient:{related_person_id}"
    related_person = r.get(key)
    if related_person is None:
        raise HTTPException(status_code=404, detail="Item not found")
    else:
        return related_person.decode()

# CREATE
@router.post("/related_persons/", tags=["related_persons"], response_model=RelatedPersonType)
async def create_related_person(patient: RelatedPersonType)  -> Any:
    # TODO: Autocreate unique id
    unique_id = 1249935 #r.execute_command('UUID')
    related_person.id = unique_id # does this data conform to FHIR?
    redis_key = f"related_person:{unique_id}"
    r.set(redis_key, related_person)
    return related_person

# UPDATE

# DELETE
