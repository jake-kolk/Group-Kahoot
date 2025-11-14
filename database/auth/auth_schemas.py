from pydantic import BaseModel

class TokenData(BaseModel):
    email: str | None = None

class GameServerToken(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str
    user_id : int
    sucsess : bool


class UserResponse(BaseModel):
    id: int
    username: str
    email: str | None = None
