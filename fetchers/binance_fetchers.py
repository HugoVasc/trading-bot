from .interface import MarketFetcher, PriceFetcher
import ccxt
from typing import List, Dict
from pandas import DataFrame

class BinanceMarketFetcher(MarketFetcher):
    def __init__(self):
        self.exchange = ccxt.binance()

    def fetch_markets(self) -> List[str]:
        markets = self.exchange.load_markets()
        return list(markets.keys())
    

class BinancePriceFetcher(PriceFetcher):

    def __init__(self):
        self.exchange = ccxt.binance()

    def fetch_prices(self, symbol: str, timeframe: str = "1h", limit: int = 100) -> List[Dict]:
        """
        Fetch historical OHLCV data for a given symbol and timeframe.
        Limit: Number of data points to fetch (default is 100, max is 1000)
        Interval	interval value
        seconds	    1s
        minutes	    1m, 3m, 5m, 15m, 30m
        hours	    1h, 2h, 4h, 6h, 8h, 12h
        days	    1d, 3d
        weeks	    1w
        months	    1M
        """
        ohlcv = self.exchange.fetch_ohlcv(symbol, timeframe=timeframe, limit=limit)
        # Estrutura: [timestamp, open, high, low, close, volume]
        data = [
            {
                "timestamp": o[0],
                "open": o[1],
                "high": o[2],
                "low": o[3],
                "close": o[4],
                "volume": o[5],
            }
            for o in ohlcv
        ]
        # return DataFrame(data).set_index('timestamp')
        return data
