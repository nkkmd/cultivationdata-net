import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

class Portfolio:
    def __init__(self, initial_balance, target_allocations):
        self.initial_balance = initial_balance
        self.target_allocations = target_allocations
        self.holdings = {asset: initial_balance * allocation for asset, allocation in target_allocations.items()}
        self.asset_values = {asset: [] for asset in target_allocations.keys()}

    def rebalance(self, current_prices):
        total_value = sum(self.holdings[asset] * price for asset, price in current_prices.items())
        for asset, target_allocation in self.target_allocations.items():
            target_value = total_value * target_allocation
            current_value = self.holdings[asset] * current_prices[asset]
            shares_adjustment = (target_value - current_value) / current_prices[asset]
            self.holdings[asset] += shares_adjustment

    def update_value(self, current_prices):
        for asset in self.holdings:
            value = self.holdings[asset] * current_prices[asset]
            self.asset_values[asset].append(value)
        return sum(self.asset_values[asset][-1] for asset in self.asset_values)

def get_historical_data(tickers, start_date, end_date):
    data = yf.download(tickers, start=start_date, end=end_date)['Adj Close']
    return data

def run_simulation(initial_balance, target_allocations, historical_data, rebalance_frequency):
    portfolio = Portfolio(initial_balance, target_allocations)
    portfolio_values = []

    for date, prices in historical_data.iterrows():
        current_prices = prices.to_dict()
        
        if rebalance_frequency > 0 and len(portfolio_values) % rebalance_frequency == 0:
            portfolio.rebalance(current_prices)
        
        portfolio_value = portfolio.update_value(current_prices)
        portfolio_values.append(portfolio_value)

    return portfolio, portfolio_values

def plot_comparison(dates, rebalanced_values, non_rebalanced_values):
    plt.figure(figsize=(12, 6))
    plt.plot(dates, rebalanced_values, label='Rebalanced Portfolio')
    plt.plot(dates, non_rebalanced_values, label='Non-rebalanced Portfolio')
    plt.title('Rebalanced vs Non-rebalanced Portfolio Performance')
    plt.xlabel('Date')
    plt.ylabel('Portfolio Value ($)')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

def calculate_performance(portfolio_values, risk_free_rate):
    total_return = (portfolio_values[-1] / portfolio_values[0] - 1) * 100
    annual_return = ((portfolio_values[-1] / portfolio_values[0]) ** (252 / len(portfolio_values)) - 1) * 100
    daily_returns = [portfolio_values[i] / portfolio_values[i-1] - 1 for i in range(1, len(portfolio_values))]
    
    # シャープレシオの計算
    daily_risk_free_rate = (1 + risk_free_rate) ** (1/252) - 1
    excess_returns = [r - daily_risk_free_rate for r in daily_returns]
    sharpe_ratio = np.sqrt(252) * np.mean(excess_returns) / np.std(excess_returns)
    
    # 最大ドローダウンの計算
    cumulative_returns = np.cumprod(1 + np.array(daily_returns))
    peak = np.maximum.accumulate(cumulative_returns)
    drawdowns = (peak - cumulative_returns) / peak
    max_drawdown = np.max(drawdowns) * 100

    return total_return, annual_return, sharpe_ratio, max_drawdown

# シミュレーション設定
initial_balance = 10000
target_allocations = {
    "SPY": 0.6,  # S&P 500 ETF
    "AGG": 0.3,  # 債券ETF
    "GLD": 0.1   # 金ETF
}
start_date = "2020-01-01"
end_date = "2023-12-31"
rebalance_frequency = 30  # 30営業日ごとにリバランス
risk_free_rate = 0.02  # 2%の年間リスクフリーレートを設定（ユーザーが変更可能）

# データ取得
historical_data = get_historical_data(list(target_allocations.keys()), start_date, end_date)

# リバランスありのシミュレーション
rebalanced_portfolio, rebalanced_values = run_simulation(initial_balance, target_allocations, historical_data, rebalance_frequency)

# リバランスなしのシミュレーション
non_rebalanced_portfolio, non_rebalanced_values = run_simulation(initial_balance, target_allocations, historical_data, 0)

# 結果表示
print(f"\n期間: {start_date} から {end_date}")
print(f"初期投資額: ${initial_balance:.2f}")
print(f"リスクフリーレート: {risk_free_rate:.2%}")

rebalanced_return, rebalanced_annual, rebalanced_sharpe, rebalanced_max_drawdown = calculate_performance(rebalanced_values, risk_free_rate)
non_rebalanced_return, non_rebalanced_annual, non_rebalanced_sharpe, non_rebalanced_max_drawdown = calculate_performance(non_rebalanced_values, risk_free_rate)

print("\nリバランスあり:")
print(f"最終ポートフォリオ価値: ${rebalanced_values[-1]:.2f}")
print(f"総収益率: {rebalanced_return:.2f}%")
print(f"年間収益率: {rebalanced_annual:.2f}%")
print(f"シャープレシオ: {rebalanced_sharpe:.2f}")
print(f"最大ドローダウン: {rebalanced_max_drawdown:.2f}%")

print("\nリバランスなし:")
print(f"最終ポートフォリオ価値: ${non_rebalanced_values[-1]:.2f}")
print(f"総収益率: {non_rebalanced_return:.2f}%")
print(f"年間収益率: {non_rebalanced_annual:.2f}%")
print(f"シャープレシオ: {non_rebalanced_sharpe:.2f}")
print(f"最大ドローダウン: {non_rebalanced_max_drawdown:.2f}%")

# グラフ描画
plot_comparison(historical_data.index, rebalanced_values, non_rebalanced_values)