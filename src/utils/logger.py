"""
Custom Logger Setup
Initializes the Loguru logger for consistent structured logging.
"""

from loguru import logger
import os
from datetime import datetime


def init_logger(log_dir: str = "./logs"):
    """Initialize the Loguru logger with rotating log files."""
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    log_file = os.path.join(log_dir, f"copilot_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log")

    logger.add(
        log_file,
        rotation="10 MB",
        retention="10 days",
        level="INFO",
        format="{time:YYYY-MM-DD at HH:mm:ss} | {level} | {message}"
    )

    logger.info(f"Logger initialized. Log file: {log_file}")
    return logger
