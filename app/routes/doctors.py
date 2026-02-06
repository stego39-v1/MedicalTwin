from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from .. import crud, schemas, auth
from ..database import get_db

router = APIRouter(prefix="/doctors", tags=["doctors"])

@router.get("/", response_model=List[schemas.Doctor])
def read_doctors(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(auth.get_current_active_user)
):
    doctors = crud.get_doctors(db, skip=skip, limit=limit)
    return doctors

@router.get("/{doctor_id}", response_model=schemas.Doctor)
def read_doctor(
    doctor_id: int,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(auth.get_current_active_user)
):
    db_doctor = crud.get_doctor(db, doctor_id=doctor_id)
    if db_doctor is None:
        raise HTTPException(status_code=404, detail="Doctor not found")
    return db_doctor

@router.get("/specialty/{specialty}", response_model=List[schemas.Doctor])
def read_doctors_by_specialty(
    specialty: str,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(auth.get_current_active_user)
):
    doctors = crud.get_doctors_by_specialty(db, specialty=specialty)
    return doctors