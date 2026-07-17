from sqlalchemy import select

from app.models.auth.refresh_token import RefreshToken
from app.modules.auth.repositories import BaseRepository


class RefreshRepository(BaseRepository[RefreshToken]):

    def get_by_user_id(
        self,
        user_id: int
    ) -> list[RefreshToken]:

        return self.db.scalars(
            select(RefreshToken).where(
                RefreshToken.user_id == user_id
            )
        ).all()

    def create(
        self,
        data: RefreshToken,
    ) -> RefreshToken:

        self.db.add(data)

        return data

    def delete(
        self,
        data: RefreshToken,
    ) -> None:

        self.db.delete(data)