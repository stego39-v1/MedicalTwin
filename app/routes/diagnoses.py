from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from .. import crud, schemas, auth
from ..database import get_db

router = APIRouter(prefix="/diagnoses", tags=["diagnoses"])

@router.get("/", response_model=List[schemas.Diagnosis])
def read_diagnoses(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(auth.get_current_active_user)
):
    diagnoses = crud.get_diagnoses(db, skip=skip, limit=limit)
    return diagnoses

@router.get("/{diagnosis_id}", response_model=schemas.Diagnosis)
def read_diagnosis(
    diagnosis_id: int,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(auth.get_current_active_user)
):
    db_diagnosis = crud.get_diagnosis(db, diagnosis_id=diagnosis_id)
    if db_diagnosis is None:
        raise HTTPException(status_code=404, detail="Diagnosis not found")
    return db_diagnosis

@router.get("/icd/{icd_code}", response_model=schemas.Diagnosis)
def read_diagnosis_by_icd(
    icd_code: str,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(auth.get_current_active_user)
):
    db_diagnosis = crud.get_diagnosis_by_icd(db, icd_code=icd_code)
    if db_diagnosis is None:
        raise HTTPException(status_code=404, detail="Diagnosis not found")
    return db_diagnosis

@router.get("/category/{category}", response_model=List[schemas.Diagnosis])
def read_diagnoses_by_category(
    category: str,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(auth.get_current_active_user)
):
    diagnoses = crud.get_diagnoses_by_category(db, category=category)
    return diagnoses