import time

class MarketAnalyzer:
    def __init__(self, kraken_api):
        self.api = kraken_api

    def get_candles(self, pair, interval, since=None):
        # Fetch OHLC candles for given pair and interval from Kraken
        params = {'pair': pair, 'interval': interval}
        if since:
            params['since'] = since
        response = self.api.query_public('OHLC', params)
        result_key = list(response['result'].keys())[0]
        return response['result'][result_key]

    def analyze_trends(self, pair):
        # Example: Analyze multiple timeframes for trend direction
        timeframes = [1, 5, 15, 60, 240]  # intervals in minutes
        trends = {}
        for tf in timeframes:
            candles = self.get_candles(pair, tf)
            # Simple trend analysis: compare last close with previous close
            if len(candles) < 2:
                trends[tf] = 'unknown'
                continue
            last_close = float(candles[-1][4])
            prev_close = float(candles[-2][4])
            if last_close > prev_close:
                trends[tf] = 'up'
            elif last_close < prev_close:
                trends[tf] = 'down'
            else:
                trends[tf] = 'neutral'
        return trends

    def is_bullish(self, trends):
        # Returns True if majority of timeframes are bullish
        up_count = sum(1 for t in trends.values() if t == 'up')
        return up_count > len(trends) // 2

    def is_bearish(self, trends):
        # Returns True if majority of timeframes are bearish
        down_count = sum(1 for t in trends.values() if t == 'down')
        return down_count > len(trends) // 2
