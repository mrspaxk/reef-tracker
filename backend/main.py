# backend/main.py
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
import os

from database import SessionLocal, engine, Base
from models import TankLog
from pydantic import BaseModel

# ----------------------------
# Pydantic schema for request
# ----------------------------
class LogCreate(BaseModel):
    date: str
    ph: float
    salinity: float
    nitrate: float
    temperature: float
    notes: str

# ----------------------------
# App setup
# ----------------------------
app = FastAPI()

# CORS (important for dev and multi-device)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # allow any origin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create database tables
Base.metadata.create_all(bind=engine)

# ----------------------------
# Serve React frontend
# ----------------------------
frontend_path = os.path.join(os.path.dirname(__file__), "../frontend/build")
if os.path.exists(frontend_path):
    app.mount("/", StaticFiles(directory=frontend_path, html=True), name="frontend")
else:
    print("WARNING: frontend/build not found. Run `npm run build` in frontend folder first.")

# ----------------------------
# Dependency
# ----------------------------
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ----------------------------
# API Routes
# ----------------------------
@app.get("/logs")
def get_logs():
    db = SessionLocal()
    logs = db.query(TankLog).all()
    return logs

@app.post("/logs")
def create_log(log: LogCreate):
    db = SessionLocal()
    new_log = TankLog(
        date=log.date,
        ph=log.ph,
        salinity=log.salinity,
        nitrate=log.nitrate,
        temperature=log.temperature,
        notes=log.notes
    )
    db.add(new_log)
    db.commit()
    db.refresh(new_log)
    return new_log