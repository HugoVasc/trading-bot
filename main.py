from fetchers.binance_fetchers import BinanceMarketFetcher, BinancePriceFetcher
from strategies.strategies import SimpleMovingAverageStrategy
from strategies.context import SandBoxTradingContext
from pandas import DataFrame

BMF = BinanceMarketFetcher()
BPF = BinancePriceFetcher()
markets = BMF.fetch_markets()

if __name__ == "__main__":

    strategy = SimpleMovingAverageStrategy(short_window=50, long_window=200)
    context = SandBoxTradingContext(strategy, BPF, "BTC/USDT", timeframe="12h", limit=1000)
    results = context.run()
    # Salvar em arquivo CSV
    df = DataFrame(results).set_index('timestamp')
    df.to_csv('./data/results.csv')
    print("Results saved to results.csv")
    print(df)
    # for r in results:
    #     print(r)

    # prices = BPF.fetch_prices("BTC/USDT", "15m", 150)
    # print(prices)