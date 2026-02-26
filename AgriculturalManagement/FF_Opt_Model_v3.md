# 新規就農者向け「適正規模・労働最小化」モデルの数理的定式化（Ver.3）

## 1. 概要と背景
本モデルは、家族経営農業における「規模拡大に伴う収穫逓減（管理精度の低下）」を考慮したVer.2モデルを土台とし、**新規就農者特有のリアルな課題**を組み込んだ拡張版（Ver.3）です。

新規就農においては、単なる「売上と労働時間」のバランスだけでなく、**「初期投資（イニシャルコスト）と資金繰り（融資返済）」**、そして **「未熟練による作業効率の低さ」** が極めて重要なファクターとなります。本モデルは、これらの要素を数理的に統合し、「借金返済に追われて過労に陥る」といった新規就農の失敗パターンを未然に防ぐための意思決定支援を行います。

### Ver.3 で追加された主要素
1. **イニシャルコストと融資条件**: 作物ごとの初期投資額、自己資金、金利、返済期間から年間の元利均等返済額を算出。
2. **借入限度額（与信枠）制約**: 信用実績のない新規就農者の現実的な借入上限を設定。
3. **習熟度（スキルレベル）パラメータ**: 未熟練による「適正規模の縮小」と「労働時間の増加」を自動補正。
4. **就農支援の補助金**: 農業次世代人材投資資金などの定額収入を資金繰りに考慮。

---

## 2. 数理モデルの定義

### 決定変数 (Decision Variables)
*   $x_j \ge 0 \quad (j = 1, 2, \dots, n)$
    *   作目 $j$ の作付面積（単位：10a）。

### 目的関数 (Objective Function)
資金繰り等の制約を満たしつつ、**習熟度で補正された年間の総労働投入量を最小化**します。

$$\text{Minimize} \quad Z = \sum_{j=1}^{n} L^\prime_j x_j$$

*   $L^\prime_j = L_j / k_{skill}$ ：作目 $j$ の単位面積あたり年間延べ労働時間（ $L_j$ ：ベテランの労働時間、 $k_{skill}$ ：習熟度 $0 < k_{skill} \le 1.0$）。

### 規模連動型収益モデル (Non-linear Revenue Model)
単位面積あたり粗収益 $R_j(x_j)$ を、作付面積 $x_j$ に依存する有理関数として定義します。習熟度により、ピークを迎える適正面積が縮小します。

$$R_j(x_j) = R_{base, j} + (R_{peak, j} - R_{base, j}) \cdot \frac{2 x_j P^\prime_j}{x_j^2 + (P'_j)^2}$$

*   $R_{peak, j}$：適正規模時の最大単収益。
*   $R_{base, j}$：管理限界を超えた際の底値単収益。
*   $P^\prime_j = P_j \times k_{skill}$：習熟度で補正された適正作付面積（ピーク面積）。

### 制約条件 (Constraints)

**1. 資金繰り制約 (Cashflow Constraint)**  
農業粗利益と補助金の合計が、最低限の生活費と融資の年間返済額を上回ること。

$$\sum_{j=1}^{n} \left( R_j(x_j) - V_j \right) x_j + B \ge I_{living} + PMT(x)$$

*   $V_j$：単位面積あたり変動費。
*   $B$：年間補助金（就農支援金など）。
*   $I_{living}$：最低限必要な年間生活費。
*   $PMT(x)$：年間返済額。以下の式で算出します。

$$PMT(x) = \max\left(0, \sum_{j=1}^{n} C_{init, j} x_j - S\right) \times \frac{r(1+r)^y}{(1+r)^y - 1}$$

（ $C_{init, j}$ ：初期投資額、 $S$ ：自己資金、 $r$ ：年利、 $y$ ：返済期間）

**2. 借入限度額制約 (Loan Limit Constraint)**  
総初期投資から自己資金を引いた借入額が、与信枠を超えないこと。

$$\max\left(0, \sum_{j=1}^{n} C_{init, j} x_j - S\right) \le D_{max}$$

*   $D_{max}$：借入限度額。

**3. 土地資源制約 (Land Constraint)**

$$\sum_{j=1}^{n} x_j \le A$$

**4. 月別労働制約 (Monthly Labor Constraints)**  
習熟度で補正された各月の労働需要が、家族労働供給限界を超えないこと。

$$\sum_{j=1}^{n} l'_{jt} x_j \le H_t \quad (\forall t \in \{1, \dots, 12\})$$
*   $l^\prime_{jt} = l_{jt} / k_{skill}$：補正後の月別労働係数。

---

## 3. Pythonによるシミュレーションコード

```python
import numpy as np
from scipy.optimize import minimize

# =========================================================
# 1. パラメータの設定 (Ver.3 新規就農向け)
# =========================================================

crops = ["露地野菜", "施設トマト", "果樹(ブドウ)"]
n_crops = len(crops)

# --- 収益・コストパラメータ (万円/10a) ---
revenue_params = {
    "R_peak": np.array([20.0, 300.0, 150.0]), # 最大単収益
    "R_base": np.array([10.0, 150.0,  50.0]), # 底値単収益
    "P_area": np.array([30.0,  10.0,  15.0])  # ベテランの適正面積(10a)
}
variable_costs = np.array([8.0, 80.0, 30.0])  # 変動費(肥料・農薬・光熱費等)

# --- 労働パラメータ (時間/10a) ---
annual_labor = np.array([30.0, 400.0, 150.0]) # ベテランの年間労働時間
# 月別労働係数 (行:月, 列:作物) ※簡略化のため6ヶ月分
monthly_labor_coeffs = np.array([
    [ 5, 40, 10],[ 5, 40, 20], [ 5, 40, 30],[ 5, 40, 40], [ 5, 40, 30],[ 5, 40, 20]
])

# --- 【追加】イニシャルコストと融資条件 ---
initial_costs = np.array([5.0, 500.0, 200.0]) # 初期投資(万円/10a) ハウスや棚の建設費など
self_capital = 300.0      # 自己資金 (万円)
interest_rate = 0.02      # 融資の年利 (2%)
repayment_years = 15      # 返済期間 (年)
max_loan = 1500.0         # 借入限度額 (万円)

# --- 【追加】新規就農者の状況設定 ---
skill_level = 0.7         # 習熟度 (ベテランの70%の能力)
subsidy = 150.0           # 就農支援の補助金 (万円/年)
living_cost = 300.0       # 最低限必要な生活費 (万円/年)
land_limit = 50.0         # 利用可能面積 (10a)
H_t = 400.0               # 月あたりの労働供給限界 (時間)

# =========================================================
# 2. 内部計算用関数の定義
# =========================================================

# 習熟度によるパラメータ補正
actual_P_area = revenue_params["P_area"] * skill_level
actual_annual_labor = annual_labor / skill_level
actual_monthly_labor = monthly_labor_coeffs / skill_level

# 資本回収係数 (CRF) の計算
if interest_rate > 0:
    CRF = (interest_rate * (1 + interest_rate)**repayment_years) / ((1 + interest_rate)**repayment_years - 1)
else:
    CRF = 1.0 / repayment_years

def calculate_loan_and_pmt(x):
    """面積xに対する借入額と年間返済額を計算"""
    total_initial_cost = np.dot(initial_costs, x)
    loan_amount = max(0, total_initial_cost - self_capital)
    annual_pmt = loan_amount * CRF
    return loan_amount, annual_pmt

def unit_revenue_func(x_val, j):
    """習熟度を反映した単位収益 R(x) を計算"""
    x = max(0, x_val)
    base = revenue_params["R_base"][j]
    peak = revenue_params["R_peak"][j]
    p_val = actual_P_area[j] # 補正後の適正規模を使用
    
    factor = (2 * x * p_val) / (x**2 + p_val**2 + 1e-9)
    return base + (peak - base) * factor

# =========================================================
# 3. 目的関数と制約条件
# =========================================================

def objective(x):
    """目的関数: 補正後総労働時間の最小化"""
    return np.dot(actual_annual_labor, x)

def constraint_cashflow(x):
    """資金繰り制約: (粗利益 + 補助金) - (生活費 + 年間返済額) >= 0"""
    total_gross_margin = sum((unit_revenue_func(x[j], j) - variable_costs[j]) * x[j] for j in range(n_crops))
    _, annual_pmt = calculate_loan_and_pmt(x)
    return (total_gross_margin + subsidy) - (living_cost + annual_pmt)

def constraint_loan_limit(x):
    """借入限度額制約: max_loan - 借入額 >= 0"""
    loan_amount, _ = calculate_loan_and_pmt(x)
    return max_loan - loan_amount

def constraint_land(x):
    """土地制約: land_limit - Σx >= 0"""
    return land_limit - np.sum(x)

def make_labor_constraint(month_idx):
    """月別労働制約: H_t - (その月の労働投入量) >= 0"""
    def cons_labor(x):
        return H_t - np.dot(actual_monthly_labor[month_idx], x)
    return cons_labor

# =========================================================
# 4. 最適化計算の実行
# =========================================================

# 初期値は「新規就農者の適正規模」付近に設定
x0 = actual_P_area.copy()
if np.sum(x0) > land_limit:
    x0 = x0 * (land_limit / np.sum(x0)) * 0.9

bounds =[(0, land_limit) for _ in range(n_crops)]

cons =[
    {'type': 'ineq', 'fun': constraint_cashflow},
    {'type': 'ineq', 'fun': constraint_loan_limit},
    {'type': 'ineq', 'fun': constraint_land}
]

# 月ごとの労働制約を追加
for t in range(len(actual_monthly_labor)):
    cons.append({'type': 'ineq', 'fun': make_labor_constraint(t)})

res = minimize(objective, x0, method='SLSQP', bounds=bounds, constraints=cons)

# =========================================================
# 5. 結果の表示
# =========================================================

if res.success:
    print("=== 新規就農向け 経営シミュレーション 最適解 (Ver.3) ===")
    print(f"前提: 習熟度 {skill_level*100}% / 自己資金 {self_capital}万円 / 補助金 {subsidy}万円/年")
    print("-" * 85)
    print(f"{'作目':<10} | {'面積(10a)':<9} | {'単収益':<8} | {'粗利益/10a':<10} | {'初期投資':<8} | {'状態'}")
    print("-" * 85)
    
    total_gross_margin = 0
    total_labor = 0
    
    for j, crop in enumerate(crops):
        area = res.x[j]
        unit_rev = unit_revenue_func(area, j)
        unit_margin = unit_rev - variable_costs[j]
        init_cost = initial_costs[j] * area
        peak_area = actual_P_area[j]
        
        if area < 0.1: 
            status = "― 作付なし"
        elif abs(area - peak_area) < 1.0: 
            status = "★ 適正規模"
        elif area > peak_area: 
            status = "▼ 規模過多"
        else: 
            status = "▲ 抑制的"

        print(f"{crop:<10} | {area:>9.2f} | {unit_rev:>8.2f} | {unit_margin:>10.2f} | {init_cost:>8.1f} | {status}")
        
        total_gross_margin += unit_margin * area
        total_labor += actual_annual_labor[j] * area

    loan_amount, annual_pmt = calculate_loan_and_pmt(res.x)
    net_cash = (total_gross_margin + subsidy) - annual_pmt
    
    print("-" * 85)
    print(f"【労働・土地】")
    print(f"  年間総労働時間 : {total_labor:>8.1f} 時間 (最小化目的)")
    print(f"  総作付面積     : {np.sum(res.x):>8.1f} / {land_limit} (10a)")
    print(f"【資金繰り】")
    print(f"  総初期投資額   : {np.dot(initial_costs, res.x):>8.1f} 万円")
    print(f"  借入額 (融資)  : {loan_amount:>8.1f} 万円 (限度額: {max_loan}万円)")
    print(f"  年間返済額     : {annual_pmt:>8.1f} 万円 (金利{interest_rate*100}%, {repayment_years}年返済)")
    print(f"  農業粗利益     : {total_gross_margin:>8.1f} 万円")
    print(f"  手元現金(生活費): {net_cash:>8.1f} 万円 (目標: {living_cost}万円)")
    
else:
    print("最適解が見つかりませんでした。")
    print("理由:", res.message)
    print("アドバイス: 初期投資が大きすぎて返済が追いつかないか、生活費の目標が高すぎる可能性があります。")
```

---

## 4. 本モデルがもたらす洞察（新規就農者へのアドバイス機能）

このモデルを動かすことで、新規就農者が陥りがちな以下の罠をシミュレーションで回避・可視化できます。

1. **「施設園芸（ハウス）の罠」の回避**
   施設トマトなどは面積あたりの収益が高いですが、イニシャルコストが莫大です。本モデルでは「ハウスを建てすぎると借金返済（PMT）が膨らみ、結果的にそれを返すために過労（労働時間増大）になる」という現象が数学的に計算され、**「借金返済と労働のバランスが取れるギリギリのハウス面積」** を弾き出します。
2. **「未熟練の罠」の可視化**
   習熟度（`skill_level`）を0.5（ベテランの半分）などに設定すると、適正規模が極端に小さくなります。これにより、「最初は無理に面積を広げず、補助金（`subsidy`）に頼りながら露地野菜などの低投資作物で食いつなぐべき」という堅実なポートフォリオが提案されます。
3. **自己資金の重要性の証明**
   `self_capital`（自己資金）のパラメータを減らすと、「自己資金が少ない状態で高収益・高投資作物に手を出すと、資金繰り制約を満たせず破綻する（最適解なしになる）」ことが明確にわかります。就農前の資金計画の妥当性を検証するツールとして機能します。

## 5. 実装・運用におけるリスクと対策

*   **補助金切れ（クリフ）への対応**:
    就農支援金（`subsidy`）は通常3〜5年で打ち切られます。運用時は、`subsidy = 0` かつ `skill_level = 1.0`（5年後の熟練状態）のシナリオも同時に計算し、「補助金が切れた後でも自立できる経営計画か」を検証することが必須です。
*   **金利変動リスク**:
    日本政策金融公庫などの固定金利を想定していますが、変動金利を利用する場合は `interest_rate` を高めに設定したストレステストを行うことが推奨されます。
