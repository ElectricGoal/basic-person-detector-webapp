import os
import shutil
from fastapi import FastAPI, UploadFile, File, HTTPException, Depends
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from pydantic import BaseModel
from sqlalchemy.orm import Session
from datetime import datetime
from typing import List

from .database import SessionLocal, engine
from . import models, detector

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

detector = detector.PersonDetectorV2()

# Mount the static directory so that visualized images can be served
app.mount("/static", StaticFiles(directory="static"), name="static")

# Dependency to get a session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Response model for clarity (optional)
class DetectionResponse(BaseModel):
    image_url: str
    count: int

class DetectionResultResponse(BaseModel):
    id: int
    timestamp: datetime
    count: int
    # Return the URL (relative to the static mount) for the image.
    image_url: str

    class Config:
        orm_mode = True

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.post("/upload", response_model=DetectionResponse)
async def upload_image(file: UploadFile = File(...), db: Session = Depends(get_db)):
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Invalid image file type")

    # Save the uploaded image temporarily
    upload_dir = "temp_uploads"
    os.makedirs(upload_dir, exist_ok=True)
    temp_file_path = os.path.join(upload_dir, file.filename)
    with open(temp_file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    try:
        # Run the dummy person detector
        visualized_path, count = detector.detect(temp_file_path)
    except Exception as e:
        os.remove(temp_file_path)
        raise HTTPException(status_code=500, detail=f"Detection failed: {e}")

    # Remove the temporary file
    os.remove(temp_file_path)

    # Save result to database
    result = models.DetectionResult(
        timestamp=datetime.now(),
        count=count,
        image_path=visualized_path
    )
    db.add(result)
    db.commit()
    db.refresh(result)

    # Return the URL (assuming the backend is hosted on the same domain)
    response = DetectionResponse(
        image_url=f"/static/{os.path.basename(visualized_path)}",
        count=count
    )
    return response


@app.get("/results", response_model=List[DetectionResultResponse])
def get_results(db: Session = Depends(get_db)):
    results = db.query(models.DetectionResult).order_by(models.DetectionResult.timestamp.desc()).all()
    # Update image_path to image_url for response (assuming images are served from /static)
    response = []
    for result in results:
        response.append(
            DetectionResultResponse(
                id=result.id,
                timestamp=result.timestamp,
                count=result.count,
                image_url=f"/static/{os.path.basename(result.image_path)}"
            )
        )
    return response

@app.delete("/results/{result_id}", status_code=204)
def delete_result(result_id: int, db: Session = Depends(get_db)):
    # Query for the detection result by ID
    result = db.query(models.DetectionResult).filter(models.DetectionResult.id == result_id).first()
    if not result:
        raise HTTPException(status_code=404, detail="Result not found")
    
    # Optionally remove the associated image file from the static folder
    image_file_path = result.image_path
    if os.path.exists(image_file_path):
        try:
            os.remove(image_file_path)
        except Exception as e:
            # Log error, but don't block deletion in the database
            print(f"Error deleting file {image_file_path}: {e}")
    
    # Delete the record from the database
    db.delete(result)
    db.commit()
    return