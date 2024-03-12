from pydantic import BaseModel, EmailStr

class UserLogin(BaseModel):
    login: str
    password: str

class TokenData(BaseModel):
    usr_login: str | None = None

class UserIn(BaseModel):
    login: str
    password: str
    email: EmailStr
    name: str
    client_id: int
    role_id: int
    status: str

class UserOut(BaseModel):
    id: int
    login: str
    email: EmailStr
    name: str

class AccessToken(BaseModel):
    access_token: str
    token_type: str
    user: UserOut
