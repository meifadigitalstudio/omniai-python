from fastapi import APIRouter

from app.api.auth import router as auth_router

router = APIRouter(
    prefix="/api/v1",
)

@router.get("/health")
def health():
    return {
        "status": "ok"
    }


router.include_router(auth_router)