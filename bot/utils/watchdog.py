import os
import time
import logging
from datetime import datetime, timedelta
from bot.utils.logger import setup_logger

watchdog_logger = setup_logger("watchdog")

LAST_HEARTBEAT_FILE = "last_heartbeat.txt"
TIMEOUT_MINUTES = 10  # Adjust this threshold as needed

def update_heartbeat():
    """Write current timestamp to heartbeat file."""
    with open(LAST_HEARTBEAT_FILE, "w") as f:
        f.write(datetime.utcnow().isoformat())
    watchdog_logger.info("Heartbeat updated.")

def check_heartbeat():
    """Checks if last heartbeat is within the allowed timeout."""
    if not os.path.exists(LAST_HEARTBEAT_FILE):
        watchdog_logger.warning("No heartbeat file found.")
        return False

    with open(LAST_HEARTBEAT_FILE, "r") as f:
        try:
            last_beat = datetime.fromisoformat(f.read().strip())
        except ValueError:
            watchdog_logger.error("Invalid heartbeat timestamp format.")
            return False

    elapsed = datetime.utcnow() - last_beat
    if elapsed > timedelta(minutes=TIMEOUT_MINUTES):
        watchdog_logger.error(f"No heartbeat detected in {elapsed}. Bot may be stalled.")
        return False

    watchdog_logger.info(f"Heartbeat OK. Last seen {elapsed} ago.")
    return True
