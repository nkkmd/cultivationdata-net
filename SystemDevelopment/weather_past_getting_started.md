# 過去の気象データ（日ごとの値）取得コード

最終更新日: 2026-06-24

このドキュメントは、cultivationdata.net の Web API を使わず、利用者自身の環境で気象庁の「過去の気象データ（日ごとの値）」を取得するための説明と Python コードをまとめたものです。

元データ:

https://www.data.jma.go.jp/obd/stats/etrn/index.php

## このコードでできること

- 気象庁の過去の気象データ（日ごとの値）ページから日別値を取得します。
- 5桁の国際地点番号、または2桁の都府県・地方番号と4桁の地点番号を指定できます。
- 年月を指定しない場合は前日のデータだけを取得します。
- 年月を指定した場合は、その月の日別データをまとめて取得します。
- JSON または CSV として保存します。

## API 版との関係

現在の Web API では、`weather_past.py` の `getPastData(prec, no, year, month)` がこの取得処理を担当しています。このドキュメントのコードは、APIサーバーを立てず、利用者が手元で直接データを取得・保存できるようにした単体スクリプトです。

## 動作環境

Python 3.10 以上を想定しています。

必要なライブラリをインストールします。

```bash
python -m pip install requests beautifulsoup4 pandas
```

## 使い方

国際地点番号を使って、小名浜の前日データを JSON に保存します。

```bash
python get_weather_past.py --no 47598 --format json --output past_47598.json
```

その他の地点として、福島県の山田の前日データを JSON に保存します。

```bash
python get_weather_past.py --prec 36 --no 1607 --format json --output past_1607.json
```

国際地点番号を使って、2024年2月の月別データを CSV に保存します。

```bash
python get_weather_past.py --no 47598 --year 2024 --month 2 --format csv --output past_47598_202402.csv
```

その他の地点として、2024年2月の月別データを CSV に保存します。

```bash
python get_weather_past.py --prec 36 --no 1607 --year 2024 --month 2 --format csv --output past_1607_202402.csv
```

## Python コード

```python
#!/usr/bin/env python3

import argparse
import calendar
import json
import re
import sys
import time
from datetime import datetime, timedelta
from pathlib import Path

import pandas as pd
import requests
from bs4 import BeautifulSoup


INTERNATIONAL_PREC_NO = {
    "47401": "11",
    "47402": "11",
    "47404": "13",
    "47405": "17",
    "47406": "13",
    "47407": "12",
    "47409": "17",
    "47411": "16",
    "47412": "14",
    "47413": "15",
    "47417": "20",
    "47418": "19",
    "47420": "18",
    "47421": "16",
    "47423": "21",
    "47424": "21",
    "47426": "22",
    "47428": "24",
    "47430": "23",
    "47433": "16",
    "47435": "17",
    "47440": "20",
    "47512": "33",
    "47520": "35",
    "47570": "36",
    "47574": "31",
    "47575": "31",
    "47576": "31",
    "47581": "31",
    "47582": "32",
    "47584": "33",
    "47585": "33",
    "47587": "35",
    "47588": "35",
    "47590": "34",
    "47592": "34",
    "47595": "36",
    "47597": "36",
    "47598": "36",
    "47600": "56",
    "47602": "54",
    "47604": "54",
    "47605": "56",
    "47606": "55",
    "47607": "55",
    "47610": "48",
    "47612": "54",
    "47615": "41",
    "47616": "57",
    "47617": "52",
    "47618": "48",
    "47620": "48",
    "47622": "48",
    "47624": "42",
    "47626": "43",
    "47629": "40",
    "47631": "57",
    "47632": "52",
    "47636": "51",
    "47637": "48",
    "47638": "49",
    "47639": "49",
    "47640": "49",
    "47641": "43",
    "47646": "40",
    "47648": "45",
    "47649": "53",
    "47651": "53",
    "47653": "51",
    "47654": "50",
    "47655": "50",
    "47656": "50",
    "47657": "50",
    "47662": "44",
    "47663": "53",
    "47666": "50",
    "47668": "50",
    "47670": "46",
    "47672": "45",
    "47674": "45",
    "47675": "44",
    "47677": "44",
    "47678": "44",
    "47682": "45",
    "47684": "53",
    "47690": "41",
    "47740": "68",
    "47741": "68",
    "47742": "69",
    "47744": "69",
    "47746": "69",
    "47747": "63",
    "47750": "61",
    "47751": "60",
    "47754": "81",
    "47755": "68",
    "47756": "66",
    "47759": "61",
    "47761": "60",
    "47762": "81",
    "47765": "67",
    "47766": "67",
    "47767": "67",
    "47768": "66",
    "47769": "63",
    "47770": "63",
    "47772": "62",
    "47776": "63",
    "47777": "65",
    "47778": "65",
    "47780": "64",
    "47784": "81",
    "47800": "84",
    "47805": "84",
    "47807": "82",
    "47809": "82",
    "47812": "84",
    "47813": "85",
    "47814": "83",
    "47815": "83",
    "47817": "84",
    "47818": "84",
    "47819": "86",
    "47821": "86",
    "47822": "87",
    "47823": "88",
    "47824": "86",
    "47827": "88",
    "47829": "87",
    "47830": "87",
    "47831": "88",
    "47835": "87",
    "47836": "88",
    "47837": "88",
    "47838": "86",
    "47843": "84",
    "47887": "73",
    "47890": "72",
    "47891": "72",
    "47892": "73",
    "47893": "74",
    "47894": "71",
    "47895": "71",
    "47897": "74",
    "47898": "74",
    "47899": "74",
    "47909": "88",
    "47912": "91",
    "47918": "91",
    "47927": "91",
    "47929": "91",
    "47936": "91",
    "47940": "91",
    "47942": "88",
    "47945": "91",
    "47971": "44",
    "47991": "44",
}

INTERNATIONAL_ITEMS = [
    "現地気圧（平均）",
    "海面気圧（平均）",
    "合計降水量",
    "最大1時間降水量",
    "最大10分間降水量",
    "平均気温",
    "最高気温",
    "最低気温",
    "平均湿度",
    "最小湿度",
    "平均風速",
    "最大風速",
    "最大風速（風向）",
    "最大瞬間風速",
    "最大瞬間風速（風向）",
    "日照時間",
    "合計降雪",
    "最深積雪",
    "天気概況（昼）",
    "天気概況（夜）",
]

LOCAL_ITEMS = [
    "合計降水量",
    "最大1時間降水量",
    "最大10分間降水量",
    "平均気温",
    "最高気温",
    "最低気温",
    "平均湿度",
    "最小湿度",
    "平均風速",
    "最大風速",
    "最大風速（風向）",
    "最大瞬間風速",
    "最大瞬間風速（風向）",
    "最多風向",
    "日照時間",
    "降雪の深さの合計",
    "最深積雪",
]


def target_date_range(year, month):
    yesterday = datetime.now() - timedelta(days=1)

    if year is None and month is None:
        return yesterday.year, yesterday.month, [yesterday.day]

    if year is None or month is None:
        raise ValueError("year と month は両方指定してください。")

    year = int(year)
    month = int(month)

    if year == yesterday.year and month == yesterday.month:
        last_day = yesterday.day
    else:
        last_day = calendar.monthrange(year, month)[1]

    return year, month, list(range(1, last_day + 1))


def build_url(prec, no, year, month):
    if len(no) == 5:
        prec = prec or INTERNATIONAL_PREC_NO.get(no)
        if not prec:
            raise ValueError("この国際地点番号の都府県・地方番号が不明です。--prec を指定してください。")
        page = "daily_s1.php"
    elif len(no) == 4:
        if not prec:
            raise ValueError("4桁の地点番号では --prec が必要です。")
        page = "daily_a1.php"
    else:
        raise ValueError("--no は5桁の国際地点番号、または4桁の地点番号を指定してください。")

    return (
        f"https://www.data.jma.go.jp/obd/stats/etrn/view/{page}"
        f"?prec_no={prec}&block_no={no}&year={year}&month={month}"
    )


def fetch_soup(url):
    response = requests.get(url, timeout=30)
    response.raise_for_status()
    return BeautifulSoup(response.content, "html.parser")


def block_name_from_soup(soup, year):
    heading = soup.find("h3")
    if heading is None:
        return "不明"

    text = heading.get_text(strip=True).replace("\u3000", "")
    match = re.findall(r"^(.*?)" + str(year), text)
    return match[0] if match else text


def cell_text(cell):
    if cell is None:
        return ""
    return cell.get_text(strip=True)


def get_cells(soup):
    return soup.select("td.data_0_0")


def extract_day(cells, day, items):
    values_per_day = len(items)
    start = values_per_day * (day - 1)
    result = {}

    for index, item in enumerate(items):
        result[item] = cell_text(cells[start + index]) if start + index < len(cells) else ""

    return result


def get_past_data(prec, no, year=None, month=None):
    time.sleep(1)
    year, month, days = target_date_range(year, month)
    url = build_url(prec, no, year, month)
    soup = fetch_soup(url)
    block_name = block_name_from_soup(soup, year)
    cells = get_cells(soup)
    items = INTERNATIONAL_ITEMS if len(no) == 5 else LOCAL_ITEMS

    result = {block_name: {}}

    for day in days:
        date_key = f"{year}-{month}-{day}"
        result[block_name][date_key] = extract_day(cells, day, items)

    return result


def rows_for_csv(data):
    rows = []

    for block_name, dates in data.items():
        for date, values in dates.items():
            row = {"地点名": block_name, "日付": date}
            row.update(values)
            rows.append(row)

    return rows


def save_json(data, output_path):
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def save_csv(data, output_path):
    pd.DataFrame(rows_for_csv(data)).to_csv(output_path, index=False, encoding="utf-8-sig")


def parse_args():
    parser = argparse.ArgumentParser(description="気象庁の過去の気象データ（日ごとの値）を取得します。")
    parser.add_argument("--prec", help="都府県・地方番号。4桁地点番号では必須です。例: 36")
    parser.add_argument("--no", required=True, help="5桁の国際地点番号、または4桁の地点番号。例: 47598 / 1607")
    parser.add_argument("--year", help="取得年。例: 2024")
    parser.add_argument("--month", help="取得月。例: 2")
    parser.add_argument("--format", choices=["json", "csv"], default="json", help="出力形式")
    parser.add_argument("--output", default=None, help="出力ファイル名")
    return parser.parse_args()


def main():
    args = parse_args()
    data = get_past_data(args.prec, args.no, year=args.year, month=args.month)
    output_path = Path(args.output or f"weather_past_{args.no}.{args.format}")

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

JSON は現在の Web API と同じように、地点名、日付、観測項目の順で階層化します。

```json
{
  "小名浜": {
    "2026-6-23": {
      "現地気圧（平均）": "1012.3",
      "海面気圧（平均）": "1014.8",
      "合計降水量": "0.0",
      "平均気温": "21.5",
      "最高気温": "25.1",
      "最低気温": "18.4"
    }
  }
}
```

上の値は形式説明用の例です。実際の値は取得時点の気象庁公開データに従います。

## 主なパラメータ

| パラメータ | 内容 | 例 |
| --- | --- | --- |
| `--prec` | 都府県・地方番号。4桁地点では必須 | `36` |
| `--no` | 5桁の国際地点番号、または4桁の地点番号 | `47598` / `1607` |
| `--year` | 月別取得する年 | `2024` |
| `--month` | 月別取得する月 | `2` |
| `--format` | 出力形式 | `json` / `csv` |

## 注意点

- 気象庁側のHTML構造や表の列構成が変更された場合、このコードの修正が必要になることがあります。
- 取得元サイトに負荷をかけないよう、短時間に何度も実行する使い方は避けてください。
- cultivationdata.net の API 説明では、過去の気象データ（日ごとの値）は毎日1時頃までに更新されると案内しています。
- 5桁の国際地点番号は、コード内の `INTERNATIONAL_PREC_NO` で都府県・地方番号を補完しています。辞書にない地点では `--prec` も指定してください。
- 4桁の地点番号では、気象庁の過去の気象データページで確認できる `prec_no` と `block_no` を指定してください。
- このコードは気象庁の公開HTMLを整形するものです。データの内容や利用条件は気象庁の公開情報を確認してください。
