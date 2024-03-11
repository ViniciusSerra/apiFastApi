from fastapi import APIRouter, HTTPException
from src.schemas.user_schemas import UsersCreate, UsersResponse
from src.services.users_service import UserService
from loguru import logger

router = APIRouter(
    prefix="/user",
    tags=["User"],
)

user_service = UserService()  


@router.get('/', response_model=UsersResponse, status_code=200)
def get_all_users():
    try:
        users_data = user_service.find_all_users()
        return {"users": users_data}
    except Exception as e:
        logger.error('Error ao buscar usuario:', detail=str(e))
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/", response_model=UsersCreate, status_code=201)
def create_users(user: UsersCreate):
    try:
        return user_service.create_users(user) 
    except Exception as e:
        logger.error('Error ao criar usuario:', detail=str(e))
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}
