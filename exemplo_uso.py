#!/usr/bin/env python3
"""
Exemplo de uso do sistema de simulação de trading.

Este arquivo demonstra como usar o SandBoxTradingContext para simular
trading com diferentes estratégias e parâmetros.
"""

from fetchers.binance_fetchers import BinancePriceFetcher
from strategies.strategies import SimpleMovingAverageStrategy
from strategies.context import SandBoxTradingContext

def exemplo_basico():
    """Exemplo básico de simulação com uma estratégia."""
    print("="*60)
    print("📊 EXEMPLO BÁSICO - SIMULAÇÃO DE TRADING")
    print("="*60)
    
    # Inicializar fetchers
    price_fetcher = BinancePriceFetcher()
    
    # Criar estratégia
    strategy = SimpleMovingAverageStrategy(short_window=10, long_window=20)
    
    # Configurar simulação
    context = SandBoxTradingContext(
        strategy=strategy,
        price_fetcher=price_fetcher,
        symbol="BTC/USDT",
        timeframe="4h",
        limit=200,
        verbose=True,  # Mostrar logs detalhados
        initial_cash=1000.0,  # $1000 inicial
        buy_percentage=0.5,   # Usar 50% do saldo em cada compra
        transaction_fee=0.001 # Taxa de 0.1%
    )
    
    # Executar simulação
    print("🚀 Executando simulação...")
    results = context.run()
    
    # Mostrar resumo
    context.print_summary()
    
    # Exportar resultados
    files = context.export_results("./data")
    print(f"📁 Arquivos salvos:")
    if files["trades_file"]:
        print(f"   - Trades: {files['trades_file']}")
    if files["metrics_file"]:
        print(f"   - Métricas: {files['metrics_file']}")

def exemplo_multiplas_configuracoes():
    """Exemplo com diferentes configurações de parâmetros."""
    print("\n" + "="*60)
    print("🔧 EXEMPLO - DIFERENTES CONFIGURAÇÕES")
    print("="*60)
    
    price_fetcher = BinancePriceFetcher()
    symbol = "ETH/USDT"
    
    # Diferentes configurações para testar
    configuracoes = [
        {
            "nome": "Conservador",
            "initial_cash": 1000,
            "buy_percentage": 0.25,  # 25% por trade
            "transaction_fee": 0.001,
            "strategy": SimpleMovingAverageStrategy(short_window=20, long_window=50)
        },
        {
            "nome": "Moderado", 
            "initial_cash": 1000,
            "buy_percentage": 0.5,   # 50% por trade
            "transaction_fee": 0.001,
            "strategy": SimpleMovingAverageStrategy(short_window=10, long_window=20)
        },
        {
            "nome": "Agressivo",
            "initial_cash": 1000,
            "buy_percentage": 0.8,   # 80% por trade
            "transaction_fee": 0.001,
            "strategy": SimpleMovingAverageStrategy(short_window=5, long_window=10)
        }
    ]
    
    resultados = []
    
    for config in configuracoes:
        print(f"\n🧪 Testando configuração: {config['nome']}")
        print(f"   Saldo inicial: ${config['initial_cash']}")
        print(f"   Percentual de compra: {config['buy_percentage']*100}%")
        print(f"   Estratégia: SMA({config['strategy'].short_window}, {config['strategy'].long_window})")
        
        context = SandBoxTradingContext(
            strategy=config['strategy'],
            price_fetcher=price_fetcher,
            symbol=symbol,
            timeframe="4h",
            limit=150,
            verbose=False,
            initial_cash=config['initial_cash'],
            buy_percentage=config['buy_percentage'],
            transaction_fee=config['transaction_fee']
        )
        
        results = context.run()
        metrics = context.calculate_metrics()
        
        # Adicionar nome da configuração
        metrics['config_name'] = config['nome']
        resultados.append(metrics)
        
        # Mostrar resumo rápido
        print(f"   ✅ Retorno: {metrics.get('return_percentage', 0):.2f}% | "
              f"Trades: {metrics.get('total_trades', 0)} | "
              f"Win Rate: {metrics.get('win_rate', 0):.1f}%")
    
    # Comparar resultados
    print(f"\n📊 COMPARAÇÃO DE CONFIGURAÇÕES:")
    print(f"{'Configuração':<12} {'Retorno':<10} {'Trades':<7} {'Win Rate':<9} {'Sharpe':<8}")
    print("-" * 60)
    
    for resultado in sorted(resultados, key=lambda x: x.get('return_percentage', 0), reverse=True):
        print(f"{resultado.get('config_name', 'N/A'):<12} "
              f"{resultado.get('return_percentage', 0):>8.2f}% "
              f"{resultado.get('total_trades', 0):<7} "
              f"{resultado.get('win_rate', 0):>7.1f}% "
              f"{resultado.get('sharpe_ratio', 0):>6.3f}")

if __name__ == "__main__":
    # Executar exemplos
    exemplo_basico()
    exemplo_multiplas_configuracoes()
    
    print(f"\n✅ Exemplos concluídos!")
    print(f"💡 Dica: Execute 'python main.py' para ver a comparação completa de estratégias.")
