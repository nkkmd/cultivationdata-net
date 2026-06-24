# 2週間気温予報データ取得コード

最終更新日: 2026-06-24

このドキュメントは、cultivationdata.net の Web API を使わず、利用者自身の環境で気象庁の「2週間気温予報」を取得するための説明と Python コードをまとめたものです。

元データ:

https://www.data.jma.go.jp/risk/probability/guidance/csv_k2w.php

## このコードでできること

- 気象庁の確率予測資料（2週間気温予報）CSVを取得します。
- 地域（地点）番号を指定して、2週間気温予報の平均・最高・最低気温を取得します。
- 予報値、平年値、過去10年平均、昨年値を JSON または CSV として保存します。
- 気温は、初期日からの13日間をそれぞれ起点とした5日間平均です。

## API 版との関係

現在の Web API では、`weather_twoweek.py` の `getTwoweekData(no)` がこの取得処理を担当しています。このドキュメントのコードは、APIサーバーを立てず、利用者が手元で直接データを取得・保存できるようにした単体スクリプトです。

## 動作環境

Python 3.10 以上を想定しています。

必要なライブラリをインストールします。

```bash
python -m pip install pandas
```

## 使い方

小名浜の2週間気温予報を JSON に保存します。

```bash
python get_weather_twoweek.py --no 47598 --format json --output twoweek_47598.json
```

CSV に保存します。

```bash
python get_weather_twoweek.py --no 47598 --format csv --output twoweek_47598.csv
```

`--no` に指定する地域（地点）番号は、アメダス観測所番号とは異なります。

## Python コード

```python
#!/usr/bin/env python3

import argparse
import json
import sys
import time
from pathlib import Path

import pandas as pd


CSV_URL = "https://www.data.jma.go.jp/risk/probability/guidance/download2w.php?2week_t_{no}.csv"


def normalize_value(value):
    if value <= -1000:
        return None
    return value / 10


def get_twoweek_data(no):
    time.sleep(1)
    url = CSV_URL.format(no=no)
    df = pd.read_csv(
        url,
        encoding="UTF-8",
        header=None,
        skiprows=1,
        usecols=[0, 1, 2, 10, 212, 213, 214],
        engine="python",
    )
    data = df.values.tolist()

    result = {
        "date": [f"{data[0][0]}/{data[0][1]}/{data[0][2]}"],
        "forecast": {},
        "normal": {},
        "last10Y": {},
        "lastY": {},
    }

    for i in range(39):
        if i < 13:
            prefix = "ave"
            day_index = i
        elif i < 26:
            prefix = "hi"
            day_index = i - 13
        else:
            prefix = "low"
            day_index = i - 26

        key = f"{prefix}{day_index}"
        result["forecast"][key] = [(data[i][3] + data[i][6]) / 10]
        result["normal"][key] = [data[i][6] / 10]

        last10y = normalize_value(data[i][5])
        if last10y is not None:
            result["last10Y"][key] = [last10y]

        lasty = normalize_value(data[i][4])
        if lasty is not None:
            result["lastY"][key] = [lasty]

    return result


def rows_for_csv(data):
    rows = []
    initial_date = data["date"][0]

    for kind, label in [("ave", "平均気温"), ("hi", "最高気温"), ("low", "最低気温")]:
        for i in range(13):
            key = f"{kind}{i}"
            rows.append(
                {
                    "初期日": initial_date,
                    "区分": label,
                    "起算日": i,
                    "予報": data["forecast"].get(key, [None])[0],
                    "平年値": data["normal"].get(key, [None])[0],
                    "過去10年平均": data["last10Y"].get(key, [None])[0],
                    "昨年値": data["lastY"].get(key, [None])[0],
                }
            )

    return rows


def save_json(data, output_path):
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def save_csv(data, output_path):
    pd.DataFrame(rows_for_csv(data)).to_csv(output_path, index=False, encoding="utf-8-sig")


def parse_args():
    parser = argparse.ArgumentParser(description="気象庁の2週間気温予報を取得します。")
    parser.add_argument("--no", required=True, help="地域（地点）番号。例: 47598")
    parser.add_argument("--format", choices=["json", "csv"], default="json", help="出力形式")
    parser.add_argument("--output", default=None, help="出力ファイル名")
    return parser.parse_args()


def main():
    args = parse_args()
    data = get_twoweek_data(args.no)
    output_path = Path(args.output or f"weather_twoweek_{args.no}.{args.format}")

    if args.format == "json":
        save_json(data, output_path)
    else:
        save_csv(data, output_path)

    print(f"Saved: {output_path}")


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print(f"エラー: {exc}", file=sys.stderr)
        sys.exit(1)
```

## 出力されるデータ

JSON は現在の Web API と同じように、`forecast`、`normal`、`last10Y`、`lastY` を持つ形式です。

```json
{
  "date": ["2026/6/24"],
  "forecast": {
    "ave0": [20.1],
    "hi0": [25.3],
    "low0": [16.4]
  },
  "normal": {
    "ave0": [19.8]
  },
  "last10Y": {
    "ave0": [20.2]
  },
  "lastY": {
    "ave0": [21.0]
  }
}
```

上の値は形式説明用の例です。実際の値は取得時点の気象庁公開データに従います。

## 主なキー

| キー | 内容 |
| --- | --- |
| `ave0` から `ave12` | 平均気温 |
| `hi0` から `hi12` | 最高気温 |
| `low0` から `low12` | 最低気温 |
| `forecast` | 予報値 |
| `normal` | 平年値 |
| `last10Y` | 過去10年平均 |
| `lastY` | 昨年値 |

## 注意点

- 気象庁側のCSV形式や列位置が変更された場合、このコードの修正が必要になることがあります。
- 取得元サイトに負荷をかけないよう、短時間に何度も実行する使い方は避けてください。
- cultivationdata.net の API 説明では、2週間気温予報は毎日9時30分頃までに更新されると案内しています。
- 地域（地点）番号はアメダスの観測所番号とは異なります。
- このコードは気象庁の公開CSVを整形するもので、独自に予想を行うものではありません。
