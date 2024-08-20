import numpy as np
import matplotlib.pyplot as plt
from dataclasses import dataclass

@dataclass
class SimulationParams:
    initial_investment: float
    investment_period: int
    risk_tolerance: str
    asset_allocation: dict
    asset_returns: dict
    asset_volatilities: dict
    inflation_rate: float
    stress_scenario: str
    rebalance_frequency: int

def run_simulation(params):
    # Adjust returns and volatilities based on risk tolerance
    risk_multipliers = {'conservative': 0.8, 'moderate': 1.0, 'aggressive': 1.2}
    risk_multiplier = risk_multipliers[params.risk_tolerance]
    adjusted_returns = {k: v * risk_multiplier for k, v in params.asset_returns.items()}
    adjusted_volatilities = {k: v * risk_multiplier for k, v in params.asset_volatilities.items()}

    # Calculate portfolio return and volatility
    portfolio_return = sum(params.asset_allocation[asset] * adjusted_returns[asset] for asset in params.asset_allocation)
    portfolio_volatility = np.sqrt(sum((params.asset_allocation[asset] * adjusted_volatilities[asset])**2 for asset in params.asset_allocation))

    # Simulate scenarios
    normal_scenario = simulate_scenario(params, portfolio_return, portfolio_volatility, 'normal')
    stress_scenario = simulate_scenario(params, portfolio_return, portfolio_volatility, params.stress_scenario)

    return normal_scenario, stress_scenario

def simulate_scenario(params, base_return, base_volatility, scenario_type):
    np.random.seed()  # Reset seed for each simulation
    scenario = [params.initial_investment]
    
    if scenario_type == 'market_crash':
        scenario[0] *= 0.6  # 40% initial drop
        return_multiplier, volatility_multiplier = 0.5, 1.5
    elif scenario_type == 'prolonged_recession':
        return_multiplier, volatility_multiplier = 0.3, 1.2
    elif scenario_type == 'high_inflation':
        return_multiplier, volatility_multiplier = 1.0, 1.0
        base_return -= params.inflation_rate / 100
    else:  # normal scenario
        return_multiplier, volatility_multiplier = 1.0, 1.0
    
    scenario_return = base_return * return_multiplier
    scenario_volatility = base_volatility * volatility_multiplier

    for month in range(params.investment_period * 12):
        monthly_return = np.random.normal(scenario_return / 12, scenario_volatility / np.sqrt(12))
        real_return = monthly_return - params.inflation_rate / 1200  # Adjust for inflation
        scenario.append(scenario[-1] * (1 + real_return))
        
        if (month + 1) % params.rebalance_frequency == 0:
            target_allocation = {asset: value * scenario[-1] for asset, value in params.asset_allocation.items()}
            scenario[-1] = sum(target_allocation.values())

    return scenario

def plot_results(normal_scenario, stress_scenario, params):
    years = range(0, params.investment_period + 1)
    normal_annual = [normal_scenario[i*12] for i in years]
    stress_annual = [stress_scenario[i*12] for i in years]

    plt.figure(figsize=(10, 6))
    plt.plot(years, normal_annual, label='Normal Scenario')
    plt.plot(years, stress_annual, label='Stress Scenario')
    plt.xlabel('Years')
    plt.ylabel('Portfolio Value ($)')
    plt.title('Asset Management Stress Test Simulation')
    plt.legend()
    plt.grid(True)
    plt.xticks(years)
    plt.show()

def get_user_input(prompt, default=None):
    if default is not None:
        user_input = input(f"{prompt} (デフォルト: {default}): ").strip()
        return default if user_input == "" else float(user_input)
    else:
        return float(input(prompt))

def main():
    print("資産運用ストレステストシミュレーター")

    initial_investment = get_user_input("初期投資額（$）")
    investment_period = int(get_user_input("投資期間（年）"))
    
    risk_tolerance_options = {
        '1': ('保守的', 'conservative'),
        '2': ('中庸', 'moderate'),
        '3': ('積極的', 'aggressive')
    }
    print("\nリスク許容度を選択してください:")
    print("1. 保守的 - リスクを最小限に抑え、安定した運用を目指します。")
    print("2. 中庸 - バランスの取れたリスクと収益を目指します。")
    print("3. 積極的 - 高いリターンを目指し、より大きなリスクを取ります。")
    risk_choice = input("番号を入力してください (1/2/3): ")
    risk_tolerance = risk_tolerance_options[risk_choice][1]

    print("\n資産配分を入力してください（合計が100%になるようにしてください）")
    stocks = get_user_input("株式の割合（%）")
    bonds = get_user_input("債券の割合（%）")
    cash = 100 - stocks - bonds
    print(f"現金の割合（%）: {cash:.1f}")
    asset_allocation = {'stocks': stocks/100, 'bonds': bonds/100, 'cash': cash/100}

    print("\n各資産クラスの想定リターンとボラティリティを入力してください")
    asset_returns = {
        'stocks': get_user_input("株式の想定リターン（%）", 8.0) / 100,
        'bonds': get_user_input("債券の想定リターン（%）", 3.0) / 100,
        'cash': get_user_input("現金の想定リターン（%）", 1.0) / 100
    }
    asset_volatilities = {
        'stocks': get_user_input("株式のボラティリティ（%）", 20.0) / 100,
        'bonds': get_user_input("債券のボラティリティ（%）", 8.0) / 100,
        'cash': get_user_input("現金のボラティリティ（%）", 1.0) / 100
    }

    inflation_rate = get_user_input("想定インフレ率（%）")

    stress_scenario_options = {
        '1': ('市場急落', 'market_crash'),
        '2': ('長期不況', 'prolonged_recession'),
        '3': ('高インフレ', 'high_inflation')
    }
    print("\nストレスシナリオを選択してください:")
    print("1. 市場急落 - 株式市場が急激に下落し、その後緩やかに回復するシナリオ")
    print("2. 長期不況 - 経済が長期間停滞し、全体的なリターンが低下するシナリオ")
    print("3. 高インフレ - インフレ率が急上昇し、実質リターンが大きく低下するシナリオ")
    scenario_choice = input("番号を入力してください (1/2/3): ")
    stress_scenario = stress_scenario_options[scenario_choice][1]

    rebalance_frequency = int(get_user_input("リバランス頻度（月）"))

    params = SimulationParams(
        initial_investment=initial_investment,
        investment_period=investment_period,
        risk_tolerance=risk_tolerance,
        asset_allocation=asset_allocation,
        asset_returns=asset_returns,
        asset_volatilities=asset_volatilities,
        inflation_rate=inflation_rate,
        stress_scenario=stress_scenario,
        rebalance_frequency=rebalance_frequency
    )

    normal_scenario, stress_scenario = run_simulation(params)

    print(f"\n通常シナリオの最終ポートフォリオ価値: ${normal_scenario[-1]:,.0f}")
    print(f"ストレスシナリオの最終ポートフォリオ価値: ${stress_scenario[-1]:,.0f}")

    plot_results(normal_scenario, stress_scenario, params)

if __name__ == "__main__":
    main()