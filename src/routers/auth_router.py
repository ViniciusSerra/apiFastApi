from typing import Annotated, Dict

from fastapi import APIRouter, Depends, HTTPException, status

from src.models.user_model import Users
from src.schemas.auth_schemas import AccessToken, UserLogin
from src.services.auth_service import AuthService, authentication
from loguru import logger

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
)


@router.post("/signin")
async def login(
    data: UserLogin, service: AuthService = Depends(AuthService)
) -> dict[str, AccessToken]:
    try:
        accessToken = service.login(data.login, data.password)
        logger.info("Login successful for user: {}", data.login)
        return {"users": accessToken}
    except Exception as e:
        logger.error("Failed to sign in user: {}. Error: {}", data.login, e)

@router.get("/token")
async def create_user(
        current_user: Users = Depends(authentication),
        service: AuthService = Depends(AuthService),
) -> AccessToken:
    accessToken = service.get_acess_token(current_user)
    return accessToken
