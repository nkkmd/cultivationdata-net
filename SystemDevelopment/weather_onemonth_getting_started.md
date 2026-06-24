# 1か月気温予報データ取得コード

最終更新日: 2026-06-24

このドキュメントは、cultivationdata.net の Web API を使わず、利用者自身の環境で気象庁の「1か月気温予報」を取得するための説明と Python コードをまとめたものです。

元データ:

https://www.data.jma.go.jp/gmd/risk/probability/guidance/csv_k1.php

## このコードでできること

- 気象庁の確率予測資料（1か月予報気温）CSVを取得します。
- 地点番号を指定して、1か月、1週目、2週目、3から4週目の気温予報を取得します。
- 予測値、昨年値、過去10年平均、平年値を JSON または CSV として保存します。
- 予報対象期間の初日、最終日、日数も取得します。

## API 版との関係

現在の Web API では、`weather_onemonth.py` の `getOnemonthData(no)` がこの取得処理を担当しています。このドキュメントのコードは、APIサーバーを立てず、利用者が手元で直接データを取得・保存できるようにした単体スクリプトです。

## 動作環境

Python 3.10 以上を想定しています。

必要なライブラリをインストールします。

```bash
python -m pip install pandas
```

## 使い方

小名浜の1か月気温予報を JSON に保存します。

```bash
python get_weather_onemonth.py --no 47598 --format json --output onemonth_47598.json
```

CSV に保存します。

```bash
python get_weather_onemonth.py --no 47598 --format csv --output onemonth_47598.csv
```

`--no` に指定する地点番号は、アメダス観測所番号とは異なります。また、地域の予報の取得には対応していません。

## Python コード

```python
#!/usr/bin/env python3

import argparse
import json
import sys
import time
from pathlib import Path

import pandas as pd


CSV_URL = "https://www.data.jma.go.jp/gmd/risk/probability/guidance/download.php?month1_t_{no}.csv"

FORECAST_NAMES = {
    0: "forecast1",
    1: "forecast2",
    2: "forecast3",
    3: "forecast4",
}


def optional_temperature(value):
    if value <= -1000:
        return None
    return value / 10


def get_onemonth_data(no):
    time.sleep(1)
    url = CSV_URL.format(no=no)
    df = pd.read_csv(
        url,
        encoding="UTF-8",
        header=None,
        skiprows=1,
        usecols=[0, 1, 2, 3, 4, 5, 6, 10, 152, 153, 154],
        engine="python",
    )
    data = df.values.tolist()
    result = {}

    for i in range(4):
        row = data[i]
        normal = row[10] / 10
        block = {
            "firstDay": [f"{row[0]}/{row[1]}/{row[2]}"],
            "lastDay": [f"{row[3]}/{row[4]}/{row[5]}"],
            "numberOfDays": [row[6]],
            "temp": [(row[7] + row[10]) / 10],
            "normal": [normal],
        }

        last_y = optional_temperature(row[8])
        if last_y is not None:
            block["lastY"] = [last_y]

        last_10y = optional_temperature(row[9])
        if last_10y is not None:
            block["last10Y"] = [last_10y]

        result[FORECAST_NAMES[i]] = block

    return result


def rows_for_csv(data):
    labels = {
        "forecast1": "1か月",
        "forecast2": "1週目",
        "forecast3": "2週目",
        "forecast4": "3から4週目",
    }
    rows = []

    for key, values in data.items():
        rows.append(
            {
                "区分": labels.get(key, key),
                "初日": values.get("firstDay", [None])[0],
                "最終日": values.get("lastDay", [None])[0],
                "日数": values.get("numberOfDays", [None])[0],
                "予測値": values.get("temp", [None])[0],
                "昨年値": values.get("lastY", [None])[0],
                "過去10年平均": values.get("last10Y", [None])[0],
                "平年値": values.get("normal", [None])[0],
            }
        )

    return rows


def save_json(data, output_path):
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def save_csv(data, output_path):
    pd.DataFrame(rows_for_csv(data)).to_csv(output_path, index=False, encoding="utf-8-sig")


def parse_args():
    parser = argparse.ArgumentParser(description="気象庁の1か月気温予報を取得します。")
    parser.add_argument("--no", required=True, help="地点番号。例: 47598")
    parser.add_argument("--format", choices=["json", "csv"], default="json", help="出力形式")
    parser.add_argument("--output", default=None, help="出力ファイル名")
    return parser.parse_args()


def main():
    args = parse_args()
    data = get_onemonth_data(args.no)
    output_path = Path(args.output or f"weather_onemonth_{args.no}.{args.format}")

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

JSON は現在の Web API と同じように、`forecast1` から `forecast4` のキーを持つ形式です。

```json
{
  "forecast1": {
    "firstDay": ["2026/6/20"],
    "lastDay": ["2026/7/17"],
    "numberOfDays": [28],
    "temp": [22.4],
    "lastY": [23.1],
    "last10Y": [22.8],
    "normal": [21.9]
  }
}
```

上の値は形式説明用の例です。実際の値は取得時点の気象庁公開データに従います。

## 主なキー

| キー | 内容 |
| --- | --- |
| `forecast1` | 1か月 |
| `forecast2` | 1週目 |
| `forecast3` | 2週目 |
| `forecast4` | 3から4週目 |
| `temp` | 予測値 |
| `lastY` | 昨年値 |
| `last10Y` | 過去10年平均 |
| `normal` | 平年値 |

## 注意点

- 気象庁側のCSV形式や列位置が変更された場合、このコードの修正が必要になることがあります。
- 取得元サイトに負荷をかけないよう、短時間に何度も実行する使い方は避けてください。
- cultivationdata.net の API 説明では、1か月気温予報は毎週木曜日9時30分頃までに更新されると案内しています。
- 地点番号はアメダスの観測所番号とは異なります。
- このコードは気象庁の公開CSVを整形するもので、独自に予想を行うものではありません。
