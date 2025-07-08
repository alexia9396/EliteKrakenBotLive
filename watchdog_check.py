import os
import time
import subprocess
import logging

logging.basicConfig(level=logging.INFO)

BOT_SCRIPT = "main.py"
HEARTBEAT_LOG = "logs/heartbeat.log"
RESTART_DELAY = 10  # seconds

def is_bot_running():
    try:
        output = subprocess.check_output(["pgrep", "-f", BOT_SCRIPT])
        return bool(output.strip())
    except subprocess.CalledProcessError:
        return False

def start_bot():
    logging.info("🟢 Starting the bot...")
    subprocess.Popen(["python3", BOT_SCRIPT])

def monitor_bot():
    while True:
        if not is_bot_running():
            logging.warning("⚠️ Bot not running, restarting...")
            start_bot()
        time.sleep(RESTART_DELAY)

if __name__ == "__main__":
    logging.info("🔍 Watchdog monitor started.")
    monitor_bot()
