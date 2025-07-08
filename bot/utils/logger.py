import logging
import os
from datetime import datetime

LOG_DIR = "logs"

def setup_logger(name, log_file=None, level=logging.INFO):
    """Creates a reusable logger with file and console output."""
    if not os.path.exists(LOG_DIR):
        os.makedirs(LOG_DIR)

    if not log_file:
        timestamp = datetime.utcnow().strftime("%Y-%m-%d")
        log_file = os.path.join(LOG_DIR, f"{name}_{timestamp}.log")

    logger = logging.getLogger(name)
    logger.setLevel(level)

    if not logger.handlers:
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(level)
        file_formatter = logging.Formatter('%(asctime)s [%(levelname)s]: %(message)s')
        file_handler.setFormatter(file_formatter)

        stream_handler = logging.StreamHandler()
        stream_handler.setLevel(level)
        stream_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        stream_handler.setFormatter(stream_formatter)

        logger.addHandler(file_handler)
        logger.addHandler(stream_handler)

    return logger
