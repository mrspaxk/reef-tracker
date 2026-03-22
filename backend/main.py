from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import SessionLocal, engine
from models import Base, TankLog
from pydantic import BaseModel

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

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
@app.post("/logs")
def create_log(log: LogCreate):
    db = SessionLocal()

    new_log = TankLog(
        date=log.get("date"),
        ph=log.get("ph"),
        salinity=log.get("salinity"),
        nitrate=log.get("nitrate"),
        temperature=log.get("temperature"),
        notes=log.get("notes")
    )

    db.add(new_log)
    db.commit()
    db.refresh(new_log)

    return new_log

@app.get("/logs")
def get_logs():
    db = SessionLocal()
    logs = db.query(TankLog).all()
    return logs