# 家族経営農業における「適正規模・労働最小化」モデル（Ver.2）のシミュレーションコードと解説

```python
import numpy as np
from scipy.optimize import minimize
import matplotlib.pyplot as plt

# =========================================================
# 1. パラメータの設定
# =========================================================

crops = ["Crop A", "Crop B", "Crop C"] # 英語表記に変更
n_crops = len(crops)
colors = ['#1f77b4', '#ff7f0e', '#2ca02c']

# --- 収益モデルパラメータ ---
revenue_params = {
    "R_peak": np.array([15.0, 20.0, 60.0]), 
    "R_base": np.array([10.0, 12.0, 40.0]),
    "P_area": np.array([30.0, 20.0, 5.0])   
}

variable_costs = np.array([5.0, 8.0, 10.0])    # 万円/10a (変動費)
annual_labor   = np.array([20.0, 25.0, 150.0]) # 時間/10a (年間労働)

# 月別労働係数 (行:月, 列:作物)
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
    """作目jの面積xにおける単位収益 R(x) を計算"""
    x = max(0, x_val)
    base = revenue_params["R_base"][j]
    peak = revenue_params["R_peak"][j]
    p_val = revenue_params["P_area"][j]
    factor = (2 * x * p_val) / (x**2 + p_val**2 + 1e-9)
    return base + (peak - base) * factor

def objective(x):
    """目的関数: 総労働時間の最小化"""
    return np.dot(annual_labor, x)

def constraint_income(x):
    """所得制約: 総粗利益 - I_min >= 0"""
    total_gross_margin = sum((unit_revenue_func(x[j], j) - variable_costs[j]) * x[j] for j in range(n_crops))
    return total_gross_margin - I_min

def constraint_land(x):
    """土地制約: land_limit - Σx >= 0"""
    return land_limit - np.sum(x)

def make_labor_constraint(month_idx):
    """月別労働制約のクロージャ"""
    def cons_labor(x):
        return H_t - np.dot(monthly_labor_coeffs[month_idx], x)
    return cons_labor

# =========================================================
# 3. 最適化計算の実行
# =========================================================

x0 = revenue_params["P_area"].copy() 
if np.sum(x0) > land_limit:
    x0 = x0 * (land_limit / np.sum(x0)) * 0.9

bounds = [(0, land_limit) for _ in range(n_crops)]

cons = [
    {'type': 'ineq', 'fun': constraint_income},
    {'type': 'ineq', 'fun': constraint_land}
]
for t in range(len(monthly_labor_coeffs)):
    cons.append({'type': 'ineq', 'fun': make_labor_constraint(t)})

res = minimize(objective, x0, method='SLSQP', bounds=bounds, constraints=cons)

# =========================================================
# 4. 結果のコンソール表示
# =========================================================

if res.success:
    print("=== Optimal Solution (Ver.2) ===")
    print(f"{'Crop':<6} | {'Area(10a)':<10} | {'Unit Rev':<8} | {'Margin/10a':<10} | {'Peak P':<6} | {'Status'}")
    print("-" * 75)
    
    total_income = 0
    total_labor = 0
    margins = []
    
    for j, crop in enumerate(crops):
        area = res.x[j]
        unit_rev = unit_revenue_func(area, j)
        unit_margin = unit_rev - variable_costs[j]
        peak_area = revenue_params["P_area"][j]
        margins.append(unit_margin * area)
        
        if area < 0.1: status = "- No Planting"
        elif abs(area - peak_area) < 1.0: status = "* Optimal Scale (Peak)"
        elif area > peak_area: status = "v Over Scale (Inefficient)"
        else: status = "^ Restrictive (Labor Saving)"

        print(f"{crop:<6} | {area:>9.2f}  | {unit_rev:>8.2f} | {unit_margin:>10.2f} | {peak_area:>6.1f} | {status}")
        total_income += unit_margin * area
        total_labor += annual_labor[j] * area

    print("-" * 75)
    print(f"Total Annual Labor : {total_labor:>8.1f} hours (Minimized)")
    print(f"Achieved Income    : {total_income:>8.1f} 10k JPY (Target: {I_min})")
    
    # =========================================================
    # 5. 視覚的分析（ダッシュボード描画） - 英語表記
    # =========================================================
    fig = plt.figure(figsize=(14, 10))
    fig.suptitle('Optimal Scale & Labor Minimization Model Dashboard', fontsize=16, fontweight='bold')

    # --- [左上] 作付面積と適正規模の比較 ---
    ax1 = plt.subplot(2, 2, 1)
    x_pos = np.arange(n_crops)
    width = 0.35
    ax1.bar(x_pos - width/2, res.x, width, label='Optimal Area', color='skyblue', edgecolor='black')
    ax1.bar(x_pos + width/2, revenue_params["P_area"], width, label='Peak Area', color='lightcoral', edgecolor='black')
    ax1.set_ylabel('Area (10a)')
    ax1.set_title('1. Optimal Area vs Peak Area')
    ax1.set_xticks(x_pos)
    ax1.set_xticklabels(crops)
    ax1.legend()
    ax1.grid(axis='y', linestyle='--', alpha=0.7)

    # --- [右上] 規模連動型収益モデルと最適解の位置 ---
    ax2 = plt.subplot(2, 2, 2)
    x_vals = np.linspace(0, 50, 200)
    for j, crop in enumerate(crops):
        y_vals = [unit_revenue_func(x, j) for x in x_vals]
        ax2.plot(x_vals, y_vals, label=f'{crop} Revenue Curve', color=colors[j], linewidth=2)
        
        # 最適解のプロット
        opt_x = res.x[j]
        opt_y = unit_revenue_func(opt_x, j)
        ax2.scatter(opt_x, opt_y, color=colors[j], s=150, zorder=5, edgecolors='black', marker='*')
        ax2.annotate(f'{opt_x:.1f}', (opt_x, opt_y), textcoords="offset points", xytext=(0,10), ha='center', fontweight='bold')

    ax2.set_xlabel('Planted Area (10a)')
    ax2.set_ylabel('Unit Gross Revenue (10k JPY/10a)')
    ax2.set_title('2. Revenue Model & Optimal Solution (*)')
    ax2.legend()
    ax2.grid(True, linestyle='--', alpha=0.7)

    # --- [左下] 月別労働時間の消費状況 ---
    ax3 = plt.subplot(2, 2, 3)
    months = [f"Month {i+1}" for i in range(len(monthly_labor_coeffs))]
    bottom = np.zeros(len(months))
    for j, crop in enumerate(crops):
        labor_j = monthly_labor_coeffs[:, j] * res.x[j]
        ax3.bar(months, labor_j, bottom=bottom, label=crop, color=colors[j], alpha=0.8, edgecolor='black')
        bottom += labor_j

    ax3.axhline(y=H_t, color='red', linestyle='--', linewidth=2, label=f'Labor Limit ({H_t}h)')
    ax3.set_ylabel('Labor Hours')
    ax3.set_title('3. Monthly Labor Consumption')
    ax3.legend()
    ax3.grid(axis='y', linestyle='--', alpha=0.7)

    # --- [右下] 粗利益の構成と目標達成状況 ---
    ax4 = plt.subplot(2, 2, 4)
    bottom_margin = 0
    for j, crop in enumerate(crops):
        ax4.bar(['Total Gross Margin'], [margins[j]], bottom=bottom_margin, label=crop, color=colors[j], width=0.4, alpha=0.8, edgecolor='black')
        if margins[j] > 10: 
            ax4.text(0, bottom_margin + margins[j]/2, f'{margins[j]:.1f}', ha='center', va='center', color='white', fontweight='bold')
        bottom_margin += margins[j]

    ax4.axhline(y=I_min, color='red', linestyle='--', linewidth=2, label=f'Target Income ({I_min})')
    ax4.set_xlim(-0.5, 0.5)
    ax4.set_ylabel('Amount (10k JPY)')
    ax4.set_title('4. Gross Margin Composition & Target')
    ax4.legend(loc='upper right')
    ax4.grid(axis='y', linestyle='--', alpha=0.7)

    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    plt.show()
    # plt.savefig("dashboard.png", dpi=300) # 保存する場合

else:
    print("Optimization failed.")
    print("Reason:", res.message)
```

このプログラムは、大きく分けて以下の5つのブロックで構成されています。

## 1. パラメータの設定（農家の条件を決める）
ここでは、シミュレーションの前提となる「農家の現状や条件」を入力しています。

*   **作物と色**: 3つの作物（Crop A, B, C）を育てます。グラフ用に色も決めています。
*   **収益モデル (`revenue_params`)**: ここがこのモデルの最大の特徴です。
    *   `P_area` (適正規模): この面積で作るのが一番効率が良い（儲かる）というピークの面積です。
    *   `R_peak` (最大単収益): 適正規模で作ったときの、面積あたりの最高の売上です。
    *   `R_base` (底値単収益): 面積を広げすぎて管理が行き届かなくなったときの、最低ラインの売上です。
*   **コストと労働時間**: 作物ごとの変動費（肥料代など）や、年間・月ごとの労働時間を設定しています。
*   **経営の絶対条件**:
    *   `I_min = 500`: 最低でも**500万円**の利益を出さなければならない（目標所得）。
    *   `land_limit = 100`: 畑の広さは最大**100**（10a）まで。
    *   `H_t = 400`: 1ヶ月に働ける限界は**400時間**まで。

## 2. 関数定義（計算のルールを決める）
ここでは、コンピュータに計算させるための「ルール（数式）」を定義しています。

*   **`unit_revenue_func` (収益の計算)**: 「面積を広げすぎると、単位面積あたりの売上が落ちる」という現実的な現象（収穫逓減）を計算する数式です。
*   **`objective` (目的)**: このプログラムの最終目標です。**「年間の総労働時間を最小にする」** ように設定されています。
*   **`constraint_...` (守るべきルール)**: 目的を達成するためでも、破ってはいけないルールです。
    *   **所得制約**: 利益は絶対に目標（500万円）以上であること。
    *   **土地制約**: 持っている畑の面積を超えないこと。
    *   **労働制約**: どの月も、労働の限界（400時間）を超えないこと。

## 3. 最適化計算の実行（ベストな答えを探す）
設定した条件とルールをもとに、Pythonの強力な計算ツール（`scipy.optimize`）を使って、**「条件をすべてクリアしつつ、一番労働時間が短くなる作付面積の組み合わせ」** を全自動で探し出します。

*   `x0`: 計算のスタート地点です。最初から面積0で計算を始めると「作っても赤字だ」とコンピュータが勘違いすることがあるため、一番効率の良い「適正規模」付近から計算をスタートさせる工夫がされています。

## 4. 結果のコンソール表示（文字で結果を報告）
計算が無事に終わったら、その結果を画面（ターミナル）に文字で出力します。

*   各作物を「どれくらいの面積で作るべきか」「その時の売上や利益はいくらか」を表示します。
*   また、その面積が適正規模に対してどういう状態か（ピーク維持、規模過多、労働節約など）を判定して教えてくれます。
*   最後に、トータルの労働時間と達成した利益を表示します。

## 5. 視覚的分析（ダッシュボード描画）
文字だけでは分かりにくいため、計算結果を4つのグラフにして1枚の画像（ダッシュボード）にまとめます。

### 4つのグラフの見方
1.  **左上 (Optimal Area vs Peak Area)**
    *   青い棒が「今回計算された最適な面積」、赤い棒が「一番効率が良い適正面積」です。無理に広げすぎていないかが一目でわかります。
2.  **右上 (Revenue Model & Optimal Solution)**
    *   山の形をした線が「面積と収益性の関係」を表します。星マーク（★）が今回の最適解です。星が山の頂上付近にあれば、「一番おいしいところ（高収益）を狙って作付けしている」ことがわかります。
3.  **左下 (Monthly Labor Consumption)**
    *   月ごとの労働時間を積み上げ棒グラフで示しています。赤い点線が「労働の限界（400時間）」です。どの月が一番忙しいか（ボトルネックになっているか）がわかります。
4.  **右下 (Gross Margin Composition & Target)**
    *   各作物がどれくらい利益に貢献しているかを示します。赤い点線が「目標所得（500万円）」です。目標をギリギリ達成するラインで面積の拡大をストップしている（無駄働きをしていない）ことが確認できます。
