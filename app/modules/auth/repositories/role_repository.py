from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import Role
from app.modules.auth.repositories import BaseRepository


class RoleRepository(BaseRepository[Role]):

    def __init__(self, db: Session):
        super().__init__(db)

    def get_by_code(self, code: str) -> Role | None:
        stmt = select(Role).where(Role.code == code)
        result = self.db.execute(stmt).scalar_one_or_none()
        return result

    def upsert(
        self,
        role: Role,
    ) -> Role:

        existing_role = self.get_by_code(role.code)

        if existing_role:

            existing_role.name = role.name
            existing_role.description = role.description
            existing_role.is_active = role.is_active
            existing_role.can_delete = role.can_delete

            self.db.commit()
            self.db.refresh(existing_role)

            return existing_role

        self.db.add(role)

        self.db.commit()
        self.db.refresh(role)

        return role
