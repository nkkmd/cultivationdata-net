# 家族経営農業における「適正規模・労働最小化」モデルの数理的定式化（Ver.2）

本モデルは、従来の線形計画法による「所得維持・労働最小化」モデルを拡張したものです。
現実の農業経営では、作付面積が拡大するにつれて管理精度が低下し、単位面積あたりの収益性が悪化する（収穫逓減の法則）傾向があります。本モデルでは、**単位面積あたり粗収益を有理関数として定義**することで、各作目の「適正規模」を考慮した意思決定プロセスを再現します。

## 1. 数理モデルの定義

### 決定変数 (Decision Variables)
*   $x_j \ge 0 \quad (j = 1, 2, \dots, n)$
    *   作目 $j$ の作付面積（単位：10a または ha）。

### 目的関数 (Objective Function)
年間の総労働投入量を最小化することを目的とします。

$$\text{Minimize} \quad Z = \sum_{j=1}^{n} L_j x_j$$ 

*   $L_j$：作目 $j$ の単位面積あたりの年間延べ労働時間（定数）。

### 規模連動型収益モデル (Scale-Dependent Revenue Model)
本モデルの核となる定義です。作目 $j$ の単位面積あたり粗収益 $R_j(x_j)$ は定数ではなく、作付面積 $x_j$ に依存する関数として定義します。

$$R_j(x_j) = R_{base, j} + (R_{peak, j} - R_{base, j}) \cdot \frac{2 x_j P_j}{x_j^2 + P_j^2}$$

この有理関数モデルは以下の特性を持ちます：
1.  **ピーク特性**: 作付面積が $x_j = P_j$ （適正規模）のとき、最大単収益 $R_{peak, j}$ を達成します。
2.  **減衰と収束**: 適正規模を超えて拡大すると ($x_j > P_j$)、管理不足等により単収益は緩やかに減少し、最終的に $R_{base, j}$ に収束します。
3.  **立ち上がり**: 規模が小さすぎる場合 ($x_j < P_j$) も、効率が悪く単収益は低くなります。

### 制約条件 (Constraints)

1.  **所得維持制約 (Minimum Income Constraint)**  
    規模によって変動する粗収益に基づき、固定費や生活費を含む必要額 $I_{min}$ を確保します。
    
    $$\sum_{j=1}^{n} \left( R_j(x_j) - V_j \right) x_j \ge I_{min}$$

    *   $V_j$：作目 $j$ の単位面積あたり変動費（定数）。
    *   $R_j(x_j) - V_j$：その規模における単位面積あたり粗利益。

2.  **土地資源制約 (Land Constraint)**  
    
    $$\sum_{j=1}^{n} x_j \le A$$ 

3.  **旬別・月別労働ピーク制約 (Seasonal Labor Constraints)**  
    
    $$\sum_{j=1}^{n} l_{jt} x_j \le H_t \quad (\forall t \in T)$$ 

4.  **非負制約 (Non-negativity Constraint)**

    $$x_j \ge 0 \quad (\forall j)$$ 

---

## 2. 概念的な説明

このモデルは、単なる「利益と労働のトレードオフ」に加え、**「経営品質（管理限界）」** という現実的な壁を導入しています。

*   **「広げすぎ」へのペナルティ**:  
    従来のモデルでは、高収益な作物は土地や労働力の限界まで作付けされました。しかし本モデルでは、ある作物を過剰に拡大すると $R_j(x_j)$ が低下し、結果として「面積を増やしたのに手取りが増えない（むしろ労働だけ増える）」という事態が発生します。
*   **適正規模での寸止め**:  
    最適化アルゴリズムは、各作物の収益性が最も高い「ピーク面積 $P_j$」付近で作付けを止めるインセンティブを持ちます。
*   **複合経営の促進**:  
    単一作物を大規模化して効率を落とすよりも、複数の作物をそれぞれの「適正規模」で組み合わせる方が、トータルの労働対効果が高くなるため、自然とリスク分散型の複合経営が導き出されやすくなります。

---

## 3. Pythonによるシミュレーション

非線形制約を含むため、`scipy.optimize.minimize` (SLSQP法) を使用します。

```python
import numpy as np
from scipy.optimize import minimize

# =========================================================
# 1. パラメータの設定
# =========================================================

crops = ["作物A", "作物B", "作物C"]
n_crops = len(crops)

# --- 収益モデルパラメータ (有理関数用) ---
# R_peak: 適正規模時の最大単収益 (万円/10a)
# R_base: 管理限界を超えた際の収束単収益 (万円/10a)
# P_area: 単収益がピークを迎える適正面積 (10a)
revenue_params = {
    "R_peak": np.array([15.0, 20.0, 60.0]), 
    "R_base": np.array([10.0, 12.0, 40.0]),
    "P_area": np.array([30.0, 20.0, 5.0])   
    # 例: 作物Cは高収益だが手間がかかるため、50a(5.0)を超えると質が落ちる
}

# 変動費・労働時間パラメータ
variable_costs = np.array([5.0, 8.0, 10.0])   # 万円/10a
annual_labor   = np.array([20.0, 25.0, 150.0]) # 時間/10a

# 月別労働係数 (行:月, 列:作物)
monthly_labor_coeffs = np.array([
    [ 0, 8, 20], [ 10, 8, 20], [ 1, 0, 30], 
    [ 2, 0, 30], [ 2, 0, 30], [ 10, 9, 20]
])

# 経営資源・目標
I_min = 500          # 必要所得 (万円)
land_limit = 100     # 利用可能面積 (10a単位 = 10ha)
H_t = 400            # 月あたりの家族労働供給限界 (時間)

# =========================================================
# 2. 関数定義 (非線形計画法)
# =========================================================

def unit_revenue_func(x, j):
    """作目jの面積xにおける単位収益 R(x) を計算"""
    if x < 0: return 0
    base = revenue_params["R_base"][j]
    peak = revenue_params["R_peak"][j]
    p_val = revenue_params["P_area"][j]
    
    # 有理関数モデル: ピーク時に1となる係数を掛ける
    factor = (2 * x * p_val) / (x**2 + p_val**2 + 1e-9)
    return base + (peak - base) * factor

def objective(x):
    """目的関数: 総労働時間の最小化"""
    return np.dot(annual_labor, x)

def constraint_income(x):
    """所得制約: 総粗利益 - I_min >= 0"""
    total_gross_margin = 0
    for j in range(n_crops):
        r_unit = unit_revenue_func(x[j], j)
        total_gross_margin += (r_unit - variable_costs[j]) * x[j]
    return total_gross_margin - I_min

def constraint_land(x):
    """土地制約: land_limit - Σx >= 0"""
    return land_limit - np.sum(x)

def constraint_monthly_labor(x):
    """月別労働制約: H_t - Ax >= 0 (ベクトル)"""
    return H_t - np.dot(monthly_labor_coeffs, x)

# =========================================================
# 3. 最適化計算の実行
# =========================================================

x0 = np.array([10.0, 10.0, 1.0]) # 初期値
bounds = [(0, land_limit) for _ in range(n_crops)]

# 制約条件の定義 (SLSQP形式)
cons = [
    {'type': 'ineq', 'fun': constraint_income},
    {'type': 'ineq', 'fun': constraint_land}
]
# 月別制約を個別に追加
for t in range(len(monthly_labor_coeffs)):
    cons.append({'type': 'ineq', 'fun': lambda x, t=t: H_t - np.dot(monthly_labor_coeffs[t], x)})

res = minimize(objective, x0, method='SLSQP', bounds=bounds, constraints=cons)

# =========================================================
# 4. 結果の表示
# =========================================================

if res.success:
    print("=== 適正規模考慮型 農業経営モデル 最適解 ===")
    print(f"ステータス: {res.message}")
    print("-" * 65)
    print(f"{'作目':<6} | {'面積(10a)':<10} | {'単収益(万円)':<12} | {'適正規模':<10} | {'状態'}")
    print("-" * 65)
    
    total_income = 0
    for j, crop in enumerate(crops):
        area = res.x[j]
        unit_rev = unit_revenue_func(area, j)
        peak_area = revenue_params["P_area"][j]
        
        # 状態判定
        if area < 0.1: status = "作付なし"
        elif abs(area - peak_area) < 1.0: status = "★最適"
        elif area > peak_area: status = "▼過多(効率減)"
        else: status = "▲拡大余地"

        print(f"{crop:<6} | {area:>9.2f}  | {unit_rev:>11.2f}  | {peak_area:>9.1f}  | {status}")
        total_income += (unit_rev - variable_costs[j]) * area

    print("-" * 65)
    print(f"最小化された年間総労働時間: {res.fun:>8.1f} 時間")
    print(f"達成所得(粗利益合計)      : {total_income:>8.1f} 万円 (目標: {I_min}万円)")
else:
    print("最適解が見つかりませんでした。条件を見直してください。")
```

---

## 4. モデルの解釈と応用

このモデルによって得られる示唆は、実際の農業経営者の感覚に非常に近いものとなります。

*   **「腹八分目」の経営判断**:  
    シミュレーション結果において、特定の作物が「適正規模（ピーク面積）」付近で止まる現象が確認できます。これは、「これ以上面積を増やしても、管理が追いつかず単価が下がるため、労働を増やす価値がない」とモデルが判断したことを意味します。
*   **技術向上への投資効果**:  
    パラメータ $P_j$（ピーク面積）を大きくすることは、機械化やスマート農業導入による「管理能力の向上」を意味します。このモデルを使えば、「新しい機械を入れて管理可能面積を10haから15haに広げた場合、どれだけ所得が増え、労働が減るか」を定量的に予測できます。
*   **高収益作物の罠**:  
    作物Cのように「ピーク時の収益は高いが、適正規模が小さい（手間がかかる）」作物は、少しでも面積を広げすぎると急激に効率が悪化します。モデルはこれを敏感に察知し、作物Cを小規模に抑えつつ、安定した作物AやBでベースを固める戦略を提案します。
