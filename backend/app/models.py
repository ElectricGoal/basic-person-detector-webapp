from sqlalchemy import Column, Integer, String, DateTime
from .database import Base
from datetime import datetime

class DetectionResult(Base):
    __tablename__ = "detection_results"

    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime, default=datetime.now())
    count = Column(Integer)
    image_path = Column(String)