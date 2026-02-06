# app/main.py
from fastapi import FastAPI
from contextlib import asynccontextmanager
from datetime import datetime
import os
import sys
from pathlib import Path
import traceback  # Добавляем импорт traceback


def create_directories():
    """Создает все необходимые директории."""
    directories = [
        Path("data"),
        Path("app/data"),
    ]

    for directory in directories:
        directory.mkdir(parents=True, exist_ok=True)
        print(f"[INFO] Directory created/verified: {directory}")



create_directories()

print(f"[DEBUG] Current working directory: {os.getcwd()}")
print(f"[DEBUG] Files in app directory: {os.listdir('.')}")


project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))


try:
    from app.database import engine, Base, SessionLocal, get_db
    from app.utils import import_csv_data

    print("[INFO] Core modules imported successfully")


    try:
        from app.routes.auth import router as auth_router
        from app.routes.patients import router as patients_router
        from app.routes.doctors import router as doctors_router
        from app.routes.diagnoses import router as diagnoses_router
        from app.routes.prescriptions import router as prescriptions_router
        from app.routes.complaints import router as complaints_router

        print("[INFO] All routers imported successfully")
    except ImportError as e:
        print(f"[ERROR] Failed to import routers: {e}")
        traceback.print_exc()


        from fastapi import APIRouter

        auth_router = APIRouter()
        patients_router = APIRouter()
        doctors_router = APIRouter()
        diagnoses_router = APIRouter()
        prescriptions_router = APIRouter()
        complaints_router = APIRouter()


        @auth_router.get("/test")
        def test_auth():
            return {"message": "Auth router stub"}


        print("[INFO] Created stub routers")

except ImportError as e:
    print(f"[ERROR] Failed to import core modules: {e}")
    traceback.print_exc()
    raise


@asynccontextmanager
async def lifespan(app: FastAPI):

    print("[STARTUP] Starting up Hospital Management API...")

    try:

        print("[DATABASE] Creating database tables...")
        Base.metadata.create_all(bind=engine)
        print("[DATABASE] Database tables created successfully!")


        print("[DATA] Importing CSV data...")
        db = SessionLocal()
        try:
            import_csv_data(db)
        finally:
            db.close()

    except Exception as e:
        print(f"[ERROR] Error during startup: {e}")
        traceback.print_exc()

    yield


    print("[SHUTDOWN] Shutting down...")



app = FastAPI(
    title="Hospital Management API",
    description="API для управления больницей с аутентификацией JWT (использует PyJWT)",
    version="1.0.0",
    lifespan=lifespan
)


app.include_router(auth_router, prefix="/api/auth", tags=["authentication"])
app.include_router(patients_router, prefix="/api/patients", tags=["patients"])
app.include_router(doctors_router, prefix="/api/doctors", tags=["doctors"])
app.include_router(diagnoses_router, prefix="/api/diagnoses", tags=["diagnoses"])
app.include_router(prescriptions_router, prefix="/api/prescriptions", tags=["prescriptions"])
app.include_router(complaints_router, prefix="/api/complaints", tags=["complaints"])


@app.get("/")
def read_root():
    return {
        "message": "Hospital Management API with JWT Authentication (PyJWT)",
        "docs": "/docs",
        "redoc": "/redoc"
    }


@app.get("/health")
def health_check():
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}


if __name__ == "__main__":
    import uvicorn

    print("[INFO] Starting server on http://127.0.0.1:8080")
    uvicorn.run(
        "main:app",
        host="127.0.0.1",
        port=8080,
        reload=True,
        log_level="info"
    )