# 青果物卸売市場調査（日別調査）データ取得コード

最終更新日: 2026-06-24

このドキュメントは、cultivationdata.net の Web API を使わず、利用者自身の環境で農林水産省の「青果物卸売市場調査（日別調査）」を取得するための説明と Python コードをまとめたものです。

参考ページ:

https://www.cultivationdata.net/mc-web-api.html

元データ:

https://www.seisen.maff.go.jp/seisen/bs04b040md001/BS04B040UC020SC998-Evt001.do

## このコードでできること

- 農林水産省の青果物卸売市場調査（日別調査）ページから最新の掲載日を取得します。
- 最新日の都市別 CSV 帳票一覧を取得します。
- 各都市の CSV を読み込み、日付・都市・品目・産地・数量・価格などの列に整形します。
- 都市コード、種別、品目コードで絞り込めます。
- CSV または JSON として保存します。
- 必要に応じて SQLite データベースにも保存できます。

## API 版との関係

現在の Web API では、主に次のファイルを使っています。

- `get_wmr.py`: 農林水産省の CSV を取得し、SQLite に保存する処理
- `api_wmr.py`: SQLite に保存されたデータを JSON または CSV で返す処理

このドキュメントのコードは、API サーバーを立てず、利用者が手元で直接データを取得・保存できるようにした単体スクリプトです。

## 動作環境

Python 3.10 以上を想定しています。

必要なライブラリをインストールします。

```bash
python -m pip install requests beautifulsoup4 pandas
```

## 使い方

全都市の最新データを CSV に保存します。

```bash
python get_wmr.py --format csv --output wmr_latest.csv
```

東京都の野菜だけを JSON に保存します。

```bash
python get_wmr.py --city 1301 --cat v --format json --output wmr_1301_vegetables.json
```

東京都のだいこんだけを CSV に保存します。

```bash
python get_wmr.py --city 1301 --item 30100 --format csv --output wmr_1301_daikon.csv
```

SQLite にも保存します。

```bash
python get_wmr.py --format csv --output wmr_latest.csv --sqlite wmr.db
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


LATEST_PAGE_URL = "https://www.seisen.maff.go.jp/seisen/bs04b040md001/BS04B040UC020SC998-Evt001.do"
REPORT_LIST_URL = "https://www.seisen.maff.go.jp/seisen/bs04b040md001/BS04B040UC020SC001-Evt001.do?s006.dataDate={date}"
CSV_URL = "https://www.seisen.maff.go.jp/seisen/bs04b040md001/BS04B040UC020SC001-Evt005.do?s004.chohyoKanriNo={report_no}"

COLUMNS = [
    "date",
    "city_name",
    "city_code",
    "item",
    "item_code",
    "area",
    "area_code",
    "trading_volume",
    "average_price",
    "volume_versus_previous_day",
    "price_versus_previous_day",
    "category",
]

CSV_COLUMNS_JA = {
    "date": "日付",
    "city_name": "都市名",
    "city_code": "都市コード",
    "item": "品目名",
    "item_code": "品目コード",
    "area": "産地名",
    "area_code": "産地コード",
    "trading_volume": "数量(Kg)",
    "average_price": "価格(円/Kg)",
    "volume_versus_previous_day": "対前日比数量(%)",
    "price_versus_previous_day": "対前日比価格(%)",
    "category": "種別",
}

ITEM_NAMES = {
    "30000": "野菜総量",
    "30100": "だいこん",
    "30200": "かぶ",
    "30300": "にんじん",
    "30400": "ごぼう",
    "30500": "たけのこ",
    "30600": "れんこん",
    "31100": "はくさい",
    "31300": "みずな",
    "31500": "こまつな",
    "31550": "その他の菜類",
    "31560": "ちんげんさい",
    "31700": "キャベツ",
    "31800": "ほうれんそう",
    "31900": "ねぎ",
    "32300": "ふき",
    "32400": "うど",
    "32500": "みつば",
    "32600": "しゅんぎく",
    "32800": "にら",
    "32900": "セルリー",
    "33100": "アスパラガス",
    "33101": "アスパラガス（うち輸入）",
    "33200": "カリフラワー",
    "33300": "ブロッコリー",
    "33301": "ブロッコリー（うち輸入）",
    "33400": "レタス",
    "33600": "パセリ",
    "34100": "きゅうり",
    "34200": "かぼちゃ",
    "34201": "かぼちゃ（うち輸入）",
    "34300": "なす",
    "34400": "トマト",
    "34450": "ミニトマト",
    "34500": "ピーマン",
    "34600": "ししとうがらし",
    "34700": "スイートコーン",
    "35100": "さやいんげん",
    "35200": "さやえんどう",
    "35201": "さやえんどう（うち輸入）",
    "35300": "実えんどう",
    "35400": "そらまめ",
    "35500": "えだまめ",
    "36100": "かんしょ",
    "36200": "ばれいしょ",
    "36300": "さといも",
    "36500": "やまのいも",
    "36610": "たまねぎ",
    "36620": "たまねぎ（うち輸入）",
    "36700": "にんにく",
    "36701": "にんにく（うち輸入）",
    "37200": "しょうが",
    "37201": "しょうが（うち輸入）",
    "38100": "生しいたけ",
    "38101": "生しいたけ（うち輸入）",
    "38300": "なめこ",
    "38400": "えのきだけ",
    "38500": "しめじ",
    "39000": "その他の野菜",
    "39100": "輸入野菜計",
    "39200": "その他の輸入野菜",
    "40000": "果実計",
    "40001": "国産果実計",
    "40100": "みかん",
    "41201": "ネーブルオレンジ",
    "41253": "甘なつみかん",
    "41301": "いよかん",
    "41321": "はっさく",
    "41999": "その他の雑かん",
    "42000": "りんご計",
    "42204": "つがる",
    "42505": "ジョナゴールド",
    "42515": "王林",
    "42804": "ふじ",
    "42999": "その他のりんご",
    "43000": "日本なし計",
    "43203": "幸水",
    "43205": "豊水",
    "43302": "二十世紀",
    "43310": "新高",
    "43499": "その他のなし",
    "43401": "西洋なし",
    "43500": "かき計",
    "43700": "甘がき",
    "43751": "渋がき",
    "43900": "びわ",
    "44100": "もも",
    "44700": "すもも",
    "44800": "おうとう",
    "44950": "うめ",
    "45000": "ぶどう計",
    "45202": "デラウェア",
    "45206": "巨峰",
    "45299": "その他のぶどう",
    "45700": "くり",
    "46100": "いちご",
    "47000": "メロン計",
    "47200": "温室メロン",
    "47213": "アンデスメロン",
    "47299": "その他のメロン",
    "48100": "すいか",
    "49300": "キウイフルーツ",
    "49500": "その他の国産果実",
    "50000": "輸入果実計",
    "50100": "バナナ",
    "50300": "パインアップル",
    "50400": "レモン",
    "50500": "グレープフルーツ",
    "50600": "オレンジ",
    "50700": "輸入おうとう",
    "50800": "輸入キウイフルーツ",
    "50850": "輸入メロン",
    "50900": "その他の輸入果実",
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
    if item_code.startswith("4") or item_code.startswith("5"):
        return "果実"
    return "不明"


def item_name(item_code):
    return ITEM_NAMES.get(item_code, "不明")


def rows_from_report(records):
    if not records:
        return []

    column_num = len(records[0])
    date = f"{int(records[0][0]):04d}/{int(records[0][1]):02d}/{int(records[0][2]):02d}"

    if column_num == 12:
        city_name = "主要卸売市場計"
        city_code = "0000"
        offset = 2
    elif column_num == 14:
        city_name = normalize_text(records[0][4])
        city_code = normalize_code(records[0][5], 4)
        offset = 0
    else:
        raise RuntimeError(f"想定外のCSV列数です: {column_num}")

    rows = []

    for record in records:
        item_code_value = normalize_code(record[7 - offset], 5)
        area = normalize_text(record[8 - offset]) or "総量"
        row = {
            "date": date,
            "city_name": city_name,
            "city_code": city_code,
            "item": item_name(item_code_value),
            "item_code": item_code_value,
            "area": area,
            "area_code": normalize_code(record[9 - offset], 3),
            "trading_volume": normalize_text(record[10 - offset]),
            "average_price": normalize_text(record[11 - offset]),
            "volume_versus_previous_day": normalize_text(record[12 - offset]),
            "price_versus_previous_day": normalize_text(record[13 - offset]),
            "category": category_from_item_code(item_code_value),
        }
        rows.append(row)

    return rows


def fetch_wmr():
    date = fetch_latest_date()
    report_numbers = fetch_report_numbers(date)
    rows = []

    for report_no in report_numbers:
        records = read_report_csv(report_no)
        rows.extend(rows_from_report(records))

    if not rows:
        raise RuntimeError("データを取得できませんでした。")

    return pd.DataFrame(rows, columns=COLUMNS)


def filter_data(df, city=None, cat=None, item=None):
    result = df.copy()

    if city:
        result = result[result["city_code"] == str(city).zfill(4)]

    if item:
        result = result[result["item_code"] == str(item).zfill(5)]
    elif cat:
        category = {"v": "野菜", "f": "果実"}.get(cat, cat)
        result = result[result["category"] == category]

    return result.reset_index(drop=True)


def to_api_style_json(df):
    if df.empty:
        return {"Error": "都市のデータが見つかりませんでした。"}

    first = df.iloc[0]
    output = {
        "Date": first["date"],
        "CityName": first["city_name"],
        "CityCode": first["city_code"],
    }

    for _, row in df.iterrows():
        item = row["item"]
        area = row["area"]

        output.setdefault(item, {"ItemCode": row["item_code"]})
        output[item][area] = {
            "ProductionAreaCode": row["area_code"],
            "TradingVolume": row["trading_volume"],
            "AveragePrice": row["average_price"],
            "VolumeVersusPreviousDay": row["volume_versus_previous_day"],
            "PriceVersusPreviousDay": row["price_versus_previous_day"],
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
            "date": "t_wmr_date",
            "city_name": "t_wmr_city_name",
            "city_code": "t_wmr_city_code",
            "item": "t_wmr_item",
            "item_code": "t_wmr_item_code",
            "area": "t_wmr_area",
            "area_code": "t_wmr_area_code",
            "trading_volume": "t_wmr_trading_volume",
            "average_price": "t_wmr_average_price",
            "volume_versus_previous_day": "t_wmr_volume_versus_previous_day",
            "price_versus_previous_day": "t_wmr_price_versus_previous_day",
            "category": "t_wmr_category",
        }
    )

    with sqlite3.connect(sqlite_path) as conn:
        db_df.to_sql("t_wmr", conn, if_exists="replace", index=False)


def parse_args():
    parser = argparse.ArgumentParser(description="農林水産省の青果物卸売市場調査（日別調査）を取得します。")
    parser.add_argument("--city", help="都市コードで絞り込みます。例: 1301")
    parser.add_argument("--cat", choices=["v", "f"], help="種別で絞り込みます。v=野菜、f=果実")
    parser.add_argument("--item", help="品目コードで絞り込みます。例: 30100")
    parser.add_argument("--format", choices=["csv", "json"], default="csv", help="出力形式")
    parser.add_argument("--output", default=None, help="出力ファイル名")
    parser.add_argument("--sqlite", default=None, help="SQLite にも保存する場合のDBファイル名")
    return parser.parse_args()


def main():
    args = parse_args()
    df = fetch_wmr()
    df = filter_data(df, city=args.city, cat=args.cat, item=args.item)

    output_path = args.output or f"wmr_latest.{args.format}"
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
日付,都市名,都市コード,品目名,品目コード,産地名,産地コード,数量(Kg),価格(円/Kg),対前日比数量(%),対前日比価格(%),種別
```

JSON は現在の Web API に近い形で、日付・都市情報のあとに、品目名、産地名の順で階層化します。

```json
{
  "Date": "2026/06/24",
  "CityName": "東京都",
  "CityCode": "1301",
  "だいこん": {
    "ItemCode": "30100",
    "北海道": {
      "ProductionAreaCode": "001",
      "TradingVolume": "12345",
      "AveragePrice": "120",
      "VolumeVersusPreviousDay": "105",
      "PriceVersusPreviousDay": "98"
    }
  }
}
```

上の値は形式説明用の例です。実際の値は取得時点の農林水産省公開データに従います。

## 主なパラメータ

| パラメータ | 内容 | 例 |
| --- | --- | --- |
| `--city` | 都市コード | `1301` |
| `--cat` | 種別。`v` は野菜、`f` は果実 | `v` |
| `--item` | 品目コード | `30100` |
| `--format` | 出力形式 | `csv` / `json` |
| `--sqlite` | SQLite保存先 | `wmr.db` |

## 注意点

- 農林水産省側のページ構成、フォーム名、CSV列構成が変更された場合、このコードの修正が必要になることがあります。
- 取得元サイトに負荷をかけないよう、短時間に何度も実行する使い方は避けてください。
- cultivationdata.net の API 説明では、青果物卸売市場調査（日別調査）は17時頃に更新されると案内しています。
- エラー回避のため、数値に見える値も文字列として扱っています。
- SQLite 保存は、既存 API 側のテーブル名 `t_wmr` と列名に寄せています。
- 元CSVの形式によっては、主要卸売市場計と各都市で列位置が異なります。このコードでは既存実装と同じように列数で判定しています。
