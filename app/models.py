# app/models.py
from sqlalchemy import Column, Integer, String, Float, Date, DateTime, ForeignKey, Text, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    full_name = Column(String)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class Patient(Base):
    __tablename__ = "patients"

    id = Column(Integer, primary_key=True, index=True)
    last_name = Column(String)
    first_name = Column(String)
    middle_name = Column(String, nullable=True)
    gender = Column(String)
    city = Column(String)
    street = Column(String)
    building = Column(String)
    email = Column(String)
    birth_date = Column(String)
    phone = Column(String)

    complaints = relationship("PatientComplaint", back_populates="patient")
    prescriptions = relationship("Prescription", back_populates="patient")


class Doctor(Base):
    __tablename__ = "doctors"

    id = Column(Integer, primary_key=True, index=True)
    last_name = Column(String)
    first_name = Column(String)
    middle_name = Column(String, nullable=True)
    specialty = Column(String)
    department = Column(String)
    email = Column(String)
    phone = Column(String)

    prescriptions = relationship("Prescription", back_populates="doctor")


class Diagnosis(Base):
    __tablename__ = "diagnoses"

    id = Column(Integer, primary_key=True, index=True)
    icd_code = Column(String, index=True)
    name = Column(String)
    category = Column(String)


class Symptom(Base):
    __tablename__ = "symptoms"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    description = Column(Text)
    category_name = Column(String)


class PatientComplaint(Base):
    __tablename__ = "patient_complaints"

    id = Column(Integer, primary_key=True, index=True)
    patient_last_name = Column(String)
    patient_first_name = Column(String)
    patient_middle_name = Column(String, nullable=True)
    symptom_name = Column(String)
    complaint_date = Column(Date)
    severity = Column(String)
    description = Column(Text)

    patient_id = Column(Integer, ForeignKey("patients.id"))
    patient = relationship("Patient", back_populates="complaints")


class Prescription(Base):
    __tablename__ = "prescriptions"

    id = Column(Integer, primary_key=True, index=True)
    patient_last_name = Column(String)
    patient_first_name = Column(String)
    patient_middle_name = Column(String, nullable=True)
    doctor_last_name = Column(String)
    doctor_first_name = Column(String)
    doctor_middle_name = Column(String, nullable=True)
    medication_name = Column(String)
    quantity = Column(Float)
    dose_unit = Column(String)
    frequency = Column(String)
    duration_in_days = Column(Integer)
    start_date = Column(Date)
    end_date = Column(Date, nullable=True)
    instructions = Column(Text)
    status = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    patient_id = Column(Integer, ForeignKey("patients.id"))
    doctor_id = Column(Integer, ForeignKey("doctors.id"))

    patient = relationship("Patient", back_populates="prescriptions")
    doctor = relationship("Doctor", back_populates="prescriptions")