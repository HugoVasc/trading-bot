from .interface import Strategy, TradingContext
from typing import List, Dict, Any, Optional
import pandas as pd
from datetime import datetime
import os
import math

class SandBoxTradingContext(TradingContext):
    def __init__(
        self, 
        strategy: Strategy, 
        price_fetcher, 
        symbol: str, 
        timeframe: str = "1h", 
        limit: int = 100, 
        verbose: bool = False,
        initial_cash: float = 1000.0,
        buy_percentage: float = 0.5,
        transaction_fee: float = 0.001
    ):
        """
        Contexto de simulação de trading com saldo inicial.
        
        Args:
            strategy: Estratégia de trading a ser executada
            price_fetcher: Fetcher de preços de mercado
            symbol: Símbolo da moeda (ex: "BTC/USDT")
            timeframe: Timeframe dos dados (ex: "1h", "4h", "1d")
            limit: Número de candles para buscar
            verbose: Se deve imprimir logs detalhados
            initial_cash: Saldo inicial em cash (padrão: $1000)
            buy_percentage: Percentual do saldo para usar em cada compra (0.0-1.0, padrão: 0.5)
            transaction_fee: Taxa de transação (padrão: 0.1% = 0.001)
        """
        self.strategy = strategy
        self.price_fetcher = price_fetcher
        self.symbol = symbol
        self.timeframe = timeframe
        self.limit = limit
        self.verbose = verbose
        
        # Parâmetros de simulação
        self.initial_cash = initial_cash
        self.buy_percentage = max(0.0, min(1.0, buy_percentage))  # Garantir entre 0-100%
        self.transaction_fee = max(0.0, transaction_fee)  # Garantir não negativo
        
        # Estado da simulação
        self.cash = initial_cash
        self.position = 0.0  # Quantidade de moeda possuída
        self.trades_history: List[Dict[str, Any]] = []
        self.portfolio_values: List[float] = []  # Para cálculo de drawdown
        
        # Métricas
        self.total_trades = 0
        self.winning_trades = 0
        self.losing_trades = 0

    def _execute_buy(self, price: float, timestamp: int) -> bool:
        """Executa uma compra se há saldo suficiente."""
        if self.cash <= 0:
            return False
            
        # Calcular valor para compra
        buy_value = self.cash * self.buy_percentage
        fee = buy_value * self.transaction_fee
        net_buy_value = buy_value - fee
        
        if net_buy_value <= 0:
            return False
            
        # Calcular quantidade a comprar
        quantity = net_buy_value / price
        
        # Atualizar estado
        self.cash -= buy_value
        self.position += quantity
        
        # Registrar trade
        trade = {
            "timestamp": timestamp,
            "action": "BUY",
            "price": price,
            "quantity": quantity,
            "value": buy_value,
            "fee": fee,
            "cash_after": self.cash,
            "position_after": self.position
        }
        self.trades_history.append(trade)
        self.total_trades += 1
        
        if self.verbose:
            print(f"BUY: {quantity:.6f} {self.symbol.split('/')[0]} @ ${price:.2f} (Fee: ${fee:.2f})")
            
        return True

    def _execute_sell(self, price: float, timestamp: int) -> bool:
        """Executa uma venda se há posição para vender."""
        if self.position <= 0:
            return False
            
        # Calcular valor da venda
        sell_value = self.position * price
        fee = sell_value * self.transaction_fee
        net_sell_value = sell_value - fee
        
        # Atualizar estado
        self.cash += net_sell_value
        old_position = self.position
        self.position = 0.0
        
        # Registrar trade
        trade = {
            "timestamp": timestamp,
            "action": "SELL",
            "price": price,
            "quantity": old_position,
            "value": sell_value,
            "fee": fee,
            "cash_after": self.cash,
            "position_after": self.position
        }
        self.trades_history.append(trade)
        self.total_trades += 1
        
        if self.verbose:
            print(f"SELL: {old_position:.6f} {self.symbol.split('/')[0]} @ ${price:.2f} (Fee: ${fee:.2f})")
            
        return True

    def _calculate_portfolio_value(self, current_price: float) -> float:
        """Calcula o valor total do portfólio (cash + posição)."""
        return self.cash + (self.position * current_price)

    def run(self) -> List[Dict]:
        """Executa a simulação de trading."""
        candles = self.price_fetcher.fetch_prices(self.symbol, self.timeframe, self.limit)
        actions = []
        
        # Reset da estratégia se tiver método reset
        if hasattr(self.strategy, 'reset'):
            self.strategy.reset()

        for candle in candles:
            decision = self.strategy.decide(candle)
            price = candle["close"]
            timestamp = candle["timestamp"]
            
            # Executar ação baseada na decisão
            if decision["action"].lower() == "buy":
                self._execute_buy(price, timestamp)
            elif decision["action"].lower() == "sell":
                self._execute_sell(price, timestamp)
            # Hold não faz nada
            
            # Calcular valor do portfólio
            portfolio_value = self._calculate_portfolio_value(price)
            self.portfolio_values.append(portfolio_value)
            
            # Adicionar informações de simulação à decisão
            enhanced_decision = {
                **decision,
                "cash": self.cash,
                "position": self.position,
                "portfolio_value": portfolio_value
            }
            actions.append(enhanced_decision)
            
            if self.verbose:
                print(f"Portfolio: ${portfolio_value:.2f} (Cash: ${self.cash:.2f}, Position: {self.position:.6f})")

        return actions

    def calculate_metrics(self) -> Dict[str, Any]:
        """Calcula métricas de performance da simulação."""
        if not self.portfolio_values:
            return {}
            
        final_price = self.portfolio_values[-1] if self.portfolio_values else self.initial_cash
        initial_value = self.initial_cash
        
        # Métricas básicas
        total_return = final_price - initial_value
        return_percentage = (total_return / initial_value) * 100
        
        # Calcular trades vencedores/perdedores
        if len(self.trades_history) >= 2:
            for i in range(1, len(self.trades_history), 2):  # Pares de buy/sell
                if i < len(self.trades_history):
                    buy_trade = self.trades_history[i-1]
                    sell_trade = self.trades_history[i]
                    
                    if sell_trade["action"] == "SELL" and buy_trade["action"] == "BUY":
                        profit = (sell_trade["price"] - buy_trade["price"]) * buy_trade["quantity"]
                        if profit > 0:
                            self.winning_trades += 1
                        else:
                            self.losing_trades += 1
        
        win_rate = (self.winning_trades / max(1, self.winning_trades + self.losing_trades)) * 100
        
        # Sharpe Ratio (simplificado)
        if len(self.portfolio_values) > 1:
            returns = [(self.portfolio_values[i] - self.portfolio_values[i-1]) / self.portfolio_values[i-1] 
                      for i in range(1, len(self.portfolio_values))]
            avg_return = sum(returns) / len(returns)
            std_return = math.sqrt(sum((r - avg_return) ** 2 for r in returns) / len(returns))
            sharpe_ratio = avg_return / std_return if std_return > 0 else 0
        else:
            sharpe_ratio = 0
            
        # Drawdown máximo
        max_drawdown = 0
        peak = self.portfolio_values[0]
        for value in self.portfolio_values:
            if value > peak:
                peak = value
            drawdown = (peak - value) / peak
            max_drawdown = max(max_drawdown, drawdown)
        max_drawdown_percentage = max_drawdown * 100
        
        # Retorno anualizado (assumindo timeframe em horas)
        timeframe_hours = self._get_timeframe_hours()
        total_hours = len(self.portfolio_values) * timeframe_hours
        years = total_hours / (365 * 24)
        annualized_return = ((final_price / initial_value) ** (1 / years) - 1) * 100 if years > 0 else 0
        
        return {
            "initial_cash": initial_value,
            "final_portfolio_value": final_price,
            "total_return": total_return,
            "return_percentage": return_percentage,
            "total_trades": self.total_trades,
            "winning_trades": self.winning_trades,
            "losing_trades": self.losing_trades,
            "win_rate": win_rate,
            "sharpe_ratio": sharpe_ratio,
            "max_drawdown_percentage": max_drawdown_percentage,
            "annualized_return": annualized_return,
            "transaction_fee_used": self.transaction_fee,
            "buy_percentage_used": self.buy_percentage
        }

    def _get_timeframe_hours(self) -> int:
        """Converte timeframe para horas."""
        timeframe_map = {
            "1m": 1/60, "3m": 3/60, "5m": 5/60, "15m": 15/60, "30m": 30/60,
            "1h": 1, "2h": 2, "4h": 4, "6h": 6, "8h": 8, "12h": 12,
            "1d": 24, "3d": 72, "1w": 168, "1M": 720
        }
        return timeframe_map.get(self.timeframe, 1)

    def export_results(self, output_dir: str = "./data") -> Dict[str, str]:
        """Exporta resultados para arquivos CSV."""
        # Criar diretório se não existir
        os.makedirs(output_dir, exist_ok=True)
        
        # Nome base dos arquivos
        strategy_name = self.strategy.__class__.__name__
        symbol_clean = self.symbol.replace("/", "").replace("-", "")
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Exportar trades
        if self.trades_history:
            trades_df = pd.DataFrame(self.trades_history)
            trades_filename = f"{strategy_name}_{symbol_clean}_trades_{timestamp}.csv"
            trades_path = os.path.join(output_dir, trades_filename)
            trades_df.to_csv(trades_path, index=False)
        else:
            trades_path = None
            
        # Exportar métricas
        metrics = self.calculate_metrics()
        if metrics:
            metrics_df = pd.DataFrame([metrics])
            metrics_filename = f"{strategy_name}_{symbol_clean}_metrics_{timestamp}.csv"
            metrics_path = os.path.join(output_dir, metrics_filename)
            metrics_df.to_csv(metrics_path, index=False)
        else:
            metrics_path = None
            
        return {
            "trades_file": trades_path,
            "metrics_file": metrics_path
        }

    def print_summary(self):
        """Imprime resumo das métricas no console."""
        metrics = self.calculate_metrics()
        
        print(f"\n{'='*60}")
        print(f"RESUMO DA SIMULAÇÃO - {self.strategy.__class__.__name__}")
        print(f"Moeda: {self.symbol} | Timeframe: {self.timeframe}")
        print(f"{'='*60}")
        print(f"Saldo Inicial:     ${metrics.get('initial_cash', 0):,.2f}")
        print(f"Saldo Final:       ${metrics.get('final_portfolio_value', 0):,.2f}")
        print(f"Lucro/Prejuízo:    ${metrics.get('total_return', 0):,.2f}")
        print(f"Retorno:           {metrics.get('return_percentage', 0):.2f}%")
        print(f"Total de Trades:   {metrics.get('total_trades', 0)}")
        print(f"Trades Vencedores: {metrics.get('winning_trades', 0)}")
        print(f"Trades Perdedores: {metrics.get('losing_trades', 0)}")
        print(f"Taxa de Vitória:   {metrics.get('win_rate', 0):.2f}%")
        print(f"Sharpe Ratio:      {metrics.get('sharpe_ratio', 0):.4f}")
        print(f"Drawdown Máximo:   {metrics.get('max_drawdown_percentage', 0):.2f}%")
        print(f"Retorno Anualizado: {metrics.get('annualized_return', 0):.2f}%")
        print(f"{'='*60}\n")
