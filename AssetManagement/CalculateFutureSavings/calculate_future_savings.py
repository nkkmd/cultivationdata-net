import numpy as np

# ユーザー入力関数
def get_user_input(prompt, input_type=float):
    while True:
        try:
            return input_type(input(prompt))
        except ValueError:
            print("Invalid input. Please try again.")

# メイン関数
def calculate_savings_goal():
    # ユーザーからの入力
    current_age = get_user_input("現在の年齢を入力してください: ", int)
    target_age = get_user_input("目標年齢を入力してください: ", int)
    target_value = get_user_input("目標金額（現在の価値、万円）を入力してください: ")
    expected_return = get_user_input("期待収益率（%）を入力してください（例: 7）: ") / 100
    inflation_rate = get_user_input("インフレ率（%）を入力してください（例: 1.5）: ") / 100

    # 実質期待収益率を計算 (参考用)
    real_return = (1 + expected_return) / (1 + inflation_rate) - 1

    # 残りの年数を計算
    years_remaining = target_age - current_age

    # 目標年齢時点で必要な金額を計算（インフレ調整後の未来価値）
    future_value = target_value * (1 + inflation_rate) ** years_remaining

    # 目標達成に必要な現在の貯蓄額を計算
    present_value = future_value / (1 + expected_return) ** years_remaining

    # 結果を表示
    print(f"\n=====計算結果=====")
    print(f"現在の年齢: {current_age}歳")
    print(f"目標年齢: {target_age}歳")
    print(f"目標金額: {target_value:.2f}万円")
    print(f"残りの年数: {years_remaining}年")
    print(f"期待収益率: {expected_return:.2%}")
    print(f"インフレ率: {inflation_rate:.2%}")
    print(f"実質期待収益率: {real_return:.2%}")
    print(f"目標達成に必要な現在の貯蓄額: {present_value:.2f}万円")
    print(f"目標年齢時点で必要な金額（インフレ調整後）: {future_value:.2f}万円")

# スクリプトを実行
if __name__ == "__main__":
    calculate_savings_goal()