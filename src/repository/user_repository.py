from datetime import datetime

from src.config.database import get_db
from src.models.user_model import Users
from loguru import logger
from typing import Optional
from fastapi import Depends
from sqlalchemy.orm import Session



class UserRepository:
    def __init__(self, db: Session = Depends(get_db)):
        self.db = db

    def find_all(self):
        try:
            list_user = self.db.query(Users).all()
            logger.info(list_user)
            return list_user
        except Exception as e:
            logger.error(f"Error occurred while fetching users: {e}")
            return []

    def find_by_usr_login(self, login: str) -> Optional[Users]:
        try:
            user_login = self.db.query(Users).filter(Users.login == login).first()
            return user_login
        except Exception as e:
            logger.error(f"Error occurred while fetching users: {e}")
            return []    
        

    def update_last_login(self, user: Users) -> Users:
        user.last_access = datetime.now()
        self.db.commit()
        return user

    def save(self, user: Users) -> Users:
            self.db.add(user)
            self.db.commit()
            self.db.refresh(user)
            return user