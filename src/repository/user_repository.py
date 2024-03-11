from datetime import datetime

from src.config.database import get_db
from src.models.user_model import Users
from loguru import logger


class UserRepository:
    def __init__(self):
        self.db = get_db()

    def find_all(self):
        try:
            list_user = self.db.query(Users).all()
            logger.info(list_user)
            return list_user
        except Exception as e:
            logger.error(f"Error occurred while fetching users: {e}")
            return []

    def find_by_usr_login(self, login: str) -> Users:
        user_login = self.db.query(Users).filter(Users.login == login).first()
        return user_login

    def update_last_login(self, user: Users) -> Users:
        user.last_access = datetime.now()
        self.db.commit()
        return user
