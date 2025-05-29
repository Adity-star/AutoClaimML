# __init__.py
import logging
import os
from logging.handlers import RotatingFileHandler
from from_root import from_root
from datetime import datetime

# Constants
LOG_DIR = 'logs'
LOG_FILE_TIMESTAMP = datetime.now().strftime('%m_%d_%Y_%H_%M_%S')
MAX_LOG_SIZE = 5 * 1024 * 1024  # 5 MB
BACKUP_COUNT = 3  # Number of rotated log files to keep

# Ensure log directory exists
log_dir_path = os.path.join(from_root(), LOG_DIR)
os.makedirs(log_dir_path, exist_ok=True)


# helper function to get log file path
def get_log_file_path(filename_prefix: str = "app", use_timestamp: bool = True) -> str:
    """
    Constructs a log file path with optional timestamp.
    """
    filename = f"{filename_prefix}_{LOG_FILE_TIMESTAMP}.log" if use_timestamp else f"{filename_prefix}.log"
    return os.path.join(log_dir_path, filename)


def configure_logger(
    logger_name: str = "",
    level: int = logging.DEBUG,
    log_filename: str = None
) -> logging.Logger:
    """
    Configures and returns a logger with both file and console handlers.
    
    Args:
        logger_name (str): The name of the logger. Default is root logger.
        level (int): Logging level. Default is DEBUG.
        log_filename (str): Optional full path to log file. If None, generates one.
    
    Returns:
        logging.Logger: Configured logger instance.
    """
    logger = logging.getLogger(logger_name)

    # Prevent adding handlers multiple times
    if logger.handlers:
        return logger
    
    # set logging lebel and formatter
    logger.setLevel(level)
    formatter = logging.Formatter("[ %(asctime)s ] %(name)s - %(levelname)s - %(message)s")

    # Setup file handler
    if log_filename is None:
        log_filename = get_log_file_path()
    file_handler = RotatingFileHandler(log_filename, maxBytes=MAX_LOG_SIZE, backupCount=BACKUP_COUNT)
    file_handler.setFormatter(formatter)
    file_handler.setLevel(logging.DEBUG)

    # Setup console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    console_handler.setLevel(logging.INFO)
    
    #Add Handlers to Logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger


logger = configure_logger()
logger.info("Logger is configured and ready.")
