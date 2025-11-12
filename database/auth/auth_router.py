from datetime import timedelta

from fastapi.security import OAuth2PasswordRequestForm
from fastapi import Depends, HTTPException, status, APIRouter
import auth
from auth.auth_handler import authenticate_user, ACCESS_TOKEN_EXPIRE_MINUTES, create_access_token, get_user, get_password_hash, create_refresh_token, check_token
from auth.auth_schemas import Token, UserResponse

from models import User, UserCreate, get_session
from sqlmodel import Session
import random

from models import LoginRequest
from fastapi import Response, Request
router = APIRouter()

#This is for looking up users to match tokens with sessions
registered_users = dict()

@router.post("/register", response_model=UserResponse)
async def register_user(user: UserCreate, db: Session = Depends(get_session)):
    db_user = get_user(db, user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="User already exists")
    print("submitted password:", user.password)
    hashed_password = get_password_hash(user.password)
    user_id = user_id = random.randint(100000, 999999) # uid is 100,000:999, THIS IS BAD CHECK FOR UID TAKEN
    db_user = User(
    id=user_id,
    username=user.username,
    email=user.email,
    hashed_password=hashed_password
    )   
    #db_user = User.model_validate(user, update={"hashed_password": hashed_password}) # Khoa I'm not smart enough to know what this does please fix <3
    #while():
        #user_id = random.randint(100000, 999999)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    access_token = create_access_token(int(user_id))
    refresh_token = create_refresh_token(int(user_id))

    return {
    "id": db_user.id,
    "username": db_user.username,
    "email": db_user.email,
    "access_token": access_token,
    "refresh_token": refresh_token,
    "token_type": "bearer",
    "sucsess" : True
    }

@router.post("/token")
async def login_for_access_token(
    response: Response,
    credentials: LoginRequest,
    db: Session = Depends(get_session)
):
    user = authenticate_user(db, credentials.username, credentials.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
              headers={"WWW-Authenticate": "Bearer"})
    
    user = get_user(db, credentials.username)
    user_id = user.id

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    #access_token = create_access_token(data={"sub": user.email}, expires_delta=access_token_expires)
    access_token = create_access_token(int(user_id))
    refresh_token = create_refresh_token(int(user_id))

    # Set cookies
    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,  # prevents JS access (for security)
        max_age=ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        samesite="Lax",  # or "None" if using cross-site cookies
        secure=False      # set True in production with HTTPS
    )

    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        max_age=60 * 60 * 24 * 7,  # e.g., 7 days
        samesite="Lax",
        secure=False
    )

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
        "user_id": user.id,
        "sucsess" : True
    }



@router.get("/me")
def protected(request: Request):
    access_token = request.cookies.get("access_token")
    user_id = check_token(access_token)

    if isinstance(user_id, HTTPException):
        raise user_id

    if not user_id:
        raise HTTPException(status_code=401, detail="Expired or invalid access token")

    return {"message": "You are authenticated!", "user_id": user_id}
    