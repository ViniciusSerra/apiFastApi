from pydantic import BaseModel, ConfigDict
from src.schemas.user_schemas import UsersResponse


class UserLogin(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    login: str
    password: str


class TokenData(BaseModel):
    usr_login: str | None = None


class AccessToken(BaseModel):
    access_token: str
    token_type: str
    user: UsersResponse


class TokenData(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    usr_login: str | None = None
