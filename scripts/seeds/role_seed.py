from sqlalchemy.orm import Session

from app.models import Role
from app.repositories import RoleRepository


class RoleSeed:

    def __init__(self, db: Session):
        self.role_repository = RoleRepository(db)

    def seed(self) -> None:
        roles = [
            {
                "name": "Super Admin",
                "code": "SUPER_ADMIN",
                "description": "Super Administrator role with full access",
                "is_active": True,
                "can_delete": False,
            },
            {
                "name": "User",
                "code": "USER",
                "description": "Regular user role with limited access",
                "is_active": True,
                "can_delete": False,
            },
        ]

        print("Seeding Roles...")

        for role in roles:
            self.role_repository.upsert(
                Role(**role)
            )

        print("Roles seeded successfully.")