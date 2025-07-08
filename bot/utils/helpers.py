import json
import logging
import os

def load_config(config_path='config.json'):
    """
    Load the JSON config file and return as a dictionary.
    """
    if not os.path.exists(config_path):
        raise FileNotFoundError(f"Config file not found: {config_path}")
    with open(config_path, 'r') as f:
        config = json.load(f)
    return config

def setup_logger(log_file='bot.log', level=logging.INFO):
    """
    Setup and return a logger instance.
    """
    logger = logging.getLogger()
    logger.setLevel(level)
    
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

    # Console handler
    ch = logging.StreamHandler()
    ch.setFormatter(formatter)
    logger.addHandler(ch)

    # File handler
    fh = logging.FileHandler(log_file)
    fh.setFormatter(formatter)
    logger.addHandler(fh)

    return logger

def safe_float(value, default=0.0):
    """
    Convert value to float, or return default on failure.
    """
    try:
        return float(value)
    except (ValueError, TypeError):
        return default

def ensure_dir_exists(path):
    """
    Ensure the directory exists, create if missing.
    """
    if not os.path.exists(path):
        os.makedirs(path)

def timestamp():
    """
    Return current timestamp string.
    """
    from datetime import datetime
    return datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')
