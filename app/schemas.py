from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import date, datetime


class UserBase(BaseModel):
    username: str
    email: EmailStr
    full_name: Optional[str] = None


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    is_active: bool

    class Config:
        from_attributes = True



class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None



class PatientBase(BaseModel):
    last_name: str
    first_name: str
    middle_name: Optional[str] = None
    gender: str
    city: str
    street: str
    building: str
    email: str
    birth_date: str
    phone: str


class PatientCreate(PatientBase):
    pass


class Patient(PatientBase):
    id: int

    class Config:
        from_attributes = True


class DoctorBase(BaseModel):
    last_name: str
    first_name: str
    middle_name: Optional[str] = None
    specialty: str
    department: str
    email: str
    phone: str


class DoctorCreate(DoctorBase):
    pass


class Doctor(DoctorBase):
    id: int

    class Config:
        from_attributes = True



class DiagnosisBase(BaseModel):
    icd_code: str
    name: str
    category: str


class DiagnosisCreate(DiagnosisBase):
    pass


class Diagnosis(DiagnosisBase):
    id: int

    class Config:
        from_attributes = True



class SymptomBase(BaseModel):
    name: str
    description: str
    category_name: str


class SymptomCreate(SymptomBase):
    pass


class Symptom(SymptomBase):
    id: int

    class Config:
        from_attributes = True



class PatientComplaintBase(BaseModel):
    patient_last_name: str
    patient_first_name: str
    patient_middle_name: Optional[str] = None
    symptom_name: str
    complaint_date: date
    severity: str
    description: str


class PatientComplaintCreate(PatientComplaintBase):
    pass


class PatientComplaint(PatientComplaintBase):
    id: int

    class Config:
        from_attributes = True



class PrescriptionBase(BaseModel):
    patient_last_name: str
    patient_first_name: str
    patient_middle_name: Optional[str] = None
    doctor_last_name: str
    doctor_first_name: str
    doctor_middle_name: Optional[str] = None
    medication_name: str
    quantity: float
    dose_unit: str
    frequency: str
    duration_in_days: int
    start_date: date
    end_date: Optional[date] = None
    instructions: str
    status: str
    created_at: datetime


class PrescriptionCreate(PrescriptionBase):
    pass


class Prescription(PrescriptionBase):
    id: int

    class Config:
        from_attributes = True