from fastapi.security import APIKeyHeader, OAuth2PasswordBearer
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from pwdlib import PasswordHash
from datetime import datetime, timedelta, timezone
import jwt
import os
from dotenv import load_dotenv

from database import get_db
from models import User

load_dotenv()

API_KEY = os.getenv("API_KEY")
SECRET_KEY = os.getenv("SECRET_KEY")

if not API_KEY or not SECRET_KEY:
    raise RuntimeError("API_KEY and SECRET_KEY must be set in .env")

key = APIKeyHeader(
    name="X-API-KEY",
    auto_error=False
)


ALGORITHM = "HS256"

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/user/login",
    auto_error=False
)

def validate_api_key_value(api_key):
    if api_key == API_KEY:
        pass
    else:
        raise HTTPException(
            status_code=401,
            detail="Authentication failed"
        )

def verify_api_key(api_key = Depends(key)):
    validate_api_key_value(api_key)

pass_hash = PasswordHash.recommended()

def create_access_token(data: dict):
    to_encode = data.copy()
    token_exp = datetime.now(timezone.utc) + timedelta(minutes=30)
    to_encode["exp"] = token_exp

    result = jwt.encode(
        to_encode,
        SECRET_KEY,
        algorithm = ALGORITHM
    )

    return result

def get_current_user(
        token = Depends(oauth2_scheme),
        db: Session = Depends(get_db)
):
    if token is None:
        raise HTTPException(
            headers={"WWW-Authenticate": "Bearer"},
            status_code=401,
            detail="Authentication failed"
        )
    return verify_jwt(token, db)

def authenticate_user(
    token=Depends(oauth2_scheme),
    api_key=Depends(key),
    db: Session=Depends(get_db)
):
    if token is not None:

        try:
            current_user = verify_jwt(token, db)
            return current_user
        except HTTPException:
            pass

    validate_api_key_value(api_key)
    return True
    
def verify_jwt(token, db: Session):

    try:

        decoded = jwt.decode(
            token,
            SECRET_KEY,
            algorithms = [ALGORITHM]
        )

        sub = decoded["sub"]

        current_user = db.query(User).filter(User.username == sub).first()

        if current_user is None:
            raise HTTPException(
                headers={"WWW-Authenticate": "Bearer"},
                status_code=401,
                detail="Authentication failed"
            )
        return current_user
    
    except jwt.InvalidTokenError:
        raise HTTPException(
            headers={"WWW-Authenticate": "Bearer"},
            status_code=401,
            detail = "Authentication failed"
        )