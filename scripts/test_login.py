from app.database.session import SessionLocal
from app.schemas.auth import LoginRequest
from app.services.auth_service import AuthService

db = SessionLocal()

try:
    service = AuthService(db)

    result = service.login(
        LoginRequest(
            identifier="zero@example.com",
            password="Admin123!",
        )
    )

    print(result.model_dump())

finally:
    db.close()