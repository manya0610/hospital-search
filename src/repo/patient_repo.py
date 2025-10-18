import logging
from collections.abc import Sequence

from sqlalchemy import CursorResult, ScalarResult, delete, insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.models import Patient
from src.exceptions.db_exceptions import DatabaseError, NotFoundError
from src.schemas.patient_schema import PatientCreate, PatientUpdate

logging.basicConfig()
logger = logging.getLogger(__name__)


async def create_patient(session: AsyncSession, patient: PatientCreate) -> Patient:
    try:
        query = insert(Patient).values(patient.model_dump()).returning(Patient)
        patient: Patient = await session.scalar(query)
        await session.commit()
        return patient
    except Exception as e:
        await session.rollback()
        logger.exception("Error creating patient=%s", patient, stack_info=True)
        raise DatabaseError from e


async def get_patient(session: AsyncSession, patient_id: int) -> Patient:
    try:
        query = select(Patient).where(Patient.patient_id == patient_id)
        result: ScalarResult = await session.scalars(query)
        patient = result.one_or_none()
        if patient is None:
            logger.exception(
                "patient with id=%s not found", patient_id, stack_info=True
            )
            raise NotFoundError
        return patient
    except NotFoundError:
        raise
    except Exception as e:
        logger.exception(
            "Error while getting patient with id=%s",
            patient_id,
            stack_info=True,
        )
        raise DatabaseError from e


# List all patients, returning a list of Patient objects
async def list_patients(
    session: AsyncSession,
    limit: int = 100,
    offset: int = 0,
) -> list[Patient]:
    try:
        query = select(Patient).limit(limit).offset(offset)
        response: ScalarResult = await session.scalars(query)
        patients: Sequence[Patient] = response.all()
        return patients
    except Exception as e:
        logger.exception("Error while listing patients", stack_info=True)
        raise DatabaseError from e


async def update_patient(
    session: AsyncSession, patient_id: int, patient: PatientUpdate
) -> Patient:
    try:
        query = (
            update(Patient)
            .where(Patient.patient_id == patient_id)
            .values(**patient.model_dump())
            .returning(Patient)
        )
        patient: Patient = await session.scalar(query)
        await session.commit()
        if patient is None:
            logger.warning("No patient found with id=%s to update", patient_id)
            raise NotFoundError
        return patient
    except NotFoundError:
        raise
    except Exception as e:
        await session.rollback()
        logger.exception(
            "Error updating patient with id=%s, data=%s",
            patient_id,
            patient,
            stack_info=True,
        )
        raise DatabaseError from e


async def delete_patient(session: AsyncSession, patient_id: int) -> int:
    try:
        query = delete(Patient).where(Patient.patient_id == patient_id)
        response: CursorResult = await session.execute(query)
        await session.commit()

        if response.rowcount == 0:
            logger.warning("No patient found with id=%s to delete", patient_id)
            raise NotFoundError
        return response.rowcount
    except NotFoundError:
        raise
    except Exception as e:
        await session.rollback()
        logger.exception(
            "Error deleting patient with id=%s", patient_id, stack_info=True
        )
        raise DatabaseError from e
