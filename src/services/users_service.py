from src.config.database import get_db
from src.schemas.user_schemas import UsersResponse, UsersCreate
from src.models.user_model import Users
from sqlalchemy.orm import Session
from typing import List, Dict,Any


class UserService:

    def __init__(self, db: Session = None):
        self.db = db

    def create_users(self, user_data: UsersCreate) -> UsersResponse:
        if self.db is None:
            self.db = next(get_db())
        user = Users(**user_data.model_dump())
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user

    def find_all_users(self) -> List[Dict[str, Any]]:
        if self.db is None:
            self.db = next(get_db())
        users = self.db.query(Users).all()
        return [
            {
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
            }
            for user in users
        ]