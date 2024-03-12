from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from src.models.user_model import Users
from src.schemas.auth_schemas import AccessToken, UserIn, UserLogin, UserOut
from src.services.auth_service import AuthService, authentication

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
)


@router.post("/singin")
async def login(
    data: UserLogin, service: AuthService = Depends(AuthService)
) -> AccessToken:
    accessToken = service.login(data.login, data.password)
    return accessToken


@router.post("/singup", status_code=status.HTTP_201_CREATED)
async def create_user(
    data: UserIn,
    service: AuthService = Depends(AuthService),
) -> UserOut:
    user_out = service.create_user(data)
    return user_out


@router.get("/token")
async def create_user(
    current_user: Users = Depends(authentication),
    service: AuthService = Depends(AuthService),
) -> AccessToken:
    accessToken = service.get_acess_token(current_user)
    return accessToken