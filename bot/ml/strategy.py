import random
import math
from bot.utils.helpers import log

def calculate_rsi(prices, period=14):
    if len(prices) < period + 1:
        return None  # Not enough data

    gains = []
    losses = []

    for i in range(1, period + 1):
        change = prices[i] - prices[i - 1]
        if change > 0:
            gains.append(change)
            losses.append(0)
        else:
            gains.append(0)
            losses.append(abs(change))

    average_gain = sum(gains) / period
    average_loss = sum(losses) / period

    if average_loss == 0:
        return 100

    rs = average_gain / average_loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

def generate_trade_signal(market_data):
    """
    market_data is a dict with:
      - 'prices': list of recent closing prices (floats)
      - 'volume': recent volume (float)
      - 'volatility': recent volatility (float)

    Returns:
      - signal: 'buy', 'sell', or 'hold'
      - confidence: float between 0 and 1
    """
    prices = market_data.get('prices', [])
    if len(prices) < 15:
        log("⚠️ Not enough data for signal generation")
        return 'hold', 0.0

    rsi = calculate_rsi(prices)
    volatility = market_data.get('volatility', 0)
    latest_price = prices[-1]
    prev_price = prices[-2]

    # Basic moonshot logic with adaptive confidence
    if rsi is None:
        return 'hold', 0.0

    if rsi < 30 and latest_price > prev_price:
        signal = 'buy'
        confidence = min(1.0, 0.7 + (30 - rsi) / 70)
    elif rsi > 70 and latest_price < prev_price:
        signal = 'sell'
        confidence = min(1.0, 0.7 + (rsi - 70) / 30)
    else:
        signal = 'hold'
        confidence = 0.1

    # Boost confidence if volatility is moderate to high
    if 0.02 < volatility < 0.1:
        confidence += 0.1
    confidence = min(confidence, 1.0)

    log(f"Signal generated: {signal} with confidence {confidence:.2f}")
    return signal, confidence
