from sqlalchemy.orm import Session
from . import models, schemas
from .auth import get_password_hash
from typing import List, Optional



def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = get_password_hash(user.password)
    db_user = models.User(
        username=user.username,
        email=user.email,
        full_name=user.full_name,
        hashed_password=hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user



def get_patient(db: Session, patient_id: int):
    return db.query(models.Patient).filter(models.Patient.id == patient_id).first()


def get_patients(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Patient).offset(skip).limit(limit).all()


def create_patient(db: Session, patient: schemas.PatientCreate):
    db_patient = models.Patient(**patient.model_dump())
    db.add(db_patient)
    db.commit()
    db.refresh(db_patient)
    return db_patient


def update_patient(db: Session, patient_id: int, patient_update: schemas.PatientCreate):
    db_patient = get_patient(db, patient_id)
    if db_patient:
        for key, value in patient_update.model_dump().items():
            setattr(db_patient, key, value)
        db.commit()
        db.refresh(db_patient)
    return db_patient


def delete_patient(db: Session, patient_id: int):
    db_patient = get_patient(db, patient_id)
    if db_patient:
        db.delete(db_patient)
        db.commit()
    return db_patient



def get_doctor(db: Session, doctor_id: int):
    return db.query(models.Doctor).filter(models.Doctor.id == doctor_id).first()


def get_doctors(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Doctor).offset(skip).limit(limit).all()


def get_doctors_by_specialty(db: Session, specialty: str):
    return db.query(models.Doctor).filter(models.Doctor.specialty == specialty).all()


def create_doctor(db: Session, doctor: schemas.DoctorCreate):
    db_doctor = models.Doctor(**doctor.model_dump())
    db.add(db_doctor)
    db.commit()
    db.refresh(db_doctor)
    return db_doctor



def get_diagnosis(db: Session, diagnosis_id: int):
    return db.query(models.Diagnosis).filter(models.Diagnosis.id == diagnosis_id).first()


def get_diagnosis_by_icd(db: Session, icd_code: str):
    return db.query(models.Diagnosis).filter(models.Diagnosis.icd_code == icd_code).first()


def get_diagnoses(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Diagnosis).offset(skip).limit(limit).all()


def get_diagnoses_by_category(db: Session, category: str):
    return db.query(models.Diagnosis).filter(models.Diagnosis.category == category).all()


def create_diagnosis(db: Session, diagnosis: schemas.DiagnosisCreate):
    db_diagnosis = models.Diagnosis(**diagnosis.model_dump())
    db.add(db_diagnosis)
    db.commit()
    db.refresh(db_diagnosis)
    return db_diagnosis



def get_symptom(db: Session, symptom_id: int):
    return db.query(models.Symptom).filter(models.Symptom.id == symptom_id).first()


def get_symptoms(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Symptom).offset(skip).limit(limit).all()


def get_symptoms_by_category(db: Session, category: str):
    return db.query(models.Symptom).filter(models.Symptom.category_name == category).all()


def create_symptom(db: Session, symptom: schemas.SymptomCreate):
    db_symptom = models.Symptom(**symptom.model_dump())
    db.add(db_symptom)
    db.commit()
    db.refresh(db_symptom)
    return db_symptom



def get_patient_complaint(db: Session, complaint_id: int):
    return db.query(models.PatientComplaint).filter(models.PatientComplaint.id == complaint_id).first()


def get_patient_complaints(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.PatientComplaint).offset(skip).limit(limit).all()


def get_complaints_by_patient(db: Session, patient_id: int):
    return db.query(models.PatientComplaint).filter(models.PatientComplaint.patient_id == patient_id).all()


def create_patient_complaint(db: Session, complaint: schemas.PatientComplaintCreate):

    patient = db.query(models.Patient).filter(
        models.Patient.last_name == complaint.patient_last_name,
        models.Patient.first_name == complaint.patient_first_name,
        models.Patient.middle_name == complaint.patient_middle_name
    ).first()

    db_complaint = models.PatientComplaint(
        **complaint.model_dump(),
        patient_id=patient.id if patient else None
    )
    db.add(db_complaint)
    db.commit()
    db.refresh(db_complaint)
    return db_complaint



def get_prescription(db: Session, prescription_id: int):
    return db.query(models.Prescription).filter(models.Prescription.id == prescription_id).first()


def get_prescriptions(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Prescription).offset(skip).limit(limit).all()


def get_prescriptions_by_patient(db: Session, patient_id: int):
    return db.query(models.Prescription).filter(models.Prescription.patient_id == patient_id).all()


def get_prescriptions_by_doctor(db: Session, doctor_id: int):
    return db.query(models.Prescription).filter(models.Prescription.doctor_id == doctor_id).all()


def get_prescriptions_by_status(db: Session, status: str):
    return db.query(models.Prescription).filter(models.Prescription.status == status).all()


def create_prescription(db: Session, prescription: schemas.PrescriptionCreate):

    patient = db.query(models.Patient).filter(
        models.Patient.last_name == prescription.patient_last_name,
        models.Patient.first_name == prescription.patient_first_name,
        models.Patient.middle_name == prescription.patient_middle_name
    ).first()

    doctor = db.query(models.Doctor).filter(
        models.Doctor.last_name == prescription.doctor_last_name,
        models.Doctor.first_name == prescription.doctor_first_name,
        models.Doctor.middle_name == prescription.doctor_middle_name
    ).first()

    db_prescription = models.Prescription(
        **prescription.model_dump(),
        patient_id=patient.id if patient else None,
        doctor_id=doctor.id if doctor else None
    )
    db.add(db_prescription)
    db.commit()
    db.refresh(db_prescription)
    return db_prescription


def update_prescription_status(db: Session, prescription_id: int, status: str):
    db_prescription = get_prescription(db, prescription_id)
    if db_prescription:
        db_prescription.status = status
        db.commit()
        db.refresh(db_prescription)
    return db_prescription