from schemas import CreateUser, UserResponse
from models import User
from database import get_db
from auth import pass_hash, get_current_user, create_access_token

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

router = APIRouter(prefix="/user")

@router.post("/register", status_code=201, response_model = UserResponse)
def create_users(user: CreateUser, db: Session= Depends(get_db)):

    user_name = db.query(User).filter(User.username == user.username).first()

    if user_name is not None:
        raise HTTPException(
            status_code=409,
            detail = "Username already exists"
        )
    hashed_password = pass_hash.hash(user.password)

    db_user = User(
        username = user.username,
        password_hash = hashed_password
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user

@router.post("/login")
def login_user(
    form = Depends(OAuth2PasswordRequestForm),
    db: Session = Depends(get_db)
):

    db_user = db.query(User).filter(User.username == form.username).first()

    if db_user is None:
        raise HTTPException(
            status_code=401,
            detail = "Invalid Username or Password"
        )

    jwt_sub = db_user.username
    data = {
        "sub": jwt_sub
    }

    check_password = pass_hash.verify(form.password, db_user.password_hash)

    if check_password is False:
        raise HTTPException(
            status_code=401,
            detail= "Invalid Username or Password"
        )
    token = create_access_token(data)

    return {
        "access_token": token,
        "token_type": "bearer"
    }

@router.get("/me", response_model=UserResponse)
def get_me(
    current_user = Depends(get_current_user)
):
    return current_user

#user.py