from sqlalchemy.orm import Session
import models, schemas

def get_all_detections(db: Session):
    return db.query(models.Detection).all()

def get_detection_by_id(db: Session, detection_id: int):
    return db.query(models.Detection).filter(models.Detection.id == detection_id).first()
