import time
import logging

class TradeExecutor:
    def __init__(self, core):
        self.core = core
        self.logger = logging.getLogger(__name__)
        self.running = True

    def execute_trade(self, pair, side, volume, price=None):
        """
        Executes a trade on Kraken.
        :param pair: Trading pair string e.g. 'XBTUSD'
        :param side: 'buy' or 'sell'
        :param volume: Amount to trade
        :param price: Optional limit price, else None for market
        :return: Trade result or None
        """
        try:
            order_type = 'limit' if price else 'market'
            order_params = {
                'pair': pair,
                'type': side,
                'ordertype': order_type,
                'volume': volume,
            }
            if price:
                order_params['price'] = price

            self.logger.info(f"Placing {side} order: {order_params}")
            response = self.core.kraken.api.query_private('AddOrder', order_params)

            if response.get('error'):
                self.logger.error(f"Order error: {response['error']}")
                return None
            else:
                self.logger.info(f"Order placed: {response['result']}")
                return response['result']

        except Exception as e:
            self.logger.exception(f"Exception while placing order: {e}")
            return None

    def run(self):
        """
        Main loop to execute trades based on signals
        """
        self.logger.info("TradeExecutor started")
        while self.running:
            try:
                signals = self.core.get_trade_signals()
                for signal in signals:
                    pair = signal['pair']
                    side = signal['side']
                    volume = signal['volume']
                    price = signal.get('price')
                    self.execute_trade(pair, side, volume, price)

                time.sleep(self.core.config.get('trade_interval', 60))
            except Exception as e:
                self.logger.exception(f"Exception in trade loop: {e}")
                time.sleep(10)

    def stop(self):
        self.running = False
