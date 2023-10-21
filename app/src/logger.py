"""Logging module for the application.""" ""
import logging

from loguru import logger

from .config import log_file


class InterceptHandler(logging.Handler):
    """Intercept logging messages and pass them to loguru."""

    LEVELS_MAP = {
        logging.CRITICAL: "CRITICAL",
        logging.ERROR: "ERROR",
        logging.WARNING: "WARNING",
        logging.INFO: "INFO",
        logging.DEBUG: "DEBUG",
    }

    def _get_level(self, record) -> str:
        """Get level of log message."""
        return self.LEVELS_MAP.get(record.levelno, record.levelno)

    def emit(self, record) -> None:
        """Emit log message."""
        logger_opt = logger.opt(depth=6, exception=record.exc_info, ansi=True, lazy=True)
        logger_opt.log(self._get_level(record), record.getMessage())


# Initialize
logging.basicConfig(level=logging.INFO, handlers=[InterceptHandler()])
log = logging.getLogger(__name__)
logger.add(
    log_file,
    rotation="1 d",
    compression="tar.xz",
    backtrace=True,
    diagnose=True,
    level="INFO",
)
log.info(f"Enabled logging into {log_file}")
