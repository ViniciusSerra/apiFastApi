from datetime import datetime, timedelta
from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel

from src.models.user_model import Users
from src.repository.user_repository import UserRepository
from ..schemas.auth_schemas import AccessToken, TokenData, UserIn, UserOut
from src.util.const import ACCESS_TOKEN_EXPIRE_MINUTES, ALGORITHM, SECRET_KEY

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def authentication(
    user_repository: Annotated[UserRepository, Depends(UserRepository)],
    token: Annotated[str, Depends(oauth2_scheme)],
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        usr_login: str = payload.get("sub")
        if usr_login is None:
            raise credentials_exception
        token_data = TokenData(usr_login=usr_login)
    except JWTError:
        raise credentials_exception

    user = user_repository.find_by_usr_login(token_data.usr_login)
    if user is None:
        raise credentials_exception

    if user.status != "S":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario está desabilitado",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return user


class AuthService:
    user_repository: UserRepository

    def __init__(
        self,
        user_repository: UserRepository = Depends(UserRepository),
    ) -> None:
        self.user_repository = user_repository
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        pass

    def verify_password(self, plain_password, hashed_password):
        return self.pwd_context.verify(plain_password, hashed_password)

    def get_password_hash(self, password):
        return self.pwd_context.hash(password)

    def login(self, login: str, password: str) -> AccessToken:
        user = self.user_repository.find_by_usr_login(login)
        # if user is None:
        #     raise HTTPException(status_code=401, detail="Usuário e/ou senha inválidos")

        # if not self.verify_password(password, user.password):
        #     raise HTTPException(status_code=401, detail="Usuário e/ou senha inválidos")

        access_token_expires = timedelta(minutes=int(30))
        token = self.create_access_token(
            data={"sub": user.login}, expires_delta=access_token_expires
        )
        # self.user_repository.update_last_login(user)

        return {
            "access_token": token,
            "token_type": "bearer",
            "user": {
                "id": user.id,
                "client_id": user.client_id,
                "role_id": user.role_id,
                "name": user.name,
                "login": user.login,
                "created_at": user.created_at,
                "updated_at": user.updated_at,
                "status": user.status,
                "last_access": user.last_access,
                "n_tentativas": user.n_tentativas,
                "email": user.email
            },
        }

    def create_access_token(self, data: dict, expires_delta: timedelta | None = None):
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=15)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt

    def create_user(self, user_create: UserIn) -> UserOut:
            user = Users()
            user.login = user_create.login
            user.password = self.get_password_hash("Teste@123")
            user.email = user_create.email
            user.name = user_create.name
            user.status = "Liberado"
            user.client_id = int(user_create.client_id)
            user.role_id = int(user_create.role_id)
            user_created = self.user_repository.save(user)

            company = self.user_repository.find_by_id(user_create.company)
            profile = self.user_repository.find_by_id(user_create.profile)

            return UserOut(
                id=user_created.id,
                username=user_create.username,
                email=user_create.email,
                name=user_create.name,
                company=company.id_company,
                profile=profile.profile_id,
            )
        
            
    def get_access_token(self, user: Users) -> AccessToken:
        access_token_expires = timedelta(minutes=int(ACCESS_TOKEN_EXPIRE_MINUTES))
        token = self.create_access_token(
            data={"sub": user.login}, expires_delta=access_token_expires
        )
        self.user_repository.update_last_login(user)

        return {
            "access_token": token,
            "token_type": "bearer",
            "user": {
                "id": user.id,
                "username": user.login,
                "email": user.email,
                "name": user.name,
            },
        }
