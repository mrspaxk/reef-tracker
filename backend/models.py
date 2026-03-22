from sqlalchemy import Column, Integer, Float, String
from database import Base


class TankLog(Base):
    __tablename__ = "tank_logs"

    id = Column(Integer, primary_key=True, index=True)
    date = Column(String)
    ph = Column(Float)
    salinity = Column(Float)
    nitrate = Column(Float)
    temperature = Column(Float)
    notes = Column(String)
