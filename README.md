# Trading Bot - Sistema de Simulação

Um sistema completo de simulação de trading com suporte a múltiplas estratégias, moedas e métricas de performance.

## 🚀 Funcionalidades

### Sistema de Simulação
- **Saldo inicial parametrizado** (padrão: $1.000)
- **Percentual de compra configurável** (padrão: 50% do saldo)
- **Taxa de transação realista** (padrão: 0.1%)
- **Rastreamento completo de posições** e histórico de trades
- **Cálculo automático de métricas** de performance

### Métricas Calculadas
- Saldo final total
- Lucro/Prejuízo absoluto e percentual
- Número total de trades
- Taxa de vitória (win rate)
- Sharpe Ratio
- Drawdown máximo
- Retorno anualizado

### Exportação de Dados
- **CSV de trades**: Histórico detalhado de todas as operações
- **CSV de métricas**: Resumo de performance
- **Nomenclatura automática**: `{Estratégia}_{Moeda}_{Tipo}_{Timestamp}.csv`

## 📁 Estrutura do Projeto

```
trading-bot/
├── fetchers/           # Fetchers de dados de mercado
│   ├── binance_fetchers.py
│   └── interface.py
├── strategies/         # Estratégias de trading
│   ├── context.py      # SandBoxTradingContext (SIMULAÇÃO)
│   ├── interface.py    # Interfaces base
│   └── strategies.py   # Implementações de estratégias
├── data/              # Arquivos CSV gerados (criado automaticamente)
├── main.py            # Comparação de múltiplas estratégias
├── exemplo_uso.py     # Exemplos de uso
└── requirements.txt   # Dependências
```

## 🛠️ Instalação

1. Clone o repositório:
```bash
git clone <seu-repositorio>
cd trading-bot
```

2. Instale as dependências:
```bash
pip install -r requirements.txt
```

## 📊 Uso Básico

### Exemplo Simples

```python
from fetchers.binance_fetchers import BinancePriceFetcher
from strategies.strategies import SimpleMovingAverageStrategy
from strategies.context import SandBoxTradingContext

# Inicializar
price_fetcher = BinancePriceFetcher()
strategy = SimpleMovingAverageStrategy(short_window=10, long_window=20)

# Configurar simulação
context = SandBoxTradingContext(
    strategy=strategy,
    price_fetcher=price_fetcher,
    symbol="BTC/USDT",
    timeframe="4h",
    limit=200,
    initial_cash=1000.0,      # $1000 inicial
    buy_percentage=0.5,       # 50% por trade
    transaction_fee=0.001     # 0.1% de taxa
)

# Executar simulação
results = context.run()

# Ver resumo
context.print_summary()

# Exportar resultados
files = context.export_results("./data")
```

### Comparação de Estratégias

Execute o script principal para comparar múltiplas estratégias:

```bash
python main.py
```

Isso irá:
- Testar 3 estratégias diferentes (SMA Rápida, Média, Lenta)
- Em 3 moedas (BTC/USDT, ETH/USDT, ADA/USDT)
- Com 2 timeframes (4h, 12h)
- Gerar arquivos CSV com todos os resultados
- Mostrar ranking das melhores performances

### Exemplos Detalhados

```bash
python exemplo_uso.py
```

## ⚙️ Parâmetros de Configuração

### SandBoxTradingContext

| Parâmetro | Tipo | Padrão | Descrição |
|-----------|------|--------|-----------|
| `initial_cash` | float | 1000.0 | Saldo inicial em USD |
| `buy_percentage` | float | 0.5 | Percentual do saldo para cada compra (0.0-1.0) |
| `transaction_fee` | float | 0.001 | Taxa de transação (0.1% = 0.001) |
| `timeframe` | str | "1h" | Timeframe dos dados (1m, 5m, 1h, 4h, 1d, etc.) |
| `limit` | int | 100 | Número de candles para buscar |
| `verbose` | bool | False | Mostrar logs detalhados |

### Estratégias Disponíveis

#### SimpleMovingAverageStrategy
- `short_window`: Janela da média móvel curta (padrão: 3)
- `long_window`: Janela da média móvel longa (padrão: 5)

## 📈 Métricas de Performance

### Métricas Básicas
- **Saldo Final**: Valor total do portfólio ao final
- **Retorno Total**: Lucro/prejuízo em valor absoluto
- **Retorno %**: Lucro/prejuízo em percentual
- **Total de Trades**: Número de operações executadas

### Métricas Avançadas
- **Taxa de Vitória**: Percentual de trades lucrativos
- **Sharpe Ratio**: Retorno ajustado ao risco
- **Drawdown Máximo**: Maior queda percentual do pico
- **Retorno Anualizado**: Projeção anual baseada no período

## 📁 Arquivos Gerados

### CSV de Trades
Contém cada operação executada:
- timestamp, action, price, quantity, value, fee
- cash_after, position_after

### CSV de Métricas
Resumo de performance:
- Todas as métricas calculadas
- Parâmetros utilizados na simulação

### Nomenclatura
- `SimpleMovingAverage_BTCUSDT_trades_20250118_143022.csv`
- `SimpleMovingAverage_BTCUSDT_metrics_20250118_143022.csv`

## 🔧 Desenvolvendo Novas Estratégias

1. Herde da classe `Strategy`:

```python
from strategies.interface import Strategy

class MinhaEstrategia(Strategy):
    def __init__(self, parametro1, parametro2):
        self.parametro1 = parametro1
        self.parametro2 = parametro2
        # Inicializar estado da estratégia
    
    def reset(self):
        """Reset do estado para nova simulação"""
        # Limpar histórico, contadores, etc.
        pass
    
    def decide(self, candle):
        """Lógica de decisão baseada no candle"""
        # Analisar candle
        # Retornar: {"action": "buy"|"sell"|"hold", ...}
        return {**candle, "action": "hold"}
```

2. Use com SandBoxTradingContext:

```python
minha_estrategia = MinhaEstrategia(parametro1=10, parametro2=20)
context = SandBoxTradingContext(minha_estrategia, price_fetcher, "BTC/USDT")
```

## 🎯 Exemplos de Uso

### Teste Rápido
```bash
python exemplo_uso.py
```

### Comparação Completa
```bash
python main.py
```

### Uso Programático
```python
# Ver exemplo_uso.py para exemplos detalhados
```

## 📊 Interpretando Resultados

### Retorno Positivo
- Estratégia lucrativa no período testado
- Verificar consistência em diferentes moedas/timeframes

### Taxa de Vitória Alta
- Estratégia acerta muitas operações
- Pode indicar estratégia conservadora

### Sharpe Ratio Alto
- Boa relação risco/retorno
- Estratégia mais estável

### Drawdown Baixo
- Menor risco de perdas grandes
- Estratégia mais defensiva

## ⚠️ Avisos Importantes

1. **Simulação vs Realidade**: Resultados passados não garantem performance futura
2. **Taxas Reais**: Verifique as taxas reais da exchange antes de trading real
3. **Slippage**: Simulação não considera slippage de mercado
4. **Liquidez**: Mercados com baixa liquidez podem ter comportamento diferente

## 🤝 Contribuindo

1. Fork o projeto
2. Crie uma branch para sua feature
3. Implemente sua estratégia ou melhoria
4. Teste com diferentes configurações
5. Submeta um pull request

## 📝 Licença

Veja o arquivo LICENSE para detalhes.
