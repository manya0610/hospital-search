import asyncio
import json
import os

from src.database import get_db
from src.schemas.note_schema import NoteCreate
from src.schemas.patient_schema import PatientCreate
from src.services import note_service, patient_service

with open("./dummy_data.json", "r") as f:
    data = json.load(f)


async def seed_db():
    print("seeding database")
    for patient in data["patients"]:
        async for db in get_db():
            await patient_service.create_patient(db, PatientCreate(**patient))

    for notes in data["notes"]:
        async for db in get_db():
            await note_service.create_note(db, NoteCreate(**notes))
    
    print("seeding finished")


if __name__ == "__main__":
    DB_URL = os.getenv("DATABASE_URL")
    asyncio.run(seed_db())