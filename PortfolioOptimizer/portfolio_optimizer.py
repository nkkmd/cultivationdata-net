# PortfolioOptimizer
# 
# このプログラムは効率的フロンティアを計算し、最適なポートフォリオ配分を提示します。
# 接点ポートフォリオと最小分散ポートフォリオを特定し、
# 結果をグラフィカルに表示します。
# このプログラムは情報提供のみを目的としており、取引や投資のアドバイスには使用しないでください。

import numpy as np
import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt
from scipy.optimize import minimize

def get_data(tickers, start_date, end_date):
    data = yf.download(tickers, start=start_date, end=end_date)['Adj Close']
    returns = data.pct_change().dropna()
    return returns

def portfolio_annualized_performance(weights, mean_returns, cov_matrix):
    returns = np.sum(mean_returns * weights) * 252
    std = np.sqrt(np.dot(weights.T, np.dot(cov_matrix, weights))) * np.sqrt(252)
    return std, returns

def negative_sharpe_ratio(weights, mean_returns, cov_matrix, risk_free_rate):
    p_var, p_ret = portfolio_annualized_performance(weights, mean_returns, cov_matrix)
    return -(p_ret - risk_free_rate) / p_var

def tangency_portfolio(mean_returns, cov_matrix, risk_free_rate):
    num_assets = len(mean_returns)
    args = (mean_returns, cov_matrix, risk_free_rate)
    constraints = ({'type': 'eq', 'fun': lambda x: np.sum(x) - 1})
    bound = (0.0, 1.0)
    bounds = tuple(bound for asset in range(num_assets))
    result = minimize(negative_sharpe_ratio, num_assets*[1./num_assets,], args=args,
                      method='SLSQP', bounds=bounds, constraints=constraints)
    return result

def portfolio_volatility(weights, mean_returns, cov_matrix):
    return portfolio_annualized_performance(weights, mean_returns, cov_matrix)[0]

def min_variance_portfolio(mean_returns, cov_matrix):
    num_assets = len(mean_returns)
    args = (mean_returns, cov_matrix)
    constraints = ({'type': 'eq', 'fun': lambda x: np.sum(x) - 1})
    bound = (0.0, 1.0)
    bounds = tuple(bound for asset in range(num_assets))
    result = minimize(portfolio_volatility, num_assets*[1./num_assets,], args=args,
                      method='SLSQP', bounds=bounds, constraints=constraints)
    return result

def efficient_frontier(mean_returns, cov_matrix, returns_range):
    efficients = []
    for ret in returns_range:
        constraints = ({'type': 'eq', 'fun': lambda x: portfolio_annualized_performance(x, mean_returns, cov_matrix)[1] - ret},
                       {'type': 'eq', 'fun': lambda x: np.sum(x) - 1})
        result = minimize(portfolio_volatility, len(mean_returns)*[1./len(mean_returns),], args=(mean_returns, cov_matrix),
                          method='SLSQP', bounds=tuple((0,1) for _ in range(len(mean_returns))), constraints=constraints)
        efficients.append(result['fun'])
    return efficients

def display_efficient_frontier(mean_returns, cov_matrix, num_portfolios, risk_free_rate, tickers, start_date, end_date):
    returns = []
    volatilities = []
    for _ in range(num_portfolios):
        weights = np.random.random(len(mean_returns))
        weights /= np.sum(weights)
        returns.append(np.sum(mean_returns * weights) * 252)
        volatilities.append(np.sqrt(np.dot(weights.T, np.dot(cov_matrix, weights))) * np.sqrt(252))
    
    max_sharpe = tangency_portfolio(mean_returns, cov_matrix, risk_free_rate)
    sdp, rp = portfolio_annualized_performance(max_sharpe['x'], mean_returns, cov_matrix)
    max_sharpe_allocation = pd.DataFrame(max_sharpe['x'], index=mean_returns.index, columns=['allocation'])
    max_sharpe_allocation.allocation = [round(i*100,2)for i in max_sharpe_allocation.allocation]
    max_sharpe_allocation = max_sharpe_allocation.T
    
    min_vari = min_variance_portfolio(mean_returns, cov_matrix)
    sdp_min, rp_min = portfolio_annualized_performance(min_vari['x'], mean_returns, cov_matrix)
    min_vari_allocation = pd.DataFrame(min_vari['x'], index=mean_returns.index, columns=['allocation'])
    min_vari_allocation.allocation = [round(i*100,2)for i in min_vari_allocation.allocation]
    min_vari_allocation = min_vari_allocation.T
    
    print("-"*80)
    print("Tangency Portfolio Allocation\n")
    print("Annualized Return: {:.2f}%".format(rp * 100))
    print("Annualized Volatility: {:.2f}%".format(sdp * 100))
    print("Sharpe Ratio: {:.2f}".format((rp - risk_free_rate) / sdp))
    print("\n")
    print(max_sharpe_allocation)
    print("-"*80)
    print("Minimum Variance Portfolio Allocation\n")
    print("Annualized Return: {:.2f}%".format(rp_min * 100))
    print("Annualized Volatility: {:.2f}%".format(sdp_min * 100))
    print("Sharpe Ratio: {:.2f}".format((rp_min - risk_free_rate) / sdp_min))
    print("\n")
    print(min_vari_allocation)
    
    plt.figure(figsize=(12, 8))
    scatter = plt.scatter(volatilities, returns, c=(np.array(returns)-risk_free_rate)/np.array(volatilities), cmap='YlGnBu', marker='o', s=10, alpha=0.3)
    plt.colorbar(scatter, label='Sharpe Ratio')
    plt.scatter(sdp, rp, marker='*', color='r', s=500, label='Tangency Portfolio')
    plt.scatter(sdp_min, rp_min, marker='*', color='g', s=500, label='Minimum Variance Portfolio')
    
    target = np.linspace(rp_min, max(returns), 50)
    efficient_portfolios = efficient_frontier(mean_returns, cov_matrix, target)
    plt.plot(efficient_portfolios, target, linestyle='-.', color='black', label='Efficient Frontier')
    plt.title('Portfolio Optimization with the Efficient Frontier')
    plt.xlabel('Annualized Volatility')
    plt.ylabel('Annualized Returns')
    plt.legend(labelspacing=0.8)
    
    # Add text box with additional information
    info_text = f"Tickers: {', '.join(tickers)}\n"
    info_text += f"Period: {start_date} to {end_date}\n"
    info_text += f"Risk-free Rate: {risk_free_rate:.2%}"
    plt.text(0.05, 0.05, info_text, transform=plt.gca().transAxes, 
             bbox=dict(facecolor='white', alpha=0.8), fontsize=9)
    
    plt.tight_layout()
    plt.show()

# メイン処理
tickers = ['VT', 'EDV', 'GLDM']  # ティッカーシンボル
start_date = '2023-01-01'
end_date = '2023-12-31'
risk_free_rate = 0.01  # 1%と仮定

# データの取得
returns = get_data(tickers, start_date, end_date)

# 平均リターンと共分散行列の計算
mean_returns = returns.mean()
cov_matrix = returns.cov()

# 効率的フロンティアの表示
display_efficient_frontier(mean_returns, cov_matrix, num_portfolios=25000, risk_free_rate=risk_free_rate,
                           tickers=tickers, start_date=start_date, end_date=end_date)