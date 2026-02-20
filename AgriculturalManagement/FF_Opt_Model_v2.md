# 家族経営農業における「適正規模・労働最小化」モデルの数理的定式化（Ver.2）

## 1. 概要と背景
本モデルは、従来の線形計画法（LP）による「所得最大化」や「労働最小化」モデルに、**「経営規模拡大に伴う管理精度の低下（収穫逓減）」** という非線形な要素を組み込んだものです。

現実の家族経営では、作付面積が「適正規模（ピーク）」を超えると、適期作業の遅れや見回りの不足により、単位面積あたりの収益性が低下します。本モデルは、この現象を有理関数として定式化し、**「無理な拡大をせず、最も効率の良い規模で複合経営を行う」** ための意思決定支援を行います。

---

## 2. 数理モデルの定義

### 決定変数 (Decision Variables)
*   $x_j \ge 0 \quad (j = 1, 2, \dots, n)$
    *   作目 $j$ の作付面積（単位：10a）。

### 目的関数 (Objective Function)
必要所得等の制約を満たしつつ、**年間の総労働投入量を最小化**します。

$$\text{Minimize} \quad Z = \sum_{j=1}^{n} L_j x_j$$

*   $L_j$：作目 $j$ の単位面積あたり年間延べ労働時間（定数）。

### 規模連動型収益モデル (Non-linear Revenue Model)
単位面積あたり粗収益 $R_j(x_j)$ を、作付面積 $x_j$ に依存する有理関数として定義します。

$$R_j(x_j) = R_{base, j} + (R_{peak, j} - R_{base, j}) \cdot \frac{2 x_j P_j}{x_j^2 + P_j^2}$$

*   $R_{peak, j}$：適正規模時の最大単収益。
*   $R_{base, j}$：管理限界を超えた際（または極小規模時）の底値単収益。
*   $P_j$：単収益が最大となる適正作付面積（ピーク面積）。

> **【論理的意図】**
> この関数は $x_j = P_j$ で最大値 $1.0$ をとる係数を持ちます。$x_j$ が $P_j$ から離れる（過小または過大）ほど収益性は $R_{base, j}$ に近づきます。これにより「広げすぎの非効率」をペナルティとして表現します。

### 制約条件 (Constraints)

1.  **所得維持制約 (Income Constraint)**  
    規模によって変動する粗収益から変動費を引いた「粗利益」が、目標額 $I_{min}$ を上回ること。
    
    $$\sum_{j=1}^{n} \left( R_j(x_j) - V_j \right) x_j \ge I_{min}$$
    
    *   $V_j$：単位面積あたり変動費（定数）。
    *   **注意点**: $R_j(x_j)$ が非線形であるため、この制約式は非凸（Non-convex）となる可能性があります。

2.  **土地資源制約 (Land Constraint)**  
    
    $$\sum_{j=1}^{n} x_j \le A$$

3.  **月別労働制約 (Monthly Labor Constraints)**  
    各月 $t$ における労働需要が、家族労働供給限界 $H_t$ を超えないこと。
    
    $$\sum_{j=1}^{n} l_{jt} x_j \le H_t \quad (\forall t \in \{1, \dots, 12\})$$

---

## 3. Pythonによるシミュレーション

```python
import numpy as np
from scipy.optimize import minimize

# =========================================================
# 1. パラメータの設定
# =========================================================

crops = ["作物A", "作物B", "作物C"]
n_crops = len(crops)

# --- 収益モデルパラメータ ---
# R_peak: 適正規模時の最大単収益 (万円/10a)
# R_base: 管理限界を超えた際の収束単収益 (万円/10a)
# P_area: 単収益がピークを迎える適正面積 (10a)
revenue_params = {
    "R_peak": np.array([15.0, 20.0, 60.0]), 
    "R_base": np.array([10.0, 12.0, 40.0]),
    "P_area": np.array([30.0, 20.0, 5.0])   
}

variable_costs = np.array([5.0, 8.0, 10.0])    # 万円/10a (変動費)
annual_labor   = np.array([20.0, 25.0, 150.0]) # 時間/10a (年間労働)

# 月別労働係数 (行:月, 列:作物)
# ※簡略化のため6ヶ月分としていますが、実際は12ヶ月分定義可能です
monthly_labor_coeffs = np.array([
    [ 0, 8, 20], [ 10, 8, 20], [ 1, 0, 30], 
    [ 2, 0, 30], [ 2, 0, 30], [ 10, 9, 20]
])

I_min = 500          # 必要所得 (万円)
land_limit = 100     # 利用可能面積 (10a)
H_t = 400            # 月あたりの労働供給限界 (時間)

# =========================================================
# 2. 関数定義
# =========================================================

def unit_revenue_func(x_val, j):
    """
    作目jの面積xにおける単位収益 R(x) を計算
    数理モデル: R(x) = Base + (Peak - Base) * (2xP / (x^2 + P^2))
    """
    # xが負になるのを防ぐ（ソルバーの挙動安定化）
    x = max(0, x_val)
    
    base = revenue_params["R_base"][j]
    peak = revenue_params["R_peak"][j]
    p_val = revenue_params["P_area"][j]
    
    # 分母のゼロ割防止 (+1e-9)
    factor = (2 * x * p_val) / (x**2 + p_val**2 + 1e-9)
    return base + (peak - base) * factor

def objective(x):
    """目的関数: 総労働時間の最小化"""
    return np.dot(annual_labor, x)

def constraint_income(x):
    """
    所得制約: 総粗利益 - I_min >= 0
    ※不等式制約は 'fun' >= 0 の形式で記述
    """
    total_gross_margin = 0
    for j in range(n_crops):
        r_unit = unit_revenue_func(x[j], j)
        # 粗利益 = (単収益 - 変動費) * 面積
        total_gross_margin += (r_unit - variable_costs[j]) * x[j]
    return total_gross_margin - I_min

def constraint_land(x):
    """土地制約: land_limit - Σx >= 0"""
    return land_limit - np.sum(x)

def make_labor_constraint(month_idx):
    """
    ループ内でlambda式を使う際のスコープ問題を回避するための
    クロージャ（関数生成関数）。各月ごとの制約関数を正しく生成します。
    """
    def cons_labor(x):
        # H_t - (その月の労働投入量) >= 0
        return H_t - np.dot(monthly_labor_coeffs[month_idx], x)
    return cons_labor

# =========================================================
# 3. 最適化計算の実行
# =========================================================

# 【重要：初期値の設定戦略】
# 非線形問題では、初期値が「0」に近いと「作っても赤字」と誤判定され
# そのまま動かない(局所解)リスクがあります。
# したがって、初期値は「適正規模(P_area)」付近に設定します。
x0 = revenue_params["P_area"].copy() 
# 土地制約を超えないようスケーリング
if np.sum(x0) > land_limit:
    x0 = x0 * (land_limit / np.sum(x0)) * 0.9

bounds = [(0, land_limit) for _ in range(n_crops)]

# 制約条件のリスト化
cons = [
    {'type': 'ineq', 'fun': constraint_income},
    {'type': 'ineq', 'fun': constraint_land}
]

# 月ごとの労働制約を追加
for t in range(len(monthly_labor_coeffs)):
    cons.append({'type': 'ineq', 'fun': make_labor_constraint(t)})

# 実行 (SLSQP法)
res = minimize(objective, x0, method='SLSQP', bounds=bounds, constraints=cons)

# =========================================================
# 4. 結果の表示と解釈
# =========================================================

if res.success:
    print("=== 適正規模考慮型 農業経営モデル 最適解 (Ver.2.1) ===")
    print(f"ステータス: {res.message}")
    print("-" * 75)
    print(f"{'作目':<6} | {'面積(10a)':<10} | {'単収益':<8} | {'粗利益/10a':<10} | {'適正P':<6} | {'状態'}")
    print("-" * 75)
    
    total_income = 0
    total_labor = 0
    
    for j, crop in enumerate(crops):
        area = res.x[j]
        unit_rev = unit_revenue_func(area, j)
        unit_margin = unit_rev - variable_costs[j]
        peak_area = revenue_params["P_area"][j]
        
        # 状態判定
        if area < 0.1: 
            status = "― 作付なし"
        elif abs(area - peak_area) < 1.0: 
            status = "★ 適正規模 (ピーク維持)"
        elif area > peak_area: 
            status = "▼ 規模過多 (効率悪化)"
        else: 
            status = "▲ 抑制的 (労働節約)"

        print(f"{crop:<6} | {area:>9.2f}  | {unit_rev:>8.2f} | {unit_margin:>10.2f} | {peak_area:>6.1f} | {status}")
        
        total_income += unit_margin * area
        total_labor += annual_labor[j] * area

    print("-" * 75)
    print(f"年間総労働時間 : {total_labor:>8.1f} 時間 (最小化目的)")
    print(f"達成所得       : {total_income:>8.1f} 万円 (目標: {I_min}万円)")
    print(f"土地利用率     : {np.sum(res.x):>8.1f} / {land_limit} (10a)")
    
else:
    print("最適解が見つかりませんでした。")
    print("理由:", res.message)
    print("アドバイス: 目標所得が高すぎるか、労働制約が厳しすぎる可能性があります。")
```

---

## 4. 本モデルの実装・運用におけるリスクと対策

本モデルは実用的ですが、非線形計画法特有の注意点がいくつか存在します。実装時には以下の点にご注意ください。

### ① 局所解（Local Minima）のリスク
*   **現象**: 収益関数が「山型」をしているため、ソルバーが「登り口」を見つけられない場合があります。特に初期値 $x_0$ がゼロに近いと、「面積を少し増やしてもコスト（変動費）を回収できない」と判断し、すべての面積を0にする誤った解（局所解）で停止することがあります。
*   **対策**: コード内で行っているように、**初期値 $x_0$ を適正規模 $P_j$ 付近に設定**して計算を開始することが推奨されます。

### ② 変動費とベース収益の関係
*   **現象**: $V_j$（変動費）が $R_{base, j}$（ベース単収益）よりも大きい場合、初期段階や過剰規模段階で「作れば作るほど赤字」という領域が発生します。
*   **対策**: 現実的にはあり得るシチュエーションですが、解の安定性を高めるため、事前に `if R_base < Variable_Cost` の作物をチェックし、警告を出す仕組みを入れると親切です。

### ③ パラメータ $P_j$ の感度
*   **現象**: 適正規模 $P_j$ の設定値によって、結果が大きく変わります。例えば $P_j$ を過小評価すると、モデルは「これ以上作っても無駄」と判断し、本来稼げるはずの機会を損失する解を出します。
*   **対策**: $P_j$ は固定値ではなく、「現在の技術レベル」と「将来の技術導入（スマート農業等）」のシナリオとして複数パターン用意し、シミュレーション比較を行う使い方が最も効果的です。
