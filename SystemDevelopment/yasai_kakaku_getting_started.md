# 食品価格動向調査(野菜)データ取得コード

最終更新日: 2026-06-24

このドキュメントは、cultivationdata.net の Web API を使わず、利用者自身の環境で農林水産省の「食品価格動向調査(野菜)」を取得するための説明と Python コードをまとめたものです。

元データは農林水産省の次のページで公開されています。

https://www.maff.go.jp/j/zyukyu/anpo/kouri/k_yasai/h22index.html

農林水産省のページでは、キャベツ、ねぎ、レタス、ばれいしょ、たまねぎ、きゅうり、トマト、にんじん、はくさい、だいこんの10品目について、小売価格の調査結果が公開されています。

## このコードでできること

- 農林水産省の公開ページから Excel ファイルへのリンクを探します。
- Excel ファイルを読み込み、週ごとの野菜価格データだけを抽出します。
- 和暦表記の週を西暦の日付に変換します。
- CSV または JSON として保存します。
- 必要に応じて SQLite データベースにも保存できます。

## API 版との関係

現在の Web API では、リポジトリ内の主に次の2ファイルを使っています。

- `get_yasai_kakaku.py`: 農林水産省のページから Excel を取得し、SQLite に保存する処理
- `yasai_kakaku.py`: SQLite に保存されたデータを API 用に JSON または CSV で返す処理

利用者が自分でデータを取得するだけであれば、API サーバーや常駐プロセスは不要です。そのため、下のサンプルコードでは「取得」「整形」「保存」を1つのスクリプトにまとめています。

## 動作環境

Python 3.10 以上を想定しています。

必要なライブラリをインストールします。

```bash
python -m pip install requests beautifulsoup4 pandas openpyxl
```

## 使い方

次のコードを `get_yasai_kakaku.py` などの名前で保存して実行します。

最新データだけを CSV に保存する例です。

```bash
python get_yasai_kakaku.py --latest --format csv --output yasai_kakaku_latest.csv
```

全件データを JSON に保存する例です。

```bash
python get_yasai_kakaku.py --all --format json --output yasai_kakaku_all.json
```

全件データを SQLite に保存する例です。

```bash
python get_yasai_kakaku.py --all --format csv --output yasai_kakaku_all.csv --sqlite yasai_kakaku.db
```

## Python コード

```python
#!/usr/bin/env python3

import argparse
import json
import re
import sqlite3
import sys
import urllib.parse
from datetime import datetime
from pathlib import Path

import pandas as pd
import requests
from bs4 import BeautifulSoup


SOURCE_URL = "https://www.maff.go.jp/j/zyukyu/anpo/kouri/k_yasai/h22index.html"

COLUMNS = [
    "week",
    "kyabetsu",
    "negi",
    "retasu",
    "bareisyo",
    "tamanegi",
    "kyuuri",
    "tomato",
    "ninjin",
    "hakusai",
    "daikon",
]

CSV_COLUMNS_JA = {
    "week": "週",
    "kyabetsu": "キャベツ",
    "negi": "ねぎ",
    "retasu": "レタス",
    "bareisyo": "ばれいしょ",
    "tamanegi": "たまねぎ",
    "kyuuri": "きゅうり",
    "tomato": "トマト",
    "ninjin": "にんじん",
    "hakusai": "はくさい",
    "daikon": "だいこん",
}

JSON_KEYS = {
    "kyabetsu": "Kyabetsu",
    "negi": "Negi",
    "retasu": "Retasu",
    "bareisyo": "Bareisyo",
    "tamanegi": "Tamanegi",
    "kyuuri": "Kyuuri",
    "tomato": "Tomato",
    "ninjin": "Ninjin",
    "hakusai": "Hakusai",
    "daikon": "Daikon",
}


def fetch_excel_links(source_url):
    response = requests.get(source_url, timeout=30)
    response.raise_for_status()
    response.encoding = response.apparent_encoding

    soup = BeautifulSoup(response.text, "html.parser")
    links = []

    for anchor in soup.find_all("a", href=True):
        href = anchor["href"]
        text = anchor.get_text(strip=True)

        if ".xlsx" not in href.lower():
            continue

        full_url = urllib.parse.urljoin(source_url, href)
        links.append({"url": full_url, "text": text})

    return links


def choose_excel_link(links):
    if not links:
        raise RuntimeError("Excel ファイルへのリンクが見つかりませんでした。")

    for link in links:
        if "価格推移" in link["text"] or "バックアップ" in link["text"]:
            return link["url"]

    return links[0]["url"]


def convert_reiwa_week_to_date(value):
    text = str(value)
    match = re.match(r"令和(\d+)年(\d+)月(\d+)日の週", text)
    if not match:
        return text

    reiwa_year = int(match.group(1))
    month = int(match.group(2))
    day = int(match.group(3))
    year = reiwa_year + 2018

    return f"{year:04d}/{month:02d}/{day:02d}"


def read_price_data(excel_url):
    df = pd.read_excel(excel_url, header=None)

    week_pattern = r"令和\d+年\d+月\d+日の週"
    week_rows = df[0].astype(str).str.match(week_pattern)
    result = df[week_rows & (df.index >= 2)].iloc[:, 0:11].copy()

    if result.empty:
        raise RuntimeError("Excel から野菜価格データを抽出できませんでした。")

    result.columns = COLUMNS
    result["week"] = result["week"].apply(convert_reiwa_week_to_date)

    return result.reset_index(drop=True)


def to_api_style_json(df):
    output = {}

    for _, row in df.iterrows():
        week = row["week"]
        output[week] = {}

        for column, json_key in JSON_KEYS.items():
            value = row[column]
            output[week][json_key] = normalize_json_value(value)

    return output


def normalize_json_value(value):
    if pd.isna(value):
        return None

    if hasattr(value, "item"):
        return value.item()

    return value


def save_csv(df, output_path):
    csv_df = df.rename(columns=CSV_COLUMNS_JA)
    csv_df.to_csv(output_path, index=False, encoding="utf-8-sig")


def save_json(df, output_path):
    data = to_api_style_json(df)

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def save_sqlite(df, sqlite_path):
    db_df = df.copy()
    db_df["inserted_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    db_df = db_df.rename(
        columns={
            "week": "t_kakaku_week",
            "kyabetsu": "t_kakaku_kyabetsu",
            "negi": "t_kakaku_negi",
            "retasu": "t_kakaku_retasu",
            "bareisyo": "t_kakaku_bareisyo",
            "tamanegi": "t_kakaku_tamanegi",
            "kyuuri": "t_kakaku_kyuuri",
            "tomato": "t_kakaku_tomato",
            "ninjin": "t_kakaku_ninjin",
            "hakusai": "t_kakaku_hakusai",
            "daikon": "t_kakaku_daikon",
        }
    )

    with sqlite3.connect(sqlite_path) as conn:
        db_df.to_sql("t_kakaku", conn, if_exists="replace", index_label="t_kakaku_id")


def parse_args():
    parser = argparse.ArgumentParser(
        description="農林水産省の食品価格動向調査(野菜)を取得します。"
    )

    target = parser.add_mutually_exclusive_group()
    target.add_argument("--latest", action="store_true", help="最新の1週分だけ出力します。")
    target.add_argument("--all", action="store_true", help="全件を出力します。")

    parser.add_argument(
        "--format",
        choices=["csv", "json"],
        default="csv",
        help="出力形式を指定します。初期値は csv です。",
    )
    parser.add_argument(
        "--output",
        default=None,
        help="出力ファイル名を指定します。省略時は形式に応じて自動設定します。",
    )
    parser.add_argument(
        "--sqlite",
        default=None,
        help="SQLite にも保存する場合はデータベースファイル名を指定します。",
    )

    return parser.parse_args()


def main():
    args = parse_args()

    excel_links = fetch_excel_links(SOURCE_URL)
    excel_url = choose_excel_link(excel_links)
    df = read_price_data(excel_url)

    if args.latest or not args.all:
        df = df.tail(1).copy()

    output_path = args.output
    if output_path is None:
        suffix = "csv" if args.format == "csv" else "json"
        scope = "latest" if args.latest or not args.all else "all"
        output_path = f"yasai_kakaku_{scope}.{suffix}"

    output_path = Path(output_path)

    if args.format == "csv":
        save_csv(df, output_path)
    else:
        save_json(df, output_path)

    if args.sqlite:
        save_sqlite(df, args.sqlite)

    print(f"Excel URL: {excel_url}")
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
週,キャベツ,ねぎ,レタス,ばれいしょ,たまねぎ,きゅうり,トマト,にんじん,はくさい,だいこん
```

JSON では現在の Web API と同じように、週をキーにして各品目の値を持つ形式にしています。

```json
{
  "2026/06/15": {
    "Kyabetsu": 123,
    "Negi": 456,
    "Retasu": 789,
    "Bareisyo": 234,
    "Tamanegi": 345,
    "Kyuuri": 456,
    "Tomato": 567,
    "Ninjin": 678,
    "Hakusai": 789,
    "Daikon": 890
  }
}
```

上の数値は形式説明用の例です。実際の値は取得時点の農林水産省公開データに従います。

## 品目キー

| 日本語 | CSV列名 | JSONキー |
| --- | --- | --- |
| キャベツ | キャベツ | Kyabetsu |
| ねぎ | ねぎ | Negi |
| レタス | レタス | Retasu |
| ばれいしょ | ばれいしょ | Bareisyo |
| たまねぎ | たまねぎ | Tamanegi |
| きゅうり | きゅうり | Kyuuri |
| トマト | トマト | Tomato |
| にんじん | にんじん | Ninjin |
| はくさい | はくさい | Hakusai |
| だいこん | だいこん | Daikon |

## 注意点

- 農林水産省のページ構成や Excel の表形式が変更された場合、このコードの修正が必要になることがあります。
- 取得元サイトに負荷をかけないよう、短時間に何度も実行する使い方は避けてください。
- このコードは公開ページに掲載されている Excel ファイルを取得して整形するものです。データの内容や更新日は農林水産省の公開情報を確認してください。
- SQLite 保存は、既存 API 側のテーブル名 `t_kakaku` と列名に寄せています。独自利用だけであれば CSV または JSON の保存だけでも十分です。

## 既存 API コードとの主な違い

既存の `get_yasai_kakaku.py` は systemd で常駐させ、毎日18時に取得処理を実行する前提です。一方、このドキュメントのコードは利用者が必要なときに手元で実行する前提にしているため、常駐処理やスケジューラを含めていません。

既存の `yasai_kakaku.py` は API から呼び出され、SQLite に保存済みのデータを返します。このドキュメントのコードは API サーバーを立てず、取得したデータを直接ファイルに保存します。
