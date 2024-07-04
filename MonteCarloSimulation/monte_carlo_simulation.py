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

def rebalance_portfolio(portfolio_values, target_weights):
    total_value = np.sum(portfolio_values)
    new_values = total_value * target_weights
    return new_values

def monte_carlo_simulation(initial_investment, months, num_simulations, expected_return, volatility, rebalance_months=None):
    days = months * 21  # Assuming 21 trading days per month
    daily_returns = np.random.normal(expected_return/252, volatility/np.sqrt(252), (days, num_simulations))
    cumulative_returns = np.zeros((days, num_simulations))
    
    for sim in range(num_simulations):
        portfolio_value = initial_investment
        for day in range(days):
            if rebalance_months and day % (rebalance_months * 21) == 0 and day > 0:
                portfolio_value = portfolio_value * (1 + daily_returns[day, sim])
            else:
                portfolio_value *= (1 + daily_returns[day, sim])
            cumulative_returns[day, sim] = portfolio_value / initial_investment

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
months = 120  # Simulation period (10 years * 12 months)
num_simulations = 1000  # Number of simulations
rebalance_months = 12  # Rebalance annually

# Run simulation
cumulative_returns, final_values = monte_carlo_simulation(initial_investment, months, num_simulations, expected_return, volatility, rebalance_months)

# Visualize results
plt.figure(figsize=(12, 7))
plt.plot(cumulative_returns)
portfolio_str = ', '.join([f'{ticker}: {weight:.1%}' for ticker, weight in portfolio.items()])
plt.title(f'Monte Carlo Simulation of Portfolio Value\nPortfolio: {portfolio_str}\nSimulation Period: {months} months, Rebalance: Every {rebalance_months} months', fontsize=14)
plt.xlabel('Days', fontsize=12)
plt.ylabel('Cumulative Return', fontsize=12)
plt.show()

# Calculate and display statistics
mean_final_value = np.mean(final_values)
median_final_value = np.median(final_values)
min_final_value = np.min(final_values)
max_final_value = np.max(final_values)

print(f"平均値: ${mean_final_value:,.2f}")
print(f"中央値: ${median_final_value:,.2f}")
print(f"最小値: ${min_final_value:,.2f}")
print(f"最大値: ${max_final_value:,.2f}")

# Calculate confidence interval
confidence_interval = np.percentile(final_values, [5, 95])
print(f"90%信頼区間: ${confidence_interval[0]:,.2f} - ${confidence_interval[1]:,.2f}")

# Calculate Value at Risk (VaR)
var_95 = norm.ppf(0.05, mean_final_value, np.std(final_values))
print(f"95% VaR: ${initial_investment - var_95:,.2f}")