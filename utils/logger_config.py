
import sys
from loguru import logger

def setup_logger():
    logger.remove()
    logger.add(sys.stderr, level="INFO")
    logger.add("app.log", rotation="10 MB", level="DEBUG", enqueue=True, backtrace=True, diagnose=True)

