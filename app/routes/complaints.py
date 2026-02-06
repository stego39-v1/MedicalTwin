from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from .. import crud, schemas, auth
from ..database import get_db


router = APIRouter(prefix="/complaints", tags=["complaints"])

@router.get("/", response_model=List[schemas.PatientComplaint])
def read_complaints(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(auth.get_current_active_user)
):
    complaints = crud.get_patient_complaints(db, skip=skip, limit=limit)
    return complaints

@router.get("/{complaint_id}", response_model=schemas.PatientComplaint)
def read_complaint(
    complaint_id: int,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(auth.get_current_active_user)
):
    db_complaint = crud.get_patient_complaint(db, complaint_id=complaint_id)
    if db_complaint is None:
        raise HTTPException(status_code=404, detail="Complaint not found")
    return db_complaint

@router.get("/patient/{patient_id}", response_model=List[schemas.PatientComplaint])
def read_complaints_by_patient(
    patient_id: int,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(auth.get_current_active_user)
):
    complaints = crud.get_complaints_by_patient(db, patient_id=patient_id)
    return complaints