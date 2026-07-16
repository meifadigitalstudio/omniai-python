from app.core.security import hash_password, verify_password

password = "Admin123!"

hashed = hash_password(password)

print("Hash:", hashed)
print("Verify:", verify_password(password, hashed))