# 青果物市況情報データ取得コード

最終更新日: 2026-06-24

このドキュメントは、cultivationdata.net の Web API を使わず、利用者自身の環境で農林水産省の「青果物市況情報」を取得するための説明と Python コードをまとめたものです。

元データ:

https://www.seisen.maff.go.jp/seisen/bs04b040md001/BS04B040UC010SC999-Evt001.do

## このコードでできること

- 農林水産省の青果物市況情報ページから最新の掲載日を取得します。
- 最新日の市場別 CSV 帳票一覧を取得します。
- 各市場の CSV を読み込み、日付・市場・品目・産地・価格などの列に整形します。
- 市場コード、種別、品目コードで絞り込めます。
- CSV または JSON として保存します。
- 必要に応じて SQLite データベースにも保存できます。

## API 版との関係

現在の Web API では、主に次のファイルを使っています。

- `get_mcdata.py`: 農林水産省の CSV を取得し、SQLite に保存する処理
- `api_mcdata.py`: SQLite に保存されたデータを JSON または CSV で返す処理

このドキュメントのコードは、API サーバーを立てず、利用者が手元で直接データを取得・保存できるようにした単体スクリプトです。

## 動作環境

Python 3.10 以上を想定しています。

必要なライブラリをインストールします。

```bash
python -m pip install requests beautifulsoup4 pandas
```

## 使い方

全市場の最新データを CSV に保存します。

```bash
python get_mcdata.py --format csv --output mcdata_latest.csv
```

東京都中央卸売市場大田市場の野菜だけを JSON に保存します。

```bash
python get_mcdata.py --market 13310 --cat v --format json --output mcdata_13310_vegetables.json
```

東京都中央卸売市場大田市場のだいこんだけを CSV に保存します。

```bash
python get_mcdata.py --market 13310 --item 30100 --format csv --output mcdata_13310_daikon.csv
```

SQLite にも保存します。

```bash
python get_mcdata.py --format csv --output mcdata_latest.csv --sqlite mcdata.db
```

`--cat` は `v` が野菜、`f` が果実です。`--item` を指定した場合は、品目コードで絞り込みます。

## Python コード

```python
#!/usr/bin/env python3

import argparse
import io
import json
import re
import sqlite3
import sys
from pathlib import Path

import pandas as pd
import requests
from bs4 import BeautifulSoup


LATEST_PAGE_URL = "https://www.seisen.maff.go.jp/seisen/bs04b040md001/BS04B040UC010SC999-Evt001.do"
REPORT_LIST_URL = "https://www.seisen.maff.go.jp/seisen/bs04b040md001/BS04B040UC010SC001-Evt001.do?s006.dataDate={date}"
CSV_URL = "https://www.seisen.maff.go.jp/seisen/bs04b040md001/BS04B040UC010SC001-Evt004.do?s004.chohyoKanriNo={report_no}"

COLUMNS = [
    "date",
    "market",
    "market_code",
    "item",
    "item_code",
    "area",
    "area_code",
    "items_total",
    "incoming_volume",
    "high_price",
    "medium_price",
    "low_price",
    "grade",
    "class",
    "variety_name",
    "weight_per_package",
    "trend",
    "category",
]

CSV_COLUMNS_JA = {
    "date": "日付",
    "market": "市場名",
    "market_code": "市場コード",
    "item": "品目名",
    "item_code": "品目コード",
    "area": "産地名",
    "area_code": "産地コード",
    "items_total": "品目計(t)",
    "incoming_volume": "入荷量(t)",
    "high_price": "高値(円)",
    "medium_price": "中値(円)",
    "low_price": "安値(円)",
    "grade": "等級",
    "class": "階級",
    "variety_name": "品名",
    "weight_per_package": "量目(Kg)",
    "trend": "動向",
    "category": "種別",
}


def fetch_soup(url):
    response = requests.get(url, timeout=30)
    response.raise_for_status()
    response.encoding = response.apparent_encoding
    return BeautifulSoup(response.text, "html.parser")


def fetch_latest_date():
    soup = fetch_soup(LATEST_PAGE_URL)
    anchor = soup.find("a", href=re.compile("s0070"))

    if anchor is None:
        raise RuntimeError("最新日のリンクが見つかりませんでした。")

    numbers = re.findall(r"\d+", anchor.get_text(" ", strip=True))
    if len(numbers) < 3:
        raise RuntimeError("最新日を読み取れませんでした。")

    year, month, day = numbers[:3]
    return f"{int(year):04d}{int(month):02d}{int(day):02d}"


def fetch_report_numbers(date):
    soup = fetch_soup(REPORT_LIST_URL.format(date=date))
    report_numbers = []

    for anchor in soup.find_all("a", href=re.compile("form003")):
        match = re.search(r"chohyoSubmit\('form003','([^']+)'\)", str(anchor))
        if match:
            report_numbers.append(match.group(1))

    if not report_numbers:
        raise RuntimeError("CSV 帳票番号が見つかりませんでした。")

    return report_numbers


def read_report_csv(report_no):
    url = CSV_URL.format(report_no=report_no)
    response = requests.get(url, timeout=30)
    response.raise_for_status()
    return pd.read_csv(io.BytesIO(response.content), encoding="cp932").values.tolist()


def normalize_code(value, width):
    text = str(value).replace(".0", "").strip()
    if text == "nan":
        text = ""
    return text.zfill(width)


def normalize_text(value):
    text = str(value).replace("\u3000", "").strip()
    return "" if text == "nan" else text


def category_from_item_code(item_code):
    if item_code.startswith("3"):
        return "野菜"
    if item_code.startswith("4"):
        return "果実"
    return "不明"


def rows_from_report(records):
    if not records:
        return []

    date = f"{int(records[0][0]):04d}/{int(records[0][1]):02d}/{int(records[0][2]):02d}"
    market = normalize_text(records[0][4])
    market_code = normalize_code(records[0][5], 5)
    rows = []

    for record in records:
        item_code = normalize_code(record[7], 5)
        row = {
            "date": date,
            "market": market,
            "market_code": market_code,
            "item": normalize_text(record[6]),
            "item_code": item_code,
            "area": normalize_text(record[8]),
            "area_code": normalize_code(record[9], 3),
            "items_total": normalize_text(record[10]),
            "incoming_volume": normalize_text(record[11]),
            "high_price": normalize_text(record[12]),
            "medium_price": normalize_text(record[13]),
            "low_price": normalize_text(record[14]),
            "grade": normalize_text(record[15]),
            "class": normalize_text(record[16]),
            "variety_name": normalize_text(record[17]),
            "weight_per_package": normalize_text(record[18]),
            "trend": normalize_text(record[19]),
            "category": category_from_item_code(item_code),
        }
        rows.append(row)

    return rows


def fetch_mcdata():
    date = fetch_latest_date()
    report_numbers = fetch_report_numbers(date)
    rows = []

    for report_no in report_numbers:
        records = read_report_csv(report_no)
        rows.extend(rows_from_report(records))

    if not rows:
        raise RuntimeError("データを取得できませんでした。")

    return pd.DataFrame(rows, columns=COLUMNS)


def filter_data(df, market=None, cat=None, item=None):
    result = df.copy()

    if market:
        result = result[result["market_code"] == str(market).zfill(5)]

    if item:
        result = result[result["item_code"] == str(item).zfill(5)]
    elif cat:
        category = {"v": "野菜", "f": "果実"}.get(cat, cat)
        result = result[result["category"] == category]

    return result.reset_index(drop=True)


def to_api_style_json(df):
    if df.empty:
        return {"Error": "市場のデータが見つかりませんでした。"}

    first = df.iloc[0]
    output = {
        "Date": first["date"],
        "MarketName": first["market"],
        "MarketCode": first["market_code"],
    }

    for _, row in df.iterrows():
        item_name = row["item"]
        area_name = row["area"]

        output.setdefault(item_name, {"ItemCode": row["item_code"]})
        output[item_name][area_name] = {
            "ProductionAreaCode": row["area_code"],
            "ItemsTotal": row["items_total"],
            "IncomingVolume": row["incoming_volume"],
            "HighPrice": row["high_price"],
            "MediumPrice": row["medium_price"],
            "LowPrice": row["low_price"],
            "Grade": row["grade"],
            "Class": row["class"],
            "VarietyName": row["variety_name"],
            "WeightPerPackage": row["weight_per_package"],
            "MarketTrend": row["trend"],
        }

    return output


def save_csv(df, output_path):
    df.rename(columns=CSV_COLUMNS_JA).to_csv(output_path, index=False, encoding="utf-8-sig")


def save_json(df, output_path):
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(to_api_style_json(df), f, ensure_ascii=False, indent=2)


def save_sqlite(df, sqlite_path):
    db_df = df.rename(
        columns={
            "date": "t_mcdata_date",
            "market": "t_mcdata_market",
            "market_code": "t_mcdata_market_code",
            "item": "t_mcdata_item",
            "item_code": "t_mcdata_item_code",
            "area": "t_mcdata_area",
            "area_code": "t_mcdata_area_code",
            "items_total": "t_mcdata_items_total",
            "incoming_volume": "t_mcdata_incoming_volume",
            "high_price": "t_mcdata_high_price",
            "medium_price": "t_mcdata_medium_price",
            "low_price": "t_mcdata_low_price",
            "grade": "t_mcdata_grade",
            "class": "t_mcdata_class",
            "variety_name": "t_mcdata_variety_name",
            "weight_per_package": "t_mcdata_weight_per_package",
            "trend": "t_mcdata_trend",
            "category": "t_mcdata_category",
        }
    )

    with sqlite3.connect(sqlite_path) as conn:
        db_df.to_sql("t_mcdata", conn, if_exists="replace", index=False)


def parse_args():
    parser = argparse.ArgumentParser(description="農林水産省の青果物市況情報を取得します。")
    parser.add_argument("--market", help="市場コードで絞り込みます。例: 13310")
    parser.add_argument("--cat", choices=["v", "f"], help="種別で絞り込みます。v=野菜、f=果実")
    parser.add_argument("--item", help="品目コードで絞り込みます。例: 30100")
    parser.add_argument("--format", choices=["csv", "json"], default="csv", help="出力形式")
    parser.add_argument("--output", default=None, help="出力ファイル名")
    parser.add_argument("--sqlite", default=None, help="SQLite にも保存する場合のDBファイル名")
    return parser.parse_args()


def main():
    args = parse_args()
    df = fetch_mcdata()
    df = filter_data(df, market=args.market, cat=args.cat, item=args.item)

    output_path = args.output or f"mcdata_latest.{args.format}"
    output_path = Path(output_path)

    if args.format == "csv":
        save_csv(df, output_path)
    else:
        save_json(df, output_path)

    if args.sqlite:
        save_sqlite(df, args.sqlite)

    print(f"Rows: {len(df)}")
    print(f"Saved: {output_path}")

    if args.sqlite:
        print(f"SQLite: {args.sqlite}")


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print(f"エラー: {exc}", file=sys.stderr)
        sys.exit(1)
```

## 出力されるデータ

CSV では次の列名で出力します。

```text
日付,市場名,市場コード,品目名,品目コード,産地名,産地コード,品目計(t),入荷量(t),高値(円),中値(円),安値(円),等級,階級,品名,量目(Kg),動向,種別
```

JSON は現在の Web API に近い形で、日付・市場情報のあとに、品目名、産地名の順で階層化します。

```json
{
  "Date": "2026/06/24",
  "MarketName": "東京都中央卸売市場大田市場",
  "MarketCode": "13310",
  "だいこん": {
    "ItemCode": "30100",
    "北海道": {
      "ProductionAreaCode": "001",
      "ItemsTotal": "12.3",
      "IncomingVolume": "4.5",
      "HighPrice": "1000",
      "MediumPrice": "800",
      "LowPrice": "600",
      "Grade": "A",
      "Class": "L",
      "VarietyName": "",
      "WeightPerPackage": "10",
      "MarketTrend": ""
    }
  }
}
```

上の値は形式説明用の例です。実際の値は取得時点の農林水産省公開データに従います。

## 主なパラメータ

| パラメータ | 内容 | 例 |
| --- | --- | --- |
| `--market` | 市場コード | `13310` |
| `--cat` | 種別。`v` は野菜、`f` は果実 | `v` |
| `--item` | 品目コード | `30100` |
| `--format` | 出力形式 | `csv` / `json` |
| `--sqlite` | SQLite保存先 | `mcdata.db` |

## 注意点

- 農林水産省側のページ構成、フォーム名、CSV列構成が変更された場合、このコードの修正が必要になることがあります。
- 取得元サイトに負荷をかけないよう、短時間に何度も実行する使い方は避けてください。
- cultivationdata.net の API 説明では、青果物市況情報は17時頃に更新されると案内しています。
- エラー回避のため、数値に見える値も文字列として扱っています。
- SQLite 保存は、既存 API 側のテーブル名 `t_mcdata` と列名に寄せています。
