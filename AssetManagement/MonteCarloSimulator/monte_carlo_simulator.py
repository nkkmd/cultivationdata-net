"""農業経営支援基金向けの取り崩し付きモンテカルロ・シミュレーター。

同じ通貨建ての調整後終値を利用し、銘柄別の日次対数リターンの平均と
共分散から相関を保った正規乱数を生成する。各月を21営業日として扱う。
"""

from dataclasses import dataclass
from pathlib import Path
from typing import Optional

import numpy as np
import pandas as pd


TRADING_DAYS_PER_MONTH = 21
SMOOTHING_MONTHS = 12


@dataclass(frozen=True)
class WithdrawalPolicy:
    """年間の支出計画と、基金に残す最低残高（いずれも同一通貨）。"""

    mode: str = "none"  # none, fixed, percentage, smoothed
    annual_amount: float = 0.0  # fixed: 年間の名目取り崩し予定額
    annual_rate: float = 0.0  # percentage / smoothed: 年率、小数（0.03=3%）
    frequency_months: int = 12  # 1=月次、12=年次
    annual_inflation: float = 0.0  # fixed のみ。各回支出額を名目で調整
    minimum_balance: float = 0.0  # 取り崩し後に保護する基金残高

    def __post_init__(self):
        if self.mode not in ("none", "fixed", "percentage", "smoothed"):
            raise ValueError("取り崩し方式は none / fixed / percentage / smoothed から選択してください。")
        if self.frequency_months not in (1, 12):
            raise ValueError("取り崩し間隔は1か月または12か月です。")
        for name, value in (("年間定額", self.annual_amount), ("年間支出率", self.annual_rate),
                            ("最低残高", self.minimum_balance), ("インフレ率", self.annual_inflation)):
            if not np.isfinite(value):
                raise ValueError(f"{name}は有限の数値で指定してください。")
        if self.annual_amount < 0 or self.minimum_balance < 0:
            raise ValueError("年間定額と最低残高は0以上にしてください。")
        if not 0 <= self.annual_rate <= 1:
            raise ValueError("年間支出率は0～1の範囲で指定してください。")
        if self.annual_inflation <= -1:
            raise ValueError("年率インフレ率は-100%より大きくしてください。")


@dataclass
class SimulationResult:
    # いずれも (月数+1, 試行数) 。0か月目は初期残高・支出ゼロ。
    portfolio_values: np.ndarray  # 各月末の取り崩し・リバランス後の残高
    cumulative_withdrawals: np.ndarray  # 実際に支払えた累計額
    cumulative_shortfalls: np.ndarray  # 支出予定額と実際の支出額との差の累計
    first_shortfall_month: np.ndarray  # 支払い不足の初発月、未発生なら0

    @property
    def final_values(self):
        return self.portfolio_values[-1]

    @property
    def shortfall_probability(self):
        return float(np.mean(self.first_shortfall_month > 0))


def get_stock_data(tickers, start_date, end_date):
    """yfinanceの調整後終値を、ティッカー順の2次元表で返す。"""
    import yfinance as yf  # オフラインの数理試験でもモジュールを読み込めるよう遅延import

    if not tickers or len(set(tickers)) != len(tickers):
        raise ValueError("ティッカーは重複のない1件以上を指定してください。")
    print("価格データを取得中...")
    raw = yf.download(
        tickers, start=start_date, end=end_date,
        auto_adjust=True, group_by="column", progress=False,
    )
    if raw is None or raw.empty:
        raise ValueError("価格データが取得できませんでした。銘柄と期間を確認してください。")
    # auto_adjust=Trueの場合、配当・分割調整済みの値は Close に入る。
    prices = raw["Close"]
    if isinstance(prices, pd.Series):
        prices = prices.to_frame(name=tickers[0])
    missing = [ticker for ticker in tickers if ticker not in prices.columns]
    if missing:
        raise ValueError(f"価格データのない銘柄: {', '.join(missing)}")
    prices = prices.loc[:, tickers].apply(pd.to_numeric, errors="coerce").dropna()
    if len(prices) < 61 or (prices.to_numpy() <= 0).any():
        raise ValueError("共通の有効価格データが不足しています（最低61営業日分・正の価格が必要）。")
    print(f"価格データ取得完了: {len(prices)}営業日（共通観測日）")
    return prices


def calculate_portfolio_returns(data, weights):
    """参考表示用の固定配分の日次単純リターン（再配分を毎日行う想定）。"""
    weights = _validate_weights(weights, data.shape[1])
    return data.pct_change(fill_method=None).dropna().dot(weights)


def _validate_weights(weights, asset_count):
    weights = np.asarray(weights, dtype=float)
    if (weights.ndim != 1 or len(weights) != asset_count or
            not np.isfinite(weights).all() or (weights < 0).any() or
            not np.isclose(weights.sum(), 1.0, rtol=0.0, atol=1e-8)):
        raise ValueError("資産配分は銘柄数と一致する非負の割合で、合計1にしてください。")
    return weights / weights.sum()


def estimate_log_return_model(prices):
    """同一観測日の資産別日次対数リターンの平均ベクトル・共分散。"""
    if prices.shape[1] < 1 or len(prices) < 61:
        raise ValueError("最低61営業日分の有効な価格データが必要です。")
    values = prices.to_numpy(dtype=float)
    if not np.isfinite(values).all() or (values <= 0).any():
        raise ValueError("価格には正の有限値だけを指定してください。")
    log_returns = np.diff(np.log(values), axis=0)
    means = log_returns.mean(axis=0)
    covariance = np.atleast_2d(np.cov(log_returns, rowvar=False))
    return means, covariance


def rebalance_portfolio(portfolio_values, target_weights):
    """指定した複数資産の合計残高を目標配分へ振り直す。"""
    values = np.asarray(portfolio_values, dtype=float)
    weights = _validate_weights(target_weights, len(values))
    return values.sum() * weights


def _withdrawal_request(policy, month, current_value, history):
    """当月の必要支出（試行ごとの配列）。月末時点で、取り崩し前に判定。"""
    if policy.mode == "none" or month % policy.frequency_months:
        return np.zeros_like(current_value)
    period_fraction = policy.frequency_months / 12
    if policy.mode == "fixed":
        # 初回支出は設定額、その後は支出時点の間隔に応じてインフレ調整。
        completed_years = (month - policy.frequency_months) / 12
        amount = policy.annual_amount * period_fraction * (1 + policy.annual_inflation) ** completed_years
        return np.full_like(current_value, amount)
    if policy.mode == "percentage":
        return current_value * policy.annual_rate * period_fraction
    # smoothed: 月末の取り崩し前評価額の直近12観測（月）の単純平均。
    average_value = np.mean(np.stack(history[-SMOOTHING_MONTHS:]), axis=0)
    return average_value * policy.annual_rate * period_fraction


def monte_carlo_simulation(initial_investment, months, num_simulations,
                           daily_log_means, daily_log_covariance, weights,
                           rebalance_months=12, withdrawal_policy=None,
                           seed: Optional[int] = None):
    """日次資産別リターン、月末の支出・再配分を試行する。

    毎月21営業日→月末評価→必要支出→（指定月なら）リバランス、の順。
    払えない額は不足額に記録し、借入やマイナス残高は認めない。
    """
    if not isinstance(months, int) or months <= 0:
        raise ValueError("期間（月数）は1以上の整数にしてください。")
    if not isinstance(num_simulations, int) or num_simulations <= 0:
        raise ValueError("試行回数は1以上の整数にしてください。")
    if not isinstance(rebalance_months, int) or rebalance_months < 0:
        raise ValueError("リバランス間隔は0（なし）または正の月数にしてください。")
    if not np.isfinite(initial_investment) or initial_investment <= 0:
        raise ValueError("初期投資額は正の有限値にしてください。")

    means = np.atleast_1d(np.asarray(daily_log_means, dtype=float))
    cov = np.atleast_2d(np.asarray(daily_log_covariance, dtype=float))
    count = len(means)
    weights = _validate_weights(weights, count)
    if (cov.shape != (count, count) or not np.isfinite(means).all() or
            not np.isfinite(cov).all() or not np.allclose(cov, cov.T, atol=1e-12)):
        raise ValueError("日次対数リターンの平均・共分散が不正です。")
    if np.linalg.eigvalsh(cov).min() < -1e-10:
        raise ValueError("共分散行列は半正定値である必要があります。")
    policy = withdrawal_policy or WithdrawalPolicy()
    if not isinstance(policy, WithdrawalPolicy):
        raise TypeError("withdrawal_policyにはWithdrawalPolicyを指定してください。")

    rng = np.random.default_rng(seed)
    holdings = np.broadcast_to(initial_investment * weights,
                               (num_simulations, count)).copy()
    values = np.empty((months + 1, num_simulations), dtype=float)
    paid = np.zeros_like(values)
    shortfalls = np.zeros_like(values)
    first_shortfall_month = np.zeros(num_simulations, dtype=int)
    values[0] = initial_investment
    history = [values[0].copy()]  # 月数が少ない間は初期残高を平均に利用

    for month in range(1, months + 1):
        for _ in range(TRADING_DAYS_PER_MONTH):
            log_change = rng.multivariate_normal(means, cov, size=num_simulations)
            log_change = log_change.reshape(num_simulations, count)
            holdings *= np.exp(log_change)
        before = holdings.sum(axis=1)
        if not np.isfinite(before).all():
            raise FloatingPointError("シミュレーション中に数値がオーバーフローしました。")
        history.append(before.copy())
        request = _withdrawal_request(policy, month, before, history)
        payable = np.minimum(request, np.maximum(before - policy.minimum_balance, 0.0))
        deficiency = np.maximum(request - payable, 0.0)
        first_mask = (first_shortfall_month == 0) & (deficiency > 1e-9)
        first_shortfall_month[first_mask] = month
        paid[month] = paid[month - 1] + payable
        shortfalls[month] = shortfalls[month - 1] + deficiency

        after = before - payable
        scale = np.divide(after, before, out=np.zeros_like(after), where=before > 0)
        holdings *= scale[:, None]  # 保有割合に応じて比例売却
        if rebalance_months and month % rebalance_months == 0:
            holdings = after[:, None] * weights[None, :]
        values[month] = after

    return SimulationResult(values, paid, shortfalls, first_shortfall_month)


def calculate_risk_metrics(final_values, initial_investment, confidence_level=0.95):
    """支出後の終期基金残高を対象にした指標（支出を損失扱いしない指標ではない）。"""
    values = np.asarray(final_values, dtype=float)
    if values.ndim != 1 or len(values) == 0 or not np.isfinite(values).all():
        raise ValueError("終期残高には有限の1次元配列を指定してください。")
    if not 0 < confidence_level < 1 or initial_investment <= 0:
        raise ValueError("信頼水準・初期残高が不正です。")
    lower = (1 - confidence_level) * 100
    lower_value = np.percentile(values, lower)
    tail = values[values <= lower_value]
    return {
        "mean": float(values.mean()),
        "median": float(np.median(values)),
        "min": float(values.min()),
        "max": float(values.max()),
        "prediction_interval_90": np.percentile(values, [5, 95]),
        "var": max(0.0, initial_investment - lower_value),
        "cvar": max(0.0, initial_investment - float(tail.mean())),
    }


def _read_float(prompt, minimum=None, default=None):
    raw = input(prompt).strip()
    value = float(raw) if raw else default
    if value is None or not np.isfinite(value) or (minimum is not None and value < minimum):
        raise ValueError(f"有限で{minimum}以上の数値を指定してください。" if minimum is not None else "数値が不正です。")
    return value


def _read_int(prompt, minimum=0, default=None):
    raw = input(prompt).strip()
    value = int(raw) if raw else default
    if value is None or value < minimum:
        raise ValueError(f"{minimum}以上の整数を指定してください。")
    return value


def get_user_input():
    portfolio = {}
    total = 0.0
    print("資産配分の合計が100%になるまで入力してください。")
    while total < 1 - 1e-8:
        ticker = input("ティッカーシンボル: ").strip().upper()
        if not ticker or ticker in portfolio:
            raise ValueError("空欄または重複したティッカーは指定できません。")
        weight = _read_float(f"{ticker}の配分割合（例: 0.4=40%）: ", minimum=0)
        if weight <= 0 or total + weight > 1 + 1e-8:
            raise ValueError("割合は正であり、合計100%を超えないようにしてください。")
        portfolio[ticker] = weight
        total += weight
        print(f"累計: {total:.1%}")
    portfolio = {ticker: weight / total for ticker, weight in portfolio.items()}

    start_date = input("過去データの開始日（YYYY-MM-DD）: ").strip()
    end_date = input("過去データの終了日（YYYY-MM-DD、終了日は含まない）: ").strip()
    if not start_date or not end_date or pd.to_datetime(start_date) >= pd.to_datetime(end_date):
        raise ValueError("データ取得期間を正しく指定してください。")

    initial = _read_float("基金の初期金額（同一通貨単位）: ", minimum=0)
    if initial <= 0:
        raise ValueError("初期金額は0より大きくしてください。")
    months = _read_int("将来のシミュレーション期間（月数）: ", minimum=1)
    trials = _read_int("試行回数（既定: 1000）: ", minimum=1, default=1000)
    rebalance = _read_int("リバランスの間隔（月数、0=なし、既定12）: ", default=12)
    mode_key = input("取り崩し方式 [0:なし, 1:年間定額, 2:期末評価額の定率, 3:直近12か月平均の定率]（既定0）: ").strip() or "0"
    modes = {"0": "none", "1": "fixed", "2": "percentage", "3": "smoothed"}
    if mode_key not in modes:
        raise ValueError("取り崩し方式は0～3で指定してください。")
    policy_args = {"mode": modes[mode_key]}
    if mode_key != "0":
        policy_args["frequency_months"] = _read_int("取り崩し頻度 [1:毎月, 12:毎年]（既定12）: ", minimum=1, default=12)
        if mode_key == "1":
            policy_args["annual_amount"] = _read_float("年間の取り崩し予定額（基金と同一通貨）: ", minimum=0)
            policy_args["annual_inflation"] = _read_float("予定額の年間増加率（%、既定0）: ", default=0) / 100
        else:
            policy_args["annual_rate"] = _read_float("年間支出率（%、例: 3）: ", minimum=0) / 100
        policy_args["minimum_balance"] = _read_float("取り崩し後に保護する最低残高（既定0）: ", minimum=0, default=0)
    policy = WithdrawalPolicy(**policy_args)
    raw_seed = input("乱数シード（空欄=毎回異なる結果、例:42）: ").strip()
    seed = int(raw_seed) if raw_seed else None
    return portfolio, start_date, end_date, initial, months, trials, rebalance, policy, seed


def print_results(result, initial_investment):
    metrics = calculate_risk_metrics(result.final_values, initial_investment)
    print("\n--- 基金シミュレーション結果（支出後の残高） ---")
    print(f"最終残高の平均値: {metrics['mean']:,.2f}")
    print(f"中央値: {metrics['median']:,.2f}")
    print(f"最小値 / 最大値: {metrics['min']:,.2f} / {metrics['max']:,.2f}")
    print(f"最終残高の90%予測区間: {metrics['prediction_interval_90'][0]:,.2f} ～ {metrics['prediction_interval_90'][1]:,.2f}")
    print(f"終期残高の95% VaR（初期金額比）: {metrics['var']:,.2f}")
    print(f"終期残高の95% CVaR（初期金額比）: {metrics['cvar']:,.2f}")
    print(f"実際に支払えた累計額の中央値: {np.median(result.cumulative_withdrawals[-1]):,.2f}")
    print(f"予定支出の不足が一度でも発生する割合: {result.shortfall_probability:.1%}")
    print(f"不足額累計の平均値: {result.cumulative_shortfalls[-1].mean():,.2f}")
    print("※VaR/CVaRは取り崩し後の残高を初期金額と比較したもので、運用損失だけを表す値ではありません。")


def plot_results(result, portfolio, output_dir="."):
    """グラフをPNG保存し、対話型バックエンドなら画面にも表示する。

    Agg等の非対話型バックエンドでplt.show()を呼ぶと警告になるため、
    非対話型環境では画像保存のみを行う。戻り値は保存先パスのタプル。
    """
    import matplotlib.pyplot as plt

    destination = Path(output_dir).expanduser()
    destination.mkdir(parents=True, exist_ok=True)

    months = np.arange(result.portfolio_values.shape[0])
    values = result.portfolio_values
    fig, ax = plt.subplots(figsize=(11, 6))
    # 混雑を避けるため経路の表示は最大100本とする。
    for trial in range(min(values.shape[1], 100)):
        ax.plot(months, values[:, trial], alpha=0.12, linewidth=0.7, color="gray")
    ax.fill_between(months, np.percentile(values, 5, axis=1),
                    np.percentile(values, 95, axis=1), alpha=0.18, label="5–95 percentile")
    ax.plot(months, np.median(values, axis=1), linewidth=2, label="Median fund balance")
    ax.set(xlabel="Months", ylabel="Fund balance (portfolio currency)",
           title=f"Monte Carlo fund balance after withdrawals: {', '.join(portfolio)}")
    ax.legend()
    ax.grid(alpha=0.2)
    fig.tight_layout()

    fig2, ax2 = plt.subplots(figsize=(11, 5))
    paid = result.cumulative_withdrawals
    ax2.fill_between(months, np.percentile(paid, 5, axis=1),
                     np.percentile(paid, 95, axis=1), alpha=0.18, label="5–95 percentile")
    ax2.plot(months, np.median(paid, axis=1), linewidth=2, label="Median cumulative paid")
    ax2.set(xlabel="Months", ylabel="Total withdrawals paid (portfolio currency)",
            title="Cumulative withdrawals from the fund")
    ax2.legend()
    ax2.grid(alpha=0.2)
    fig2.tight_layout()

    balance_path = destination / "monte_carlo_fund_balance.png"
    withdrawals_path = destination / "monte_carlo_cumulative_withdrawals.png"
    try:
        fig.savefig(balance_path, dpi=150)
        fig2.savefig(withdrawals_path, dpi=150)
        print(f"基金残高のグラフを保存しました: {balance_path.resolve()}")
        print(f"累計支出のグラフを保存しました: {withdrawals_path.resolve()}")

        # バックエンドがAgg等の場合、show()は表示できず警告になる。
        noninteractive_backends = {"agg", "pdf", "svg", "ps", "pgf", "cairo", "template"}
        if plt.get_backend().lower() not in noninteractive_backends:
            plt.show()
        return balance_path, withdrawals_path
    finally:
        plt.close(fig)
        plt.close(fig2)


def main():
    (portfolio, start_date, end_date, initial, months,
     trials, rebalance, policy, seed) = get_user_input()
    prices = get_stock_data(list(portfolio), start_date, end_date)
    means, covariance = estimate_log_return_model(prices)
    result = monte_carlo_simulation(
        initial, months, trials, means, covariance, list(portfolio.values()),
        rebalance_months=rebalance, withdrawal_policy=policy, seed=seed,
    )
    print_results(result, initial)
    plot_results(result, portfolio)


if __name__ == "__main__":
    try:
        main()
    except (ValueError, TypeError, FloatingPointError) as exc:
        raise SystemExit(f"エラー: {exc}") from exc
