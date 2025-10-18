from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_db
from src.database.models import Patient
from src.exceptions.db_exceptions import NotFoundError
from src.schemas.patient_schema import PatientCreate, PatientPublic, PatientUpdate
from src.services import patient_service

patient_router = APIRouter(prefix="/patient")


@patient_router.post("")
async def create_patient(
    patient: PatientCreate,
    db: AsyncSession = Depends(get_db),
) -> PatientPublic:
    try:
        patient: Patient = await patient_service.create_patient(db, patient)
        return PatientPublic(**patient.__dict__)
    except Exception as e:
        raise HTTPException(status_code=500) from e


@patient_router.get("")
async def list_patients(
    db: AsyncSession = Depends(get_db),
    limit: Annotated[int, Query(le=100)] = 100,
    offset: int = 0,
) -> list[PatientPublic]:
    try:
        patients: list[Patient] = await patient_service.list_patients(db, limit, offset)
        return [PatientPublic(**patient.__dict__) for patient in patients]
    except Exception as e:
        raise HTTPException(status_code=500) from e


@patient_router.get("/{patient_id}")
async def get_patient(
    patient_id: int, db: AsyncSession = Depends(get_db)
) -> PatientPublic:
    try:
        patient: Patient = await patient_service.get_patient(db, patient_id)
        return PatientPublic(**patient.__dict__)
    except NotFoundError:
        raise HTTPException(status_code=404, detail="patient not found") from None
    except Exception as e:
        raise HTTPException(status_code=500) from e


@patient_router.patch("/{patient_id}")
async def update_patient(
    patient_id: int,
    patient: PatientUpdate,
    db: AsyncSession = Depends(get_db),
) -> PatientPublic:
    try:
        patient: Patient = await patient_service.update_patient(db, patient_id, patient)
        return PatientPublic(**patient.__dict__)
    except NotFoundError:
        raise HTTPException(status_code=404, detail="patient not found") from None
    except Exception as e:
        raise HTTPException(status_code=500) from e


@patient_router.delete("/{patient_id}")
async def delete_patient(
    patient_id: int,
    db: AsyncSession = Depends(get_db),
) -> dict[str, str]:
    try:
        await patient_service.delete_patient(db, patient_id)
        return {"details": "patient deleted"}
    except NotFoundError:
        raise HTTPException(status_code=404, detail="patient not found") from None
    except Exception as e:
        raise HTTPException(status_code=500) from e
