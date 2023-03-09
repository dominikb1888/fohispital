from typing import Any

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from . import crud, models, schemas
from .routers import patients
from .database import SessionLocal, engine

from fhir.resources import construct_fhir_element


models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


app.include_router(patients.router)


@app.get("/")
async def get_resources(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_resources(db)

@app.post("/")
async def add_resources(resource: dict, db:  Session = Depends(get_db)) -> Any:
    fhir_resource = construct_fhir_element(resource["resourceType"], resource)

    return crud.create_resource(db, fhir_resource)
