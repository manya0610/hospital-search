from fastapi import FastAPI

from src.app.routers.note_router import note_router
from src.app.routers.patient_router import patient_router

app = FastAPI()

app.include_router(note_router)
app.include_router(patient_router)
