from .interface import Strategy
from typing import List, Dict, Any

class SimpleMovingAverageStrategy(Strategy):
    def __init__(self, short_window: int = 3, long_window: int = 5):
        self.short_window = short_window
        self.long_window = long_window
        self.history: List[float] = []
        self.last_action = None

    def reset(self):
        """Reset the strategy state for a new simulation."""
        self.history = []
        self.last_action = None

    def decide(self, candle: Dict[str, Any]) -> Dict[str, Any]:
        self.history.append(candle["close"])

        if len(self.history) < self.long_window:
            return {**candle, "action": "hold", "short_avg": None, "long_avg": None}

        short_avg = sum(self.history[-self.short_window:]) / self.short_window
        long_avg = sum(self.history[-self.long_window:]) / self.long_window

        if short_avg > long_avg and self.last_action != "buy":
            action = "buy"
        elif short_avg < long_avg and self.last_action != "sell":
            action = "sell"
        else:
            action = "hold"

        self.last_action = action if action != "hold" else self.last_action

        return {**candle, "action": action, "short_avg": short_avg, "long_avg": long_avg}
