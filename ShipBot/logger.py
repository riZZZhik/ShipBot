# Import logging libraries
import logging
from loguru import logger

# Module imports
from .config import log_file


# Default logging module using loguru
class InterceptHandler(logging.Handler):
    LEVELS_MAP = {
        logging.CRITICAL: "CRITICAL",
        logging.ERROR: "ERROR",
        logging.WARNING: "WARNING",
        logging.INFO: "INFO",
        logging.DEBUG: "DEBUG"
    }

    def _get_level(self, record):
        return self.LEVELS_MAP.get(record.levelno, record.levelno)

    def emit(self, record):
        logger_opt = logger.opt(depth=6, exception=record.exc_info, ansi=True, lazy=True)
        logger_opt.log(self._get_level(record), record.getMessage())


# Initialization
logging.basicConfig(level=logging.INFO, handlers=[InterceptHandler()])
log = logging.getLogger(__name__)
logger.add(log_file, rotation="1 d", compression="tar.xz", backtrace=True, diagnose=True, level="INFO")
log.info(f"Enabled logging into {log_file}")
