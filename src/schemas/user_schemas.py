from pydantic import BaseModel, ConfigDict
from typing import List, Optional
from datetime import date, datetime


class UsersCreate(BaseModel):
    client_id: int
    role_id: int
    name: str
    login: str
    password: datetime
    updated_at: datetime
    status: str
    last_access: int
    email: str


class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: Optional[int]
    client_id: Optional[int]
    role_id: Optional[int]
    name: Optional[str]
    login: Optional[str]
    created_at: Optional[date]
    updated_at: Optional[date]
    status: Optional[str]
    last_access: Optional[date]
    n_tentativas: Optional[int]
    email: Optional[str]


class UsersResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    users: List[UserResponse]


class ClientDTO(BaseModel):
    id: Optional[int]
    name: Optional[str]


class RoleDTO(BaseModel):
    id: Optional[int]
    name: Optional[str]
