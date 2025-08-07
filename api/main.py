from fastapi import FastAPI , HTTPException, Depends,UploadFile, File, Form
from pydantic import BaseModel
from typing import List,Annotated
import bcrypt
import os
import shutil
import models
from database import SessionLocal, engine
from sqlalchemy.orm import Session
import datetime

app = FastAPI()
models.Base.metadata.create_all(bind=engine)

class User(BaseModel):
    username: str
    password: str

class log(BaseModel):
    date: str
    time_in: str
    time_out: str
    comment: str
    image_path: str

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]


@app.get("/")
def read_root():
    return {"Hello World"}


@app.post("/users")
async def create_user(user: User, db: db_dependency):
    try:
        # Check if user exists
        existing_user = db.query(models.User).filter(models.User.username == user.username).first()
        if existing_user:
            raise HTTPException(status_code=400, detail="Username already exists")

        # Hash password
        hashed_password = bcrypt.hashpw(user.password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

        # Create and store user
        db_user = models.User(username=user.username, password=hashed_password)
        db.add(db_user)
        db.commit()
        db.refresh(db_user)


        return {
            "message": "User created successfully",
            "user": {"id": db_user.id, "username": db_user.username}
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Server error: {str(e)}")

@app.post("/login")
async def login(request: User, db: db_dependency):
    user = db.query(models.User).filter(models.User.username == request.username).first()

    if not user:
        raise HTTPException(status_code=401, detail="Invalid username or password")

    # Compare the plain password with the hashed password from DB
    if not bcrypt.checkpw(request.password.encode('utf-8'), user.password.encode('utf-8')):
        raise HTTPException(status_code=401, detail="Invalid username or password")

    return {"message": "Login successful", "username": user.username}

@app.post("/logs")
async def logs(
    date: str = Form(...),
    time_in: str = Form(...),
    time_out: str = Form(...),
    comment: str = Form(...),
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    try:
        # Create uploads folder if it doesn't exist
        upload_folder = "uploads"
        os.makedirs(upload_folder, exist_ok=True)

        # Example: add timestamp to filename

        timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        new_filename = f"{timestamp}_{file.filename}"

        file_location = os.path.join(upload_folder, new_filename)
        with open(file_location, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # Save log to DB
        db_logs = models.logs(
            date=date,
            time_in=time_in,
            time_out=time_out,
            comment=comment,
            image_path=file_location
        )
        db.add(db_logs)
        db.commit()
        db.refresh(db_logs)

        return {
            "message": "Log created successfully",
            "log": {
                "id": db_logs.id,
                "date": db_logs.date,
                "image_path": db_logs.image_path
            }
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Server error: {str(e)}")


@app.get("/logs")
async def get_logs(db: db_dependency):
    log = db.query(models.logs).all()
    return log
