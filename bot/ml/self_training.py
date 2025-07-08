import json
import os
from statistics import mean
from bot.utils.logger import setup_logger

logger = setup_logger("SelfTraining")

DATA_FILE = "trade_history.json"
PERFORMANCE_FILE = "performance_metrics.json"

def record_trade_result(pair, profit_pct, confidence_score):
    """Save the outcome of each trade for adaptive training."""
    entry = {
        "pair": pair,
        "profit_pct": profit_pct,
        "confidence": confidence_score
    }

    data = []
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            try:
                data = json.load(f)
            except Exception:
                logger.warning("Could not parse trade history file. Starting fresh.")

    data.append(entry)

    with open(DATA_FILE, "w") as f:
        json.dump(data[-500:], f, indent=2)  # Keep last 500 trades

    logger.info(f"✅ Trade recorded: {pair}, profit={profit_pct}%, confidence={confidence_score}")

def adjust_confidence_threshold(current_threshold, goal_profit_pct=1.0):
    """Adjusts the confidence threshold based on recent performance."""
    if not os.path.exists(DATA_FILE):
        return current_threshold

    try:
        with open(DATA_FILE, "r") as f:
            data = json.load(f)
            recent = data[-50:]
    except Exception:
        logger.warning("Failed to load trade history for self-training.")
        return current_threshold

    avg_profit = mean([entry["profit_pct"] for entry in recent if "profit_pct" in entry])
    logger.info(f"📊 Avg recent profit: {avg_profit:.2f}%")

    if avg_profit > goal_profit_pct:
        current_threshold = min(current_threshold + 0.01, 0.95)
    else:
        current_threshold = max(current_threshold - 0.01, 0.60)

    logger.info(f"🎯 Updated confidence threshold: {current_threshold:.2f}")

    # Save for monitoring
    with open(PERFORMANCE_FILE, "w") as f:
        json.dump({"confidence_threshold": current_threshold, "avg_profit": avg_profit}, f, indent=2)

    return round(current_threshold, 2)
