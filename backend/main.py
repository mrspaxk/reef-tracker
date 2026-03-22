from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from database import SessionLocal, engine
from models import Base, TankLog
from pydantic import BaseModel
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)

class LogCreate(BaseModel):
    date: str
    ph: float
    salinity: float
    nitrate: float
    temperature: float
    notes: str

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

@app.get("/logs")
def get_logs():
    db = SessionLocal()
    return db.query(TankLog).all()

# Serve React frontend
frontend_path = os.path.join(os.path.dirname(__file__), "../frontend/build")

if os.path.exists(frontend_path):
    app.mount("/", StaticFiles(directory=frontend_path, html=True), name="frontend")
else:
    print("⚠️ frontend/build not found. Run npm run build")