import os
import sys
from pathlib import Path

from loguru import logger


class Log:
    """
    A wrapper around Loguru to provide a simple, reusable logging interface.
    Supports console and file logging with rotation and retention.
    """

    def __init__(
        self,
        log_dir: str = "logs",
        log_name: str = "app.log",
        rotation: str = "10 MB",
        retention: str = "7 days",
        level: str = "INFO",
    ):
        """
        Initialize a Loguru logger instance.

        Args:
            log_dir (str): Directory to store log files.
            log_name (str): Log file name.
            rotation (str): When to rotate the log file (e.g., "10 MB", "1 week").
            retention (str): How long to keep old log files (e.g., "7 days").
            level (str): Minimum log level to capture.
        """
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(parents=True, exist_ok=True)

        log_path = self.log_dir / log_name

        # Remove default Loguru handlers to avoid duplicate logs
        logger.remove()

        # Console handler
        logger.add(
            sys.stdout,
            colorize=True,
            format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
            "<level>{level: <8}</level> | "
            "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - "
            "<level>{message}</level>",
            level=level,
        )

        # File handler
        logger.add(
            log_path,
            rotation=rotation,
            retention=retention,
            compression="zip",
            encoding="utf-8",
            enqueue=True,
            backtrace=True,
            diagnose=True,
            level=level,
            format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}",
        )

        self.logger = logger

    def get_logger(self):
        """Return the configured Loguru logger."""
        return self.logger
