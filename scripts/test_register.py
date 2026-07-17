from app.database.session import SessionLocal
from app.schemas.auth import RegisterRequest
from app.services.auth_service import AuthService

db = SessionLocal()

try:
    service = AuthService(db)

    result = service.register(
        RegisterRequest(
            full_name="Muhammad Rafli",
            username="zero",
            email="zero@example.com",
            password="Admin123!",
        )
    )

    print(result.model_dump())

finally:
    db.close()