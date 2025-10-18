"""
Module serves as a wrapper over patient_repo.

We can extra business logic, or redis caching logic etc in here
mostly needed for update and search part
"""

from sqlalchemy.ext.asyncio import AsyncSession

from src.database.models import Patient
from src.repo import patient_repo
from src.schemas.patient_schema import PatientCreate, PatientUpdate


async def create_patient(db: AsyncSession, patient: PatientCreate) -> Patient:
    return await patient_repo.create_patient(db, patient)


async def get_patient(db: AsyncSession, patient_id: int) -> Patient:
    return await patient_repo.get_patient(db, patient_id)


async def list_patients(
    db: AsyncSession, limit: int = 100, offset: int = 0
) -> list[Patient]:
    return await patient_repo.list_patients(db, limit, offset)


async def update_patient(
    db: AsyncSession, patient_id: int, patient: PatientUpdate
) -> Patient:
    """
    Update Patient

    We remove attributes that are not set, incase user didn't pass those in json
    This avoids setting null values for not passed fields.
    """
    if patient.age is None:
        delattr(patient, "age")

    if patient.name is None:
        delattr(patient, "name")

    return await patient_repo.update_patient(db, patient_id, patient)


async def delete_patient(db: AsyncSession, patient_id: int) -> Patient:
    return await patient_repo.delete_patient(db, patient_id)
