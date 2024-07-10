import numpy as np
import matplotlib.pyplot as plt
from dataclasses import dataclass

@dataclass
class SimulationParams:
    initial_investment: float
    investment_period: int
    risk_tolerance: str
    asset_allocation: dict
    inflation_rate: float
    stress_scenario: str
    rebalance_frequency: int

def run_simulation(params):
    np.random.seed(42)  # For reproducibility

    # Define asset class returns and volatilities
    asset_returns = {
        'stocks': 0.10,
        'bonds': 0.05,
        'cash': 0.02
    }
    asset_volatilities = {
        'stocks': 0.20,
        'bonds': 0.05,
        'cash': 0.01
    }

    # Adjust returns and volatilities based on risk tolerance
    if params.risk_tolerance == 'conservative':
        asset_returns = {k: v * 0.8 for k, v in asset_returns.items()}
        asset_volatilities = {k: v * 0.8 for k, v in asset_volatilities.items()}
    elif params.risk_tolerance == 'aggressive':
        asset_returns = {k: v * 1.2 for k, v in asset_returns.items()}
        asset_volatilities = {k: v * 1.2 for k, v in asset_volatilities.items()}

    # Calculate portfolio return and volatility
    portfolio_return = sum(params.asset_allocation[asset] * asset_returns[asset] for asset in params.asset_allocation)
    portfolio_volatility = np.sqrt(sum((params.asset_allocation[asset] * asset_volatilities[asset])**2 for asset in params.asset_allocation))

    # Simulate normal scenario
    normal_scenario = [params.initial_investment]
    for month in range(params.investment_period * 12):
        monthly_return = np.random.normal(portfolio_return / 12, portfolio_volatility / np.sqrt(12))
        normal_scenario.append(normal_scenario[-1] * (1 + monthly_return))
        
        # Rebalance if it's time
        if (month + 1) % params.rebalance_frequency == 0:
            target_allocation = {asset: value * normal_scenario[-1] for asset, value in params.asset_allocation.items()}
            normal_scenario[-1] = sum(target_allocation.values())

    # Simulate stress scenario
    stress_scenario = [params.initial_investment]
    if params.stress_scenario == 'market_crash':
        stress_scenario[0] *= 0.7  # 30% initial drop
        stress_return = portfolio_return * 0.5
        stress_volatility = portfolio_volatility * 1.5
    elif params.stress_scenario == 'prolonged_recession':
        stress_return = portfolio_return * 0.3
        stress_volatility = portfolio_volatility * 1.2
    elif params.stress_scenario == 'high_inflation':
        stress_return = portfolio_return - params.inflation_rate / 100
        stress_volatility = portfolio_volatility

    for month in range(params.investment_period * 12):
        monthly_return = np.random.normal(stress_return / 12, stress_volatility / np.sqrt(12))
        stress_scenario.append(stress_scenario[-1] * (1 + monthly_return))
        
        # Rebalance if it's time
        if (month + 1) % params.rebalance_frequency == 0:
            target_allocation = {asset: value * stress_scenario[-1] for asset, value in params.asset_allocation.items()}
            stress_scenario[-1] = sum(target_allocation.values())

    return normal_scenario, stress_scenario

def plot_results(normal_scenario, stress_scenario, params):
    years = range(0, params.investment_period + 1)
    normal_annual = [normal_scenario[i*12] for i in years]
    stress_annual = [stress_scenario[i*12] for i in years]

    plt.figure(figsize=(10, 6))
    plt.plot(years, normal_annual, label='Normal Scenario')
    plt.plot(years, stress_annual, label='Stress Scenario')
    plt.xlabel('Years')
    plt.ylabel('Portfolio Value')
    plt.title('Asset Management Stress Test Simulation')
    plt.legend()
    plt.grid(True)
    plt.xticks(years)
    plt.show()

def main():
    print("資産運用ストレステストシミュレーター")

    initial_investment = float(input("初期投資額（円）を入力してください: "))
    investment_period = int(input("投資期間（年）を入力してください: "))
    
    risk_tolerance_options = ['保守的', '中庸', '積極的']
    print("リスク許容度を選択してください:")
    for i, option in enumerate(risk_tolerance_options, 1):
        print(f"{i}. {option}")
    risk_choice = int(input("番号を入力してください: "))
    risk_tolerance = ['conservative', 'moderate', 'aggressive'][risk_choice - 1]

    print("資産配分を入力してください（合計が100%になるようにしてください）")
    stocks = float(input("株式の割合（%）: "))
    bonds = float(input("債券の割合（%）: "))
    cash = float(input("現金の割合（%）: "))
    asset_allocation = {'stocks': stocks/100, 'bonds': bonds/100, 'cash': cash/100}

    inflation_rate = float(input("想定インフレ率（%）を入力してください: "))

    stress_scenario_options = ['市場急落', '長期不況', '高インフレ']
    print("ストレスシナリオを選択してください:")
    for i, option in enumerate(stress_scenario_options, 1):
        print(f"{i}. {option}")
    scenario_choice = int(input("番号を入力してください: "))
    stress_scenario = ['market_crash', 'prolonged_recession', 'high_inflation'][scenario_choice - 1]

    rebalance_frequency = int(input("リバランス頻度（月）を入力してください: "))

    params = SimulationParams(
        initial_investment=initial_investment,
        investment_period=investment_period,
        risk_tolerance=risk_tolerance,
        asset_allocation=asset_allocation,
        inflation_rate=inflation_rate,
        stress_scenario=stress_scenario,
        rebalance_frequency=rebalance_frequency
    )

    normal_scenario, stress_scenario = run_simulation(params)

    print(f"\n通常シナリオの最終ポートフォリオ価値: {normal_scenario[-1]:,.0f}円")
    print(f"ストレスシナリオの最終ポートフォリオ価値: {stress_scenario[-1]:,.0f}円")

    plot_results(normal_scenario, stress_scenario, params)

if __name__ == "__main__":
    main()