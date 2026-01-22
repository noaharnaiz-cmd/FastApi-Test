from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta

from ..hashing import Hash
from .. import database, models, token, schemas

router = APIRouter(tags=["Authentication"])

@router.post("/login", response_model=schemas.Token)
def login(request: OAuth2PasswordRequestForm = Depends(),
          db: Session = Depends(database.get_db)):

    user = db.query(models.User).filter(models.User.email == request.username).first()

    if not user or not Hash.verify(request.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )

    access_token = token.create_access_token(
        data={"sub": user.email},
        expires_delta=timedelta(minutes=token.ACCESS_TOKEN_EXPIRE_MINUTES)
    )

    return {"access_token": access_token, "token_type": "bearer"}


