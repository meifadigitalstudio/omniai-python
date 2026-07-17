import sys
from pathlib import Path

from loguru import logger

from app.core.config import settings

LOG_DIR = Path("logs")
LOG_DIR.mkdir(exist_ok=True)

logger.remove()

# Console
logger.add(
    sys.stdout,
    level="DEBUG" if settings.DEBUG else "INFO",
    colorize=True,
    backtrace=settings.DEBUG,
    diagnose=settings.DEBUG,
    enqueue=True,
    format=(
        "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
        "<level>{level:<8}</level> | "
        "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> | "
        "<level>{message}</level>"
    ),
)

# Application Log
logger.add(
    LOG_DIR / "app.log",
    level="INFO",
    rotation="10 MB",
    retention="30 days",
    compression="zip",
    enqueue=True,
    encoding="utf-8",
)

# Error Log
logger.add(
    LOG_DIR / "error.log",
    level="ERROR",
    rotation="10 MB",
    retention="60 days",
    compression="zip",
    enqueue=True,
    encoding="utf-8",
)

__all__ = ["logger"]