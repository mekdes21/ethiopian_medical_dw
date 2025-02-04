from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
import models, schemas, crud
from database import SessionLocal, engine, init_db

# Initialize database
init_db()

# Create FastAPI app
app = FastAPI()

# Dependency for DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# API Endpoints
@app.get("/detections", response_model=list[schemas.DetectionSchema])
def read_detections(db: Session = Depends(get_db)):
    return crud.get_all_detections(db)

@app.get("/detections/{detection_id}", response_model=schemas.DetectionSchema)
def read_detection(detection_id: int, db: Session = Depends(get_db)):
    detection = crud.get_detection_by_id(db, detection_id)
    if detection is None:
        return {"error": "Detection not found"}
    return detection
