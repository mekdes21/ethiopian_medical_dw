from pydantic import BaseModel

class DetectionSchema(BaseModel):
    id: int
    image: str
    class_id: int
    x: float
    y: float
    width: float
    height: float
    confidence: float

    class Config:
        orm_mode = True
