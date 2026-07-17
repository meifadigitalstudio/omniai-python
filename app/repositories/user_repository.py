from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import User
from app.repositories import BaseRepository


class UserRepository(BaseRepository[User]):

    def __init__(self, db: Session):
        super().__init__(db)

    def get_by_email(
        self,
        email: str,
    ) -> User | None:

        return self.db.scalar(
            select(User).where(
                User.email == email
            )
        )

    def get_by_username(
        self,
        username: str,
    ) -> User | None:

        return self.db.scalar(
            select(User).where(
                User.username == username
            )
        )

    def create(
        self,
        user: User,
    ) -> User:

        self.db.add(user)

        self.db.commit()

        self.db.refresh(user)

        return user