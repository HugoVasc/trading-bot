# Trading Bot - Simulation System

A complete trading simulation system with support for multiple strategies, currencies, and performance metrics.

## 🚀 Features

### Simulation System
- **Configurable initial balance** (default: $1,000)
- **Configurable buy percentage** (default: 50% of balance)
- **Realistic transaction fee** (default: 0.1%)
- **Full position tracking** and trade history
- **Automatic calculation** of performance metrics

### Calculated Metrics
- Total final balance
- Absolute and percentage profit/loss
- Total number of trades
- Win rate
- Sharpe Ratio
- Maximum drawdown
- Annualized return

### Data Export
- **Trades CSV**: Detailed history of all operations
- **Metrics CSV**: Performance summary
- **Automatic naming**: `{Strategy}_{Currency}_{Type}_{Timestamp}.csv`

## 📁 Project Structure

```
trading-bot/
├── fetchers/ # Market data fetchers
│ ├── binance_fetchers.py
│ └── interface.py
├── strategies/ # Trading strategies
│ ├── context.py # SandBoxTradingContext (SIMULATION)
│ ├── interface.py # Base interfaces
│ └── strategies.py # Strategy implementations
├── data/ # Generated CSV files (created automatically)
├── main.py # Comparison of multiple strategies
├── exemplo_uso.py # Usage examples
└── requirements.txt # Dependencies
```


## 🛠️ Installation

1. Clone the repository:
```bash
git clone <your-repository>
cd trading-bot
```

2. Install the dependencies:
```bash
pip install -r requirements.txt
```

## 📊 Basic Usage

### Simple Example

```python
from fetchers.binance_fetchers import BinancePriceFetcher
from strategies.strategies import SimpleMovingAverageStrategy
from strategies.context import SandBoxTradingContext

# Initialize
price_fetcher = BinancePriceFetcher()
strategy = SimpleMovingAverageStrategy(short_window=10, long_window=20)

# Configure simulation
context = SandBoxTradingContext(
    strategy=strategy,
    price_fetcher=price_fetcher,
    symbol="BTC/USDT",
    timeframe="4h",
    limit=200,
    initial_cash=1000.0,      # $1000 initial
    buy_percentage=0.5,       # 50% per trade
    transaction_fee=0.001     # 0.1% fee
)

# Run simulation
results = context.run()

# View summary
context.print_summary()

# Export results
files = context.export_results("./data")
```

### Strategy Comparison

Run the main script to compare multiple strategies:

```bash
python main.py
```

This will:
- Test 3 different strategies (Fast, Medium, and Slow SMA)
- On 3 currencies (BTC/USDT, ETH/USDT, ADA/USDT)
- With 2 timeframes (4h, 12h)
- Generate CSV files with all results
- Show a ranking of the best performances

### Detailed Examples

```bash
python exemplo_uso.py
```

## ⚙️ Configuration Parameters

### SandBoxTradingContext

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `initial_cash` | float | 1000.0 | Initial balance in USD |
| `buy_percentage` | float | 0.5 | Percentage of balance for each buy (0.0-1.0) |
| `transaction_fee` | float | 0.001 | Transaction fee (0.1% = 0.001) |
| `timeframe` | str | "1h" | Data timeframe (1m, 5m, 1h, 4h, 1d, etc.) |
| `limit` | int | 100 | Number of candles to fetch |
| `verbose` | bool | False | Show detailed logs |

### Available Strategies

#### SimpleMovingAverageStrategy
- `short_window`: Short moving average window (default: 3)
- `long_window`: Long moving average window (default: 5)

## 📈 Performance Metrics

### Basic Metrics
- **Final Balance**: Total portfolio value at the end
- **Total Return**: Profit/loss in absolute value
- **Return %**: Profit/loss as a percentage
- **Total Trades**: Number of operations executed

### Advanced Metrics
- **Win Rate**: Percentage of profitable trades
- **Sharpe Ratio**: Risk-adjusted return
- **Maximum Drawdown**: Largest percentage drop from peak
- **Annualized Return**: Annual projection based on the period

## 📁 Generated Files

### Trades CSV
Contains every operation executed:
- timestamp, action, price, quantity, value, fee
- cash_after, position_after

### Metrics CSV
Performance summary:
- All calculated metrics
- Parameters used in the simulation

### Naming
- `SimpleMovingAverage_BTCUSDT_trades_20250118_143022.csv`
- `SimpleMovingAverage_BTCUSDT_metrics_20250118_143022.csv`

## 🔧 Developing New Strategies

1. Inherit from the `Strategy` class:

```python
from strategies.interface import Strategy

class MyStrategy(Strategy):
    def __init__(self, parameter1, parameter2):
        self.parameter1 = parameter1
        self.parameter2 = parameter2
        # Initialize strategy state
    
    def reset(self):
        """Reset state for a new simulation"""
        # Clear history, counters, etc.
        pass
    
    def decide(self, candle):
        """Decision logic based on the candle"""
        # Analyze candle
        # Return: {"action": "buy"|"sell"|"hold", ...}
        return {**candle, "action": "hold"}
```

2. Use with SandBoxTradingContext:

```python
my_strategy = MyStrategy(parameter1=10, parameter2=20)
context = SandBoxTradingContext(my_strategy, price_fetcher, "BTC/USDT")
```

## 🎯 Usage Examples

### Quick Test
```bash
python exemplo_uso.py
```

### Full Comparison
```bash
python main.py
```

### Programmatic Usage
```python
# See exemplo_uso.py for detailed examples
```

## 📊 Interpreting Results

### Positive Return
- Profitable strategy in the tested period
- Check consistency across different currencies/timeframes

### High Win Rate
- Strategy gets many operations right
- May indicate a conservative strategy

### High Sharpe Ratio
- Good risk/return ratio
- More stable strategy

### Low Drawdown
- Lower risk of large losses
- More defensive strategy

## ⚠️ Important Warnings

1. **Simulation vs. Reality**: Past results do not guarantee future performance
2. **Real Fees**: Check the exchange's actual fees before live trading
3. **Slippage**: The simulation does not account for market slippage
4. **Liquidity**: Low-liquidity markets may behave differently

## 🤝 Contributing

1. Fork the project
2. Create a branch for your feature
3. Implement your strategy or improvement
4. Test with different configurations
5. Submit a pull request

## 📝 License

See the LICENSE file for details.
