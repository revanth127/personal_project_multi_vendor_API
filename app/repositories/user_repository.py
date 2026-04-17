from sqlalchemy.orm import Session
from app.repositories.base import BaseRepository
import app.models as models

class UserRepository(BaseRepository[models.Users]):
    def __init__(self, db: Session):
        super().__init__(models.Users, db)

    def get_by_email(self, email: str) -> models.Users | None:
        return self.get_by_field("email", email)

    def create_user(self, email: str, hashed_password: str, role: str) -> models.Users:
        user_data = {
            "email": email,
            "hashed_password": hashed_password,
            "role": role
        }
        return self.create(user_data)
