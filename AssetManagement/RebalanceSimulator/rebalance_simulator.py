import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
from enum import Enum

class RebalanceMethod(Enum):
    PERIODIC = 1
    THRESHOLD = 2

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

    def check_threshold(self, current_prices, threshold):
        total_value = sum(self.holdings[asset] * price for asset, price in current_prices.items())
        for asset, target_allocation in self.target_allocations.items():
            current_allocation = (self.holdings[asset] * current_prices[asset]) / total_value
            if abs(current_allocation - target_allocation) > threshold:
                return True
        return False

def get_historical_data(tickers, start_date, end_date):
    data = yf.download(tickers, start=start_date, end=end_date)['Adj Close']
    return data

def run_simulation(initial_balance, target_allocations, historical_data, rebalance_method, rebalance_param):
    portfolio = Portfolio(initial_balance, target_allocations)
    portfolio_values = []
    rebalance_dates = []

    for date, prices in historical_data.iterrows():
        current_prices = prices.to_dict()
        
        should_rebalance = False
        if rebalance_method == RebalanceMethod.PERIODIC:
            if len(portfolio_values) % rebalance_param == 0:
                should_rebalance = True
        elif rebalance_method == RebalanceMethod.THRESHOLD:
            if portfolio.check_threshold(current_prices, rebalance_param):
                should_rebalance = True
        
        if should_rebalance:
            portfolio.rebalance(current_prices)
            rebalance_dates.append(date)
        
        portfolio_value = portfolio.update_value(current_prices)
        portfolio_values.append(portfolio_value)

    return portfolio, portfolio_values, rebalance_dates

def plot_comparison(dates, periodic_values, threshold_values, non_rebalanced_values, periodic_rebalance_dates, threshold_rebalance_dates):
    plt.figure(figsize=(12, 6))
    plt.plot(dates, periodic_values, label='Periodic Rebalancing')
    plt.plot(dates, threshold_values, label='Threshold Rebalancing')
    plt.plot(dates, non_rebalanced_values, label='No Rebalancing')
    
    for date in periodic_rebalance_dates:
        plt.axvline(x=date, color='r', linestyle='--', alpha=0.3)
    
    for date in threshold_rebalance_dates:
        plt.axvline(x=date, color='g', linestyle='--', alpha=0.3)
    
    plt.title('Comparison of Portfolio Rebalancing Strategies')
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
    
    daily_risk_free_rate = (1 + risk_free_rate) ** (1/252) - 1
    excess_returns = [r - daily_risk_free_rate for r in daily_returns]
    sharpe_ratio = np.sqrt(252) * np.mean(excess_returns) / np.std(excess_returns)
    
    cumulative_returns = np.cumprod(1 + np.array(daily_returns))
    peak = np.maximum.accumulate(cumulative_returns)
    drawdowns = (peak - cumulative_returns) / peak
    max_drawdown = np.max(drawdowns) * 100

    return total_return, annual_return, sharpe_ratio, max_drawdown

# ユーザー入力
print("ポートフォリオリバランスシミュレーター")
initial_balance = float(input("初期投資額（$）を入力してください: "))

portfolio = {}
total_weight = 0
while total_weight < 1:
    ticker = input("ETFのティッカーシンボルを入力してください: ").upper()
    weight = float(input(f"{ticker}の比率を入力してください（0-1の間）: "))
    portfolio[ticker] = weight
    total_weight += weight
    print(f"現在の合計比率: {total_weight:.2f}")
    if total_weight >= 1:
        break
    if total_weight < 1:
        print(f"残りの比率: {1 - total_weight:.2f}")

# 合計が1になるように正規化
if total_weight != 1:
    for ticker in portfolio:
        portfolio[ticker] /= total_weight

start_date = input("開始日（YYYY-MM-DD）を入力してください: ")
end_date = input("終了日（YYYY-MM-DD）を入力してください: ")
risk_free_rate = float(input("年間リスクフリーレート（小数）を入力してください: "))
periodic_rebalance_frequency = int(input("定期リバランスの頻度（営業日数）を入力してください: "))
threshold = float(input("閾値リバランスの閾値（小数）を入力してください: "))

# データ取得
historical_data = get_historical_data(list(portfolio.keys()), start_date, end_date)

# シミュレーション実行
periodic_portfolio, periodic_values, periodic_rebalance_dates = run_simulation(
    initial_balance, portfolio, historical_data, RebalanceMethod.PERIODIC, periodic_rebalance_frequency
)

threshold_portfolio, threshold_values, threshold_rebalance_dates = run_simulation(
    initial_balance, portfolio, historical_data, RebalanceMethod.THRESHOLD, threshold
)

non_rebalanced_portfolio, non_rebalanced_values, _ = run_simulation(
    initial_balance, portfolio, historical_data, RebalanceMethod.PERIODIC, len(historical_data)
)

# 結果表示
print(f"\n期間: {start_date} から {end_date}")
print(f"初期投資額: ${initial_balance:,.2f}")
print("ポートフォリオ構成:")
for ticker, weight in portfolio.items():
    print(f"  {ticker}: {weight:.2%}")
print(f"リスクフリーレート: {risk_free_rate:.2%}")

periodic_return, periodic_annual, periodic_sharpe, periodic_max_drawdown = calculate_performance(periodic_values, risk_free_rate)
threshold_return, threshold_annual, threshold_sharpe, threshold_max_drawdown = calculate_performance(threshold_values, risk_free_rate)
non_rebalanced_return, non_rebalanced_annual, non_rebalanced_sharpe, non_rebalanced_max_drawdown = calculate_performance(non_rebalanced_values, risk_free_rate)

print("\n定期リバランス:")
print(f"最終ポートフォリオ価値: ${periodic_values[-1]:,.2f}")
print(f"総収益率: {periodic_return:.2f}%")
print(f"年間収益率: {periodic_annual:.2f}%")
print(f"シャープレシオ: {periodic_sharpe:.2f}")
print(f"最大ドローダウン: {periodic_max_drawdown:.2f}%")
print(f"リバランス回数: {len(periodic_rebalance_dates)}")

print("\n閾値リバランス:")
print(f"最終ポートフォリオ価値: ${threshold_values[-1]:,.2f}")
print(f"総収益率: {threshold_return:.2f}%")
print(f"年間収益率: {threshold_annual:.2f}%")
print(f"シャープレシオ: {threshold_sharpe:.2f}")
print(f"最大ドローダウン: {threshold_max_drawdown:.2f}%")
print(f"リバランス回数: {len(threshold_rebalance_dates)}")

print("\nリバランスなし:")
print(f"最終ポートフォリオ価値: ${non_rebalanced_values[-1]:,.2f}")
print(f"総収益率: {non_rebalanced_return:.2f}%")
print(f"年間収益率: {non_rebalanced_annual:.2f}%")
print(f"シャープレシオ: {non_rebalanced_sharpe:.2f}")
print(f"最大ドローダウン: {non_rebalanced_max_drawdown:.2f}%")

# グラフ描画
plot_comparison(historical_data.index, periodic_values, threshold_values, non_rebalanced_values, periodic_rebalance_dates, threshold_rebalance_dates)