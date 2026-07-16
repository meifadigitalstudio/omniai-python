from loguru import logger
import sys

logger.remove()

logger.add(
    sys.stdout,
    level="INFO",
    colorize=True,
)

logger.add(
    "app/logs/app.log",
    rotation="10 MB",
    retention="30 days",
    level="INFO",
)
