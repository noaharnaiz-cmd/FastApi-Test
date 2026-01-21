from fastapi import FastAPI, APIRouter, Depends, HTTPException, status
from .. import schemas, models, database
from sqlalchemy.orm import Session
from ..hashing import Hash
from ..repository import user as userRepository




router = APIRouter(prefix="/user", tags =["Users"])

get_db = database.get_db

@router.post("/", response_model=schemas.ShowUser)
def create_user(request: schemas.User, db: Session = Depends(database.get_db)):
    return userRepository.create(request, db)


@router.get("/{id}", response_model=schemas.ShowUser)
def get_user(id: int, db: Session = Depends(database.get_db)):
    return userRepository.show(id, db)