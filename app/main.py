from fastapi import FastAPI
from app.routers import patients
from app.routers import related_persons

app = FastAPI()

app.include_router(patients.router)
app.include_router(related_persons.router)


@app.get("/")
async def root():
    return {"message": "Hello World"}
