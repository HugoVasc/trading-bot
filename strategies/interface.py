from abc import ABC, abstractmethod
from typing import Dict, Any


class Strategy(ABC):
    @abstractmethod
    def decide(self, candle: Dict[str, Any]) -> Dict[str, Any]:
        """
        Decide the action based on the current market candle.
        Returns dict: {"action": "Buy" | "Hold" | "Sell", "timestamp": ...}
        """
        pass
    
    def reset(self):
        """
        Reset the strategy state. Override this method if the strategy maintains state.
        This is called before each simulation run.
        """
        pass

class TradingContext(ABC):
    @abstractmethod
    def __init__(self, strategy: Strategy):
        self.strategy = strategy
        pass
    
    @abstractmethod
    def run(self) -> Any:
        """
        Run the trading context, executing the strategy on incoming market data.
        """
        pass