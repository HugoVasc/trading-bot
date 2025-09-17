from abc import ABC, abstractmethod
from typing import List, Dict


class MarketFetcher(ABC):
    @abstractmethod
    def fetch_markets(self) -> List[str]:
        """Fetch available markets/symbols from exchange."""
        pass


class PriceFetcher(ABC):
    @abstractmethod
    def fetch_prices(self, symbol: str, timeframe: str = "1h") -> List[Dict]:
        """Fetch price data (OHLCV) for a given symbol."""
        pass

