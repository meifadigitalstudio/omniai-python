from sqlalchemy import select

from app.models import User
from app.modules.auth.repositories import BaseRepository


class UserRepository(BaseRepository[User]):

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

        return user

    def update(
        self,
        user: User,
    ) -> User:

        return user

    def delete(
        self,
        user: User,
    ) -> None:

        self.db.delete(user)