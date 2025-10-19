from fetchers.binance_fetchers import BinanceMarketFetcher, BinancePriceFetcher
from strategies.strategies import SimpleMovingAverageStrategy
from strategies.context import SandBoxTradingContext
from pandas import DataFrame
import os

def run_simulation(strategy, symbol, timeframe="4h", limit=500, initial_cash=1000, buy_percentage=0.5, transaction_fee=0.001):
    """Executa uma simulação de trading e retorna os resultados."""
    print(f"\n🚀 Iniciando simulação para {symbol} com {strategy.__class__.__name__}")
    print(f"   Saldo inicial: ${initial_cash:,.2f}")
    print(f"   Percentual de compra: {buy_percentage*100:.1f}%")
    print(f"   Taxa de transação: {transaction_fee*100:.3f}%")
    
    context = SandBoxTradingContext(
        strategy=strategy,
        price_fetcher=BPF,
        symbol=symbol,
        timeframe=timeframe,
        limit=limit,
        verbose=False,
        initial_cash=initial_cash,
        buy_percentage=buy_percentage,
        transaction_fee=transaction_fee
    )
    
    results = context.run()
    
    # Imprimir resumo
    context.print_summary()
    
    # Exportar resultados
    files = context.export_results("./data")
    if files["trades_file"]:
        print(f"📊 Trades salvos em: {files['trades_file']}")
    if files["metrics_file"]:
        print(f"📈 Métricas salvas em: {files['metrics_file']}")
    
    return context.calculate_metrics()

def compare_strategies():
    """Compara múltiplas estratégias e moedas."""
    print("="*80)
    print("🤖 SIMULAÇÃO DE TRADING - COMPARAÇÃO DE ESTRATÉGIAS")
    print("="*80)
    
    # Configurações
    symbols = ["BTC/USDT", "ETH/USDT", "ADA/USDT"]
    timeframes = ["4h", "12h"]
    initial_cash = 1000
    buy_percentage = 0.5
    transaction_fee = 0.001
    limit = 500
    
    # Estratégias para testar
    strategies = [
        ("SMA Rápida", SimpleMovingAverageStrategy(short_window=10, long_window=20)),
        ("SMA Média", SimpleMovingAverageStrategy(short_window=20, long_window=50)),
        ("SMA Lenta", SimpleMovingAverageStrategy(short_window=50, long_window=200))
    ]
    
    all_results = []
    
    for strategy_name, strategy in strategies:
        print(f"\n{'='*60}")
        print(f"📊 TESTANDO ESTRATÉGIA: {strategy_name}")
        print(f"{'='*60}")
        
        for symbol in symbols:
            for timeframe in timeframes:
                try:
                    metrics = run_simulation(
                        strategy=strategy,
                        symbol=symbol,
                        timeframe=timeframe,
                        limit=limit,
                        initial_cash=initial_cash,
                        buy_percentage=buy_percentage,
                        transaction_fee=transaction_fee
                    )
                    
                    # Adicionar informações do teste
                    metrics.update({
                        "strategy_name": strategy_name,
                        "symbol": symbol,
                        "timeframe": timeframe
                    })
                    all_results.append(metrics)
                    
                except Exception as e:
                    print(f"❌ Erro ao testar {strategy_name} em {symbol} ({timeframe}): {e}")
    
    # Resumo comparativo
    if all_results:
        print(f"\n{'='*80}")
        print("📊 RESUMO COMPARATIVO - TOP 5 MELHORES PERFORMANCES")
        print(f"{'='*80}")
        
        # Ordenar por retorno percentual
        sorted_results = sorted(all_results, key=lambda x: x.get('return_percentage', 0), reverse=True)
        
        print(f"{'Rank':<4} {'Estratégia':<15} {'Moeda':<10} {'TF':<4} {'Retorno':<10} {'Trades':<7} {'Win Rate':<9} {'Sharpe':<8}")
        print("-" * 80)
        
        for i, result in enumerate(sorted_results[:5], 1):
            print(f"{i:<4} {result.get('strategy_name', 'N/A'):<15} {result.get('symbol', 'N/A'):<10} "
                  f"{result.get('timeframe', 'N/A'):<4} {result.get('return_percentage', 0):>8.2f}% "
                  f"{result.get('total_trades', 0):<7} {result.get('win_rate', 0):>7.1f}% "
                  f"{result.get('sharpe_ratio', 0):>6.3f}")
        
        # Salvar resumo comparativo
        summary_df = DataFrame(all_results)
        summary_file = f"./data/comparison_summary_{len(all_results)}_tests.csv"
        summary_df.to_csv(summary_file, index=False)
        print(f"\n💾 Resumo comparativo salvo em: {summary_file}")

if __name__ == "__main__":
    # Inicializar fetchers
    BMF = BinanceMarketFetcher()
    BPF = BinancePriceFetcher()
    
    # Criar diretório de dados se não existir
    os.makedirs("./data", exist_ok=True)
    
    # Executar comparação
    compare_strategies()
    
    print(f"\n✅ Simulação concluída! Verifique a pasta './data' para os arquivos CSV gerados.")