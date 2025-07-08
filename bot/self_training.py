import json
import os
import logging
from datetime import datetime

class SelfTraining:
    def __init__(self, log_dir='bot/ml/training_logs', logger=None):
        self.log_dir = log_dir
        self.logger = logger or logging.getLogger(__name__)
        os.makedirs(self.log_dir, exist_ok=True)
        self.performance_file = os.path.join(self.log_dir, 'performance.json')

    def load_performance(self):
        if os.path.exists(self.performance_file):
            try:
                with open(self.performance_file, 'r') as f:
                    return json.load(f)
            except Exception as e:
                self.logger.error(f"Error loading performance data: {e}")
        return {}

    def save_performance(self, performance_data):
        try:
            with open(self.performance_file, 'w') as f:
                json.dump(performance_data, f, indent=4)
            self.logger.info("Performance data saved successfully.")
        except Exception as e:
            self.logger.error(f"Failed to save performance data: {e}")

    def record_trade_result(self, trade_id, result):
        performance = self.load_performance()
        performance[trade_id] = result
        self.save_performance(performance)

    def evaluate_performance(self):
        performance = self.load_performance()
        if not performance:
            self.logger.warning("No performance data to evaluate.")
            return None

        total_trades = len(performance)
        wins = sum(1 for r in performance.values() if r.get('profit', 0) > 0)
        losses = total_trades - wins
        win_rate = wins / total_trades if total_trades > 0 else 0
        avg_profit = sum(r.get('profit', 0) for r in performance.values()) / total_trades

        self.logger.info(f"Total trades: {total_trades}, Wins: {wins}, Losses: {losses}, Win rate: {win_rate:.2%}, Avg profit: {avg_profit:.6f}")

        # Example of simple threshold-based reinforcement trigger
        if win_rate < 0.5:
            self.logger.warning("Performance below threshold, recommend adjusting strategy.")
            return False
        return True

    def update_strategy(self):
        # Placeholder for reinforcement learning or ML model update logic
        self.logger.info("Updating strategy based on performance data...")
        # Add your ML model training and adjustment here

    def run_training_cycle(self):
        if self.evaluate_performance():
            self.logger.info("Performance satisfactory. Continuing current strategy.")
        else:
            self.update_strategy()
