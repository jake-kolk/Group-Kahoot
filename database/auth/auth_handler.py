from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jwt.exceptions import InvalidTokenError
from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone
from jose import jwt, JWTError
from fastapi import Request, HTTPException, status

from auth.auth_schemas import TokenData

from models import User, get_session
from sqlmodel import Session, select

from dotenv import load_dotenv
import os
import secrets


# This is what the tokens are signed with, changes on server restart, its a 32 byte psudorandom string
# JWT_SECRET = secrets.token_urlsafe(32)
#SECRET_KEY = os.getenv("SECRET_KEY") or secrets.token_hex(32) 
SECRET_KEY = "05e1e5bb65f2a2ed05e0456145c1d21f25bcf93267a0dd0f7521a2c7d17d8965" #this is very insecure, use above line in prod, this is for testing
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 60))
REFRESH_TOKEN_EXPIRE_DAYS = int(os.getenv("REFRESH_TOKEN_EXPIRE_DAYS", 14))

load_dotenv()


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def get_user(db: Session, email: str):
    db_user = db.exec(select(User).where(User.email == email)).first()
    return db_user

def lookup_user(db: Session,  uid:int):
    db_user = db.exec(select(User).where(User.id == uid)).first()
    return db_user

def authenticate_user(db: Session, email: str, password: str):
    user = get_user(db, email)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user
'''
There are two types of tokens, accsess toekns and refresh tokens, acsses tokens only last about
15 minutes, while refresh tokens last for weeks, we need to make both
'''
"""
def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
"""
def create_access_token(user_id: int):
    return jwt.encode(
        {
            "sub": str(user_id),
            "exp": datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        },
        SECRET_KEY, algorithm=ALGORITHM
    )

def create_refresh_token(user_id: int):
    return jwt.encode(
        {
            "sub": str(user_id),
            "exp": datetime.now(timezone.utc) + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
        },
        SECRET_KEY, algorithm=ALGORITHM
    )


async def get_current_user(request: Request, db: Session = Depends(get_session)):
    # Get token from HttpOnly cookie
    token = request.cookies.get("access_token")
    
    user_id = check_token(token)
    if isinstance(user_id, HTTPException):
        raise user_id
    
    # Look up user in DB
    user = db.exec(select(User).where(User.id == user_id)).first()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials: user_id not found"
        )
    return user

async def get_current_active_user(current_user: User = Depends(get_current_user)):
    print("get_current_active_user")
    return current_user

def check_token(token: str):
    # 401 if no token present
    if not token:
        return None

    try:
        payload = jwt.decode(str(token), SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            return HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials"
            )
        token_data = TokenData(user_id=user_id)
    except JWTError as e:
        return HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Could not validate credentials: {str(e)}"
        )
    
    return user_id