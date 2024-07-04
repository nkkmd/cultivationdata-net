import numpy as np
import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt
from scipy.stats import norm

def get_stock_data(tickers, start_date, end_date):
    data = yf.download(tickers, start=start_date, end=end_date)['Adj Close']
    return data

def calculate_portfolio_returns(data, weights):
    returns = data.pct_change()
    portfolio_returns = returns.dot(weights)
    return portfolio_returns

def monte_carlo_simulation(initial_investment, years, num_simulations, expected_return, volatility):
    daily_returns = np.random.normal(expected_return/252, volatility/np.sqrt(252), (252*years, num_simulations))
    cumulative_returns = np.cumprod(1 + daily_returns, axis=0)
    final_values = initial_investment * cumulative_returns[-1]
    return cumulative_returns, final_values

# Portfolio configuration
portfolio = {
    'VT': 0.7,
    'EDV': 0.2,
    'GLDM': 0.1
}

# Data retrieval
start_date = '2015-01-01'
end_date = '2023-12-31'
tickers = list(portfolio.keys())
weights = list(portfolio.values())

stock_data = get_stock_data(tickers, start_date, end_date)

# Calculate portfolio returns
portfolio_returns = calculate_portfolio_returns(stock_data, weights)

# Calculate expected return and volatility based on historical data
expected_return = portfolio_returns.mean() * 252  # Annualized return
volatility = portfolio_returns.std() * np.sqrt(252)  # Annualized volatility

# Simulation parameters
initial_investment = 10000  # Initial investment ($10,000)
years = 10  # Simulation period (years)
num_simulations = 1000  # Number of simulations

# Run simulation
cumulative_returns, final_values = monte_carlo_simulation(initial_investment, years, num_simulations, expected_return, volatility)

# Visualize results
plt.figure(figsize=(12, 7))
plt.plot(cumulative_returns)
portfolio_str = ', '.join([f'{ticker}: {weight:.1%}' for ticker, weight in portfolio.items()])
plt.title(f'Monte Carlo Simulation of Portfolio Value\nPortfolio: {portfolio_str}\nSimulation Period: {years} years', fontsize=14)
plt.xlabel('Days', fontsize=12)
plt.ylabel('Cumulative Return', fontsize=12)
plt.show()

# Calculate and display statistics
mean_final_value = np.mean(final_values)
median_final_value = np.median(final_values)
min_final_value = np.min(final_values)
max_final_value = np.max(final_values)

print(f"平均最終ポートフォリオ価値: ${mean_final_value:,.2f}")
print(f"中央値最終ポートフォリオ価値: ${median_final_value:,.2f}")
print(f"最小最終ポートフォリオ価値: ${min_final_value:,.2f}")
print(f"最大最終ポートフォリオ価値: ${max_final_value:,.2f}")

# Calculate confidence interval
confidence_interval = np.percentile(final_values, [5, 95])
print(f"90%信頼区間: ${confidence_interval[0]:,.2f} - ${confidence_interval[1]:,.2f}")

# Calculate Value at Risk (VaR)
var_95 = norm.ppf(0.05, mean_final_value, np.std(final_values))
print(f"95% VaR: ${initial_investment - var_95:,.2f}")