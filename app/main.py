from fastapi import FastAPI
from app.routers import patients

app = FastAPI()
app.include_router(patients.router)


@app.get("/")
async def root():
    return {"message": "Hello World"}
