from sqlalchemy import Column, Integer, Float, String
from database import Base

class Detection(Base):
    __tablename__ = "yolo_detections"

    id = Column(Integer, primary_key=True, index=True)
    image = Column(String, index=True)
    class_id = Column(Integer)
    x = Column(Float)
    y = Column(Float)
    width = Column(Float)
    height = Column(Float)
    confidence = Column(Float)
