from fastapi import APIRouter, Depends
from typing import Annotated

from auth.auth_handler import get_current_active_user
from auth.auth_schemas import UserResponse
# from dbModels import User
from models import User
from fastapi import Request, Depends

router = APIRouter()

@router.get("/users/me/",  response_model=UserResponse)
async def read_user_me(current_user: User = Depends(get_current_active_user)):
    return current_user
