import logging
from bot.core import Core
from bot.trade_executor import TradeExecutor
from krakenex import API  # Make sure you have krakenex installed

logging.basicConfig(level=logging.INFO)

def main():
    # Initialize Kraken API client
    kraken_api = API()
    # Load your Kraken API key/secret here
    # You can also set them manually like this:
    # kraken_api.key = 'your_api_key_here'
    # kraken_api.secret = 'your_api_secret_here'
    kraken_api.load_key('kraken.key')  # Or use your preferred way

    # Initialize core bot with Kraken API client
    core = Core(kraken_api)
    
    # Initialize trade executor and assign to core
    trade_executor = TradeExecutor(core)
    core.executor = trade_executor
    
    # Start the main bot loop
    core.run()

if __name__ == "__main__":
    main()
