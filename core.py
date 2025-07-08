import time
import logging
from bot.utils.helpers import (
    get_kraken_session, get_balance, analyze_market,
    place_order, send_email_alert, calculate_trade_amount,
    log_trade, perform_conversion_if_needed, fetch_valid_pairs,
    dynamic_trailing_stop
)

logger = logging.getLogger(__name__)

def run_bot():
    logger.info("💓 Heartbeat: Bot is alive and scanning...")

    kraken = get_kraken_session()
    valid_pairs = fetch_valid_pairs(kraken)

    for pair in valid_pairs:
        try:
            logger.info(f"🔍 Checking pair: {pair}")
            signal = analyze_market(kraken, pair)
            if signal['action'] == 'buy':
                balance_info = get_balance(kraken)
                amount = calculate_trade_amount(balance_info, pair)
                if amount > 0:
                    logger.info(f"📈 Buy signal on {pair}, amount: {amount}")
                    order_info = place_order(kraken, pair, amount, 'buy')
                    log_trade(pair, amount, 'buy', order_info)
                    send_email_alert(f"📈 Buy Executed: {pair}", f"Bought {amount} of {pair}")
            elif signal['action'] == 'sell':
                balance_info = get_balance(kraken)
                amount = balance_info.get(pair.split('/')[0], 0)
                if amount > 0:
                    logger.info(f"📉 Sell signal on {pair}, amount: {amount}")
                    order_info = place_order(kraken, pair, amount, 'sell')
                    log_trade(pair, amount, 'sell', order_info)
                    send_email_alert(f"📉 Sell Executed: {pair}", f"Sold {amount} of {pair}")
            else:
                logger.info(f"⚠️ No trade action for {pair}")
        except Exception as e:
            logger.error(f"❌ Error with pair {pair}: {str(e)}")
            continue

    # Fallback conversion and trailing stops
    try:
        perform_conversion_if_needed(kraken)
        dynamic_trailing_stop(kraken)
    except Exception as e:
        logger.error(f"❌ Error in conversion or trailing stop logic: {str(e)}")

if __name__ == '__main__':
    while True:
        run_bot()
        time.sleep(60)  # 🕐 Run every 60 seconds
