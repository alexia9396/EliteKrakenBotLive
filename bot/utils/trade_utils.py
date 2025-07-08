from decimal import Decimal, ROUND_DOWN
from bot.utils.logger import setup_logger

logger = setup_logger("TradeUtils")

def format_amount(amount, precision):
    """Formats a Decimal amount to the correct precision for Kraken trading."""
    return Decimal(amount).quantize(Decimal(precision), rounding=ROUND_DOWN)

def get_trade_amount(balance, percent=1.0, min_trade=10.0):
    """Returns the amount to trade based on available balance and trade percent."""
    trade_amount = (Decimal(balance) * Decimal(percent)).quantize(Decimal("0.01"))
    return max(trade_amount, Decimal(min_trade))

def calculate_trailing_stop(entry_price, current_price, trail_percent):
    """Determines if trailing stop should trigger."""
    trail_trigger_price = entry_price * (1 + Decimal(trail_percent) / Decimal(100))
    exit_trigger = current_price < trail_trigger_price
    return exit_trigger

def safe_cast(value, default=0.0):
    """Converts to float safely, fallback to default."""
    try:
        return float(value)
    except Exception:
        return default
