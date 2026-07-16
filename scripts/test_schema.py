from app.schemas.auth import RegisterRequest

data = RegisterRequest(
    full_name="Zero Sensei",
    username="zero",
    email="zero@example.com",
    password="Admin123!",
)

print(data.model_dump())
