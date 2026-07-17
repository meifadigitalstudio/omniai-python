from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core import settings

engine = create_engine(
    settings.DATABASE_URL,
    echo=settings.DEBUG,
)

SessionLocal = sessionmaker(
    autoflush=False,
    autocommit=False,
    bind=engine,
)