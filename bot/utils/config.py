# ✅ Replace the values below with your own (already done for main.py)
KRAKEN_API_KEY = "your_api_key_here"
KRAKEN_API_SECRET = "your_api_secret_here"

# ✅ Email settings (already inserted by you earlier)
EMAIL_ADDRESS = "your_email_here@gmail.com"
EMAIL_PASSWORD = "your_gmail_app_password_here"

# Default trade settings
DEFAULT_TRADE_USD = 10.00  # 💵 Starting trade size
MAX_TRADE_USD = 1000.00    # 📈 Safety limit cap
BASE_CURRENCY_PRIORITY = ["XXRP", "USDT", "USD", "XBT"]  # 💱 Smart conversion priority
DAILY_PROFIT_GOAL_MULTIPLIER = 2.0  # 📊 Try to double daily
WEEKLY_FALLBACK_MULTIPLIER = 2.0    # 📊 Fallback target for weekly

# Volatility-based dynamic trailing stop
TRAILING_STOP_BASE_PERCENT = 0.02  # 2% base trailing stop
TRAILING_STOP_MAX_PERCENT = 0.08   # Max allowed trailing stop
