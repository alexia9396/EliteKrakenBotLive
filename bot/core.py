import time
import logging
from bot.trade_executor import TradeExecutor
from bot.pair_handler import get_valid_pairs
from bot.config import CONFIG

class Core:
    def __init__(self, kraken):
        self.config = CONFIG
        self.kraken = kraken
        self.executor = TradeExecutor(self)
        self.valid_pairs = []
        self.last_pair_check = 0
        self.pair_check_interval = 3600  # Check pairs every hour
        self.last_trade_time = 0
        self.trade_interval = 60  # Run trades every 60 seconds
        self.heartbeat_interval = 300  # Heartbeat every 5 minutes
        self.last_heartbeat = 0

    def heartbeat(self):
        logging.info("💓 Heartbeat: Bot is alive and scanning...")

    def update_valid_pairs(self):
        logging.info("🔄 Updating valid trading pairs...")
        self.valid_pairs = get_valid_pairs(self.kraken)
        self.last_pair_check = time.time()
        logging.info(f"✅ {len(self.valid_pairs)} valid trading pairs found.")

    def get_trade_signals(self):
        # Placeholder for actual trade signal logic
        # Return list of dicts with keys: pair, side, volume, price (optional)
        return []

    def run(self):
        logging.info("🚀 EliteKrakenBotLive Starting main loop...")
        while True:
            now = time.time()

            # Heartbeat log
            if now - self.last_heartbeat >= self.heartbeat_interval:
                self.heartbeat()
                self.last_heartbeat = now

            # Update trading pairs periodically
            if now - self.last_pair_check >= self.pair_check_interval:
                self.update_valid_pairs()

            # Run trade logic
            if now - self.last_trade_time >= self.trade_interval:
                try:
                    signals = self.get_trade_signals()
                    for signal in signals:
                        pair = signal['pair']
                        side = signal['side']
                        volume = signal['volume']
                        price = signal.get('price', None)
                        self.executor.execute_trade(pair, side, volume, price)
                except Exception as e:
                    logging.error(f"❌ Trade execution error: {e}")
                self.last_trade_time = now

            time.sleep(5)
