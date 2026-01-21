from fastapi import APIRouter, HTTPException, status, Depends
from datetime import datetime, timedelta, timezone
from fastapi.security import OAuth2PasswordRequestForm
from jose import JWTError, jwt
from ..hashing import Hash
from .. import schemas, database, models, token
from sqlalchemy.orm import Session
router = APIRouter(tags=["Authentication"])

@router.post("/login")
def login(request: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):

    # 1️⃣ Buscar usuario por email
    user = db.query(models.User).filter(
        models.User.email == request.username
    ).first()

    # 2️⃣ Si no existe
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )

    # 3️⃣ Verificar contraseña (ESTO ES LO IMPORTANTE)
    if not Hash.verify(request.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )
    

    access_token = token.create_access_token(
        data={"sub": user.email}
    )
    return schemas.Token(access_token=access_token, token_type="bearer")


