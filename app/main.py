from fastapi import FastAPI
from app.routers import patients

from fhir.resources import construct_fhir_element

from typing import Any

app = FastAPI()
app.include_router(patients.router)


@app.get("/")
async def root():
    return {"message": "POST any FHIR resource to test if it is valid and store it here"}

@app.post("/")
async def fhir_dump(resource: dict) -> Any:
    result = construct_fhir_element(resource["resourceType"], resource)

    return result
