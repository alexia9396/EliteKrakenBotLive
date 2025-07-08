import time
import requests
from bot.utils.logger import setup_logger

logger = setup_logger("Conversion")

class AssetConverter:
    def __init__(self, kraken_api):
        self.api = kraken_api
        self.quote_assets = ["USD", "USDT", "EUR", "XBT"]
        self.retry_delay = 3

    def convert(self, from_asset, to_asset, amount):
        try:
            logger.info(f"🔄 Attempting conversion: {amount} {from_asset} ➝ {to_asset}")
            path = self._find_conversion_path(from_asset, to_asset)
            if not path:
                logger.warning(f"No conversion path from {from_asset} to {to_asset}")
                return False

            for i in range(len(path) - 1):
                src = path[i]
                dst = path[i + 1]
                pair = self._format_pair(src, dst)
                logger.info(f"➡️ Converting {src} ➝ {dst} via {pair}")
                self.api.market_sell(pair, amount)
                time.sleep(2)
                amount = self.api.get_balance(dst)
            return True
        except Exception as e:
            logger.error(f"Conversion failed: {e}")
            return False

    def _find_conversion_path(self, from_asset, to_asset):
        if from_asset == to_asset:
            return [from_asset]
        direct = self._pair_exists(from_asset, to_asset)
        if direct:
            return [from_asset, to_asset]
        for mid in self.quote_assets:
            if self._pair_exists(from_asset, mid) and self._pair_exists(mid, to_asset):
                return [from_asset, mid, to_asset]
        for a in self.quote_assets:
            for b in self.quote_assets:
                if self._pair_exists(from_asset, a) and self._pair_exists(a, b) and self._pair_exists(b, to_asset):
                    return [from_asset, a, b, to_asset]
        return None

    def _pair_exists(self, base, quote):
        try:
            pair = self._format_pair(base, quote)
            return pair in self.api.get_tradable_pairs()
        except Exception:
            return False

    def _format_pair(self, base, quote):
        return f"{base}{quote}".upper()
