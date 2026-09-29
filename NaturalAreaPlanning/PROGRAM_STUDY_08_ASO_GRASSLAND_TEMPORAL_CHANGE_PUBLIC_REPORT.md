# Natural Area Planning / NAP-AGTC-2026-08-25-v1 — 公開研究報告

**阿蘇草原の時系列変化・木本侵入様構造転換研究1**  
**— 公開された衛星観測資料で、計画単位ごとの草原の持続性、経時変化、木本侵入に似た構造変化を調べる —**

- レポート版: **v1.0.1**
- 編集改訂: **2026-09-28 — 日本語表現の整備。科学的結果・判定は変更なし**
- 作成日: **2026-09-16 JST**
- 研究番号: **08**
- 研究ID: **NAP-AGTC-2026-08-25-v1**
- 研究状態: **COMPLETE / FROZEN / INTEGRATED TO MAIN**
- 正式判定: **PARTIALLY_SUPPORTED**
- 科学的結果を確定したコミット: **nkkmd/natural-area-planning @ 051c9c27bb3dec2a8f1409d25549b1441dfad097**
- 本文の性格: **単体公開用研究レポート**

この文書は、元のGitHubリポジトリや内部資料を参照しなくても、研究の背景、問い、方法、主要結果、限界、再現性、今後の研究境界を理解できるように構成している。

## 要旨

阿蘇の193の計画単位について、1985–2025年のLandsat、2017–2025年のSentinel-2、JAXA高解像度土地利用土地被覆図日本域版v25.04の2020・2022・2024年、および既存の公開植生図集計を用い、長期的な光学的変化方向と近年の地図上の草地・木本の分類の推移を評価した。解析対象、季節、品質管理、指数、閾値、欠測・不一致の扱いは結果確認前に凍結した。

Landsatでは174/193単位が長期方向判定の条件を満たし、156単位が`OPTICAL_ALL_INCREASING`、2単位が`OPTICAL_ALL_DECREASING`、16単位が`OPTICAL_MIXED`、19単位が`OPTICAL_INSUFFICIENT`だった。Sentinel-2では41単位が`OPTICAL_ALL_INCREASING`、9単位が`OPTICAL_ALL_DECREASING`、143単位が`OPTICAL_MIXED`だった。両センサーの近年方向比較は`CONCORDANT` 16、`DISCORDANT` 7、`PARTIAL` 151、`NOT_COMPARABLE` 19だった。

JAXA HRLULCの事前に確定した規則では、`PERSISTENT_GRASSLAND_COMPATIBLE` 95、`DECLINING_GRASSLAND_COMPATIBILITY` 3、`TRANSITIONING` 95であり、`WOODY_ENCROACHMENT_LIKE_STRUCTURAL_CHANGE`の全条件を満たした単位は0だった。これは木本侵入が存在しないことの証明ではない。PALSAR-2 FNF Ver.2.1.0の指定された16ファイルはログイン後の画面でも取得できず、R1を`ACCESS_LIMITED`として保持した。歴史植生図は比較対象と共通する調査時点や、事前に確定した分類の対応規則がないため、全193単位を`NOT_COMPARABLE`とした。

L1・S2・C1の主要評価項目は推定できた一方、独立した合成開口レーダー（SAR）による構造の検証を実施できず、歴史植生図との同一カテゴリ比較も成立しなかったため、研究全体の正式判定は`PARTIALLY_SUPPORTED`である。衛星観測上の変化から、管理行為、因果的管理効果、生物多様性変化、現地確認済み木本侵入、または管理推奨を導いていない。

# 1. 研究の背景

これまでのNatural Area Planning研究では、対象区域の区分、既存植生図との重ね合わせ、計画単位ごとの公開情報の整理まで進めた。一方、それらは阿蘇草原の長期的な衛星の光学指標の変化や、近年の草地・木本の分類の推移を同じ事前に確定した研究計画で評価していなかった。

研究08は、この未解決部分を一般公開された衛星観測資料だけで検討する独立研究として開始した。先行研究で確定した判定、しきい値、評価項目、`historical transfer_to_zone_contribution = false`は変更対象にしなかった。

# 2. 研究対象

研究対象は、凍結済みGeoJSONに含まれる阿蘇の193の計画単位である。計画単位を識別する地理情報はSHA-256 `46ef4dd475ec7645d78130722e8ddfcae9f51c6244ce95dc22ea9f7dcaa6609d`で固定した。

本研究の対象は衛星観測と公開地図上の時系列的な状態・方向である。現地植生、個別の管理行為、土地所有者・管理者の意図、管理の効果、生物多様性応答は直接測定していない。

# 3. 研究目的と中心的研究質問

中心的研究質問は次のとおりである。

> 公開オンラインで再現可能な衛星・土地被覆資料を用いた場合、阿蘇の193の計画単位について、長期的な光学指標の変化、近年の草地への適合性、地図上で木本の分類へ持続的に変化したかどうか、センサー間不一致、歴史植生図との比較可能性を、事前に確定した規則の範囲でどこまで推定できるか。

研究全体の正式判定は`SUPPORTED_WITHIN_FROZEN_SCOPE`、`PARTIALLY_SUPPORTED`、`NOT_SUPPORTED`、`INDETERMINATE`、`NON_ESTIMABLE`、`ACCESS_LIMITED`、`STRUCTURALLY_UNAVAILABLE`、`INSUFFICIENT_TEMPORAL_COVERAGE`のいずれかとした。

# 4. 先行研究と本研究の新規性の範囲

NDVI、NDMI、NBR、Theil–Sen傾き、Landsat、Sentinel-2、PALSAR-2 FNF、土地被覆分類は既存の一般的方法・公開データであり、本研究はそれ自体の発明を主張しない。本研究の対象固有の貢献は、事前に確定した193の計画単位と判定規則の下で、複数情報源の取得、欠測、不一致、比較不能を救済せずに統合した点にある。

# 5. 使用した情報と使用しなかった情報

使用した情報はすべて`PUBLIC-ONLINE ONLY`である。

| 区分 | 情報源 | 期間・版 | 役割 |
|---|---|---|---|
| L1 | USGS Landsat Collection 2 Level-2 SR（Earth Engine経由） | 1985–2025 | 長期の光学観測資料（主な資料） |
| S2 | Copernicus Sentinel-2 L2A harmonized（Earth Engine経由） | 2017–2025 | 近年の光学観測資料（補助資料） |
| C1 | JAXA HRLULC Japan v25.04 | 2020・2022・2024 | 草地・木本の分類の推移を示す地図上の代替指標 |
| R1 | JAXA PALSAR-2 FNF Ver.2.1.0 | 2017–2020 | SARによる構造変化の検証。資料を取得できなかったため`ACCESS_LIMITED` |
| H1 | 既存公開植生図の計画単位集計 | 元データの作成年 2001・2007・2022 | 比較のためだけに用いる資料 |

行政照会、現地確認、直接観測、非公開の地域資料、人を対象とする研究は使用していない。JAXAおよびGoogle Earth Engineの登録は公開・無料のデータセットへのアクセス手段として扱い、認証情報は記録・コミットしていない。

# 6. 結果を見る前の研究計画と確定手順

正式な研究ID、193単位の識別情報、資料ごとの役割、対象期間、品質管理、光学指数、Theil–Sen法による変化方向の判定規則、C1の分類と面積・割合・連結したまとまりのしきい値、欠測・不一致の扱い、判定値の定義を結果確認前に確定した。実行前の検証はP1–P12すべてPASSだった。

Landsatの全期間分の年次データを書き出す処理がEarth Engineで時間切れとなったため、1985–1991、1992–1998、1999–2005、2006–2012、2013–2019、2020–2025の6つの期間に分割した。使用データ、対象季節、除外条件、指標、地理情報、集計方法は変更していない。6区間は41年を欠落・重複なく再結合した。

# 7. 方法

## 7.1 Landsat

1985–2025年の7月1日–9月30日を対象に、Collection 2 Level-2の地表面反射率からNDVI、NDMI、NBRの画素ごとの年次中央値を作成した。欠損、雲、雲の影、雪、巻雲、放射量の飽和を除外し、画素・年の組み合わせは2観測以上を要求した。計画単位集計は境界から内側に30 mの余裕を設ける処理と処理後も元の面積の50%以上を保持する規則を用いた。

各指標について、20年以上の有効な年次値があり、3つの時代区分のすべてに観測値があることを要求し、Theil–Sen傾きと最初と最後にあたる有効な各5年の中央値の符号で方向を分類した。

## 7.2 Sentinel-2

2017–2025年の同一季節を対象に、`COPERNICUS/S2_SR_HARMONIZED`と`COPERNICUS/S2_CLOUD_PROBABILITY`を使用した。雲である確率が40%未満の観測値を用いた。計画単位の境界から10 m内側に絞り、元の面積の50%以上が残ることを求めた。有効な年次値が6年以上あり、観測期間が6暦年以上にわたることを方向判定条件とした。

LandsatとSentinel-2の値は結合・平均せず、近年方向の一致、不一致、部分一致、比較不能を報告した。

## 7.3 JAXA HRLULC

v25.04の2020・2022・2024年を同じ10 m格子で解析した。草地の分類値は5、木本に関する分類値は6・7・8・9・11とした。2020年に草地と分類され、2022年と2024年の両方で木本と分類された画素について、1.0 ha以上、2020年草地面積の5%以上、8近傍で連結した最大のまとまり 0.5 ha以上をすべて要求した。

## 7.4 R1とH1

FNFは指定された4枚のタイルについて4年分をログイン後の画面で探したが、必要なダウンロードリンクが提供されなかったため`ACCESS_LIMITED`とした。別の版・対象年・分類器は用いていない。

H1には作成年が2001・2007・2022年と異なる資料が混在し、C1との共通の時点や、事前に確定した分類の対応規則がない。このため、結果を見てから新しい分類対応規則を作ることはせず、全単位を`NOT_COMPARABLE`とした。

# 8. 主要結果

## 8.1 評価項目A — 対象期間を評価できる範囲

- Landsatで判定可能: **174/193（90.2%）**
- Landsatで残存面積または時系列の条件を満たさない: **19/193（9.8%）**
- Sentinel-2で判定可能: **193/193（100%）**
- C1で3時点の資料が揃った: **193/193（100%）**
- R1で判定可能: **0/193、ACCESS_LIMITED**

## 8.2 評価項目B — 光学指標の経時変化

| 状態 | Landsat | Sentinel-2 |
|---|---:|---:|
| `OPTICAL_ALL_INCREASING` | 156 | 41 |
| `OPTICAL_ALL_DECREASING` | 2 | 9 |
| `OPTICAL_MIXED` | 16 | 143 |
| `OPTICAL_INSUFFICIENT` | 19 | 0 |

これらは光学指標の変化方向であり、草地状態、木本侵入、管理効果、生物多様性変化を直接表さない。

## 8.3 評価項目C — 草地・木本の地図上の分類の推移

| 状態 | 計画単位 |
|---|---:|
| `PERSISTENT_GRASSLAND_COMPATIBLE` | 95 |
| `DECLINING_GRASSLAND_COMPATIBILITY` | 3 |
| `TRANSITIONING` | 95 |
| `WOODY_ENCROACHMENT_LIKE_STRUCTURAL_CHANGE` | 0 |

強い木本侵入様分類が0であったことは、C1について事前に確定した地図上の分類規則を満たす単位がなかったという結果である。現地の木本侵入がないことを示さない。

## 8.4 評価項目D — 不確実性と検証

| LandsatとSentinel-2の近年の変化方向 | 計画単位 |
|---|---:|
| `CONCORDANT` | 16 |
| `DISCORDANT` | 7 |
| `PARTIAL` | 151 |
| `NOT_COMPARABLE` | 19 |

R1は`ACCESS_LIMITED`、SARとの検証は`NOT_COMPARABLE`である。センサー不一致は平均化して消していない。

## 8.5 評価項目E — 過去の植生図との比較

`NOT_COMPARABLE`は193/193だった。これは歴史植生図が誤りという意味ではなく、作成年や分類の定義が異なる資料を同じカテゴリとして比較するための、事前に確定した規則がなかったためである。

# 9. 正式判定

```text
Study 08 outcome = PARTIALLY_SUPPORTED
```

L1、S2、C1から、長期・近年の光学指標の変化方向と2020–2024年のC1の地図上の分類の推移は推定できた。一方、独立した合成開口レーダー（SAR）による構造検証（R1）が取得不能であり、H1比較も`NOT_COMPARABLE`だった。したがって、凍結済み範囲の一部は実行・検証できたが、研究計画で必要とした構造変化の診断や検証の一部が欠ける場合に対応する`PARTIALLY_SUPPORTED`を適用した。

# 10. 本研究が支持すること

- 事前に確定した193の計画単位でLandsatの光学指標の長期的な変化方向を174単位で推定できる。
- Sentinel-2の近年方向を193単位について推定できる。
- 両光学センサーの方向は一様に一致せず、不一致または部分一致の状態を明示する必要がある。
- C1 v25.04の3時点地図上の分類の推移では、持続的な草地に適合する分類が95単位、草地への適合性が低下した分類が3単位、変化の途中と判定された分類が95単位となる。
- 凍結済み強判定条件を満たす木本侵入に似た変化は0だった。
- R1欠測とH1比較不能を残したまま、研究を否定的な結果や一部支持の結果を含む正式な完了として閉じられる。

# 11. 本研究が支持しないこと

- 衛星観測で見えた変化から特定の管理行為を同定すること
- 植生の変化の推移から因果的管理効果を推定すること
- 光学指標の変化から火入れ、採草、放牧を識別すること
- C1の地図上の分類の推移を現地確認済み木本侵入とみなすこと
- 光学指標の増加・減少を生物多様性の改善/悪化とみなすこと
- 後年衛星結果だけで歴史植生図を誤りと判定すること
- 計画単位ごとの管理推奨を行うこと
- 人による検証が実施されたとみなすこと
- NAP-003を承認すること

# 12. 実務的含意

本結果は、193単位のどこで長期光学情報が十分か、C1上で近年の草地の状態が地図上でどの分類に当てはまるか、センサー間でどの程度一致しないかを監査可能な形で示す。計画の検討や追加調査の情報整理には使えるが、個別管理行為の選択や優先順位を直接決める根拠ではない。

# 13. 限界

1. R1 FNFが取得できず、独立したLバンド合成開口レーダーによる構造変化の検証を実行できなかった。
2. C1は複数センサーを使う外部で作成された地図であり、L1/S2から完全に独立した現地調査で確認された事実ではない。
3. 2022 C1の後処理は2020年と2024年の分類の一致に依存し得る。
4. Landsatは境界から内側に30 mの余裕を設ける処理により19単位が不足状態になった。
5. LandsatとSentinel-2はセンサー、解像度、期間が異なり、値の直接結合を行っていない。
6. H1は作成年が異なる資料の混在で、C1との凍結済みカテゴリ間の対応規則がない。
7. 傾斜のGeoTIFFは同じ名前の既存のGoogleドライブ上のファイルと今回の処理で作成したファイルを区別できなかったため、SHA値の一致と出所を特定できないという制約を取得記録に明記し、計画単位ごとの光学指標の変化方向を判定する正式な処理では使用しなかった。
8. 現地確認、管理履歴、利用に制限のある地域資料、人による検証は含まれない。
9. L1/S2それぞれの取得記録を確定する前に、ヘッダーの確認のためCSV先頭データ行が表示された。事前に確定したしきい値、情報源、規則、コードはその後変更していないが、取得手順の逸脱として取得・処理の記録と正式な結果へ記録した。このため、取得記録の形式で定めた`resultValuesInspectedBeforeManifestFreeze = false` 条件を満たしたとは主張しない。

# 14. 第三者資料・データの取扱い

大容量のEarth Engineからの書き出し結果とJAXAのラスターデータ一式はリポジトリへ再配布していない。リポジトリには取得仕様、ファイル名、ファイルサイズ、SHA-256、処理スクリプト、集計結果を保存した。パスワード、確認用URL、登録情報、電子メールの内容は保存していない。

# 15. 後続研究との境界

研究08の科学的結果はスナップショットとなるコミットで確定され、`main`へ統合された。研究09は`PLANNED / NOT STARTED`であり、別途、結果を見る前に定める開始条件を必要とする。研究09その他の後続研究は、研究08や先行研究の正式な結果を遡及的に書き換えてはならない。

`NAP-002 Study 2B = DEFERRED / NOT STARTED`、`human validation = NOT PERFORMED`、`Future NAP-003 = NOT AUTHORIZED`を維持する。

# 16. 再現性・検証

- 実行前の検証: **P1–P12 PASS**
- 分類結果の監査: **PASS**
- 想定外のケースを含む監査: **PASS**
- 統合した計画単位ごとの結果: **193 rows / 193 unique pu_id**
- 先行研究の結果を変更しない条件: **PASS**
- `historical transfer_to_zone_contribution`: **false**
- `main` への統合: **COMPLETE AFTER SCIENTIFIC SNAPSHOT**

大容量元のデータはGit外の長期保存用のローカル領域に保存し、L1/S2/C1の取得記録にハッシュ値を記録した。Landsat分割年次CSVは1985–2025の41年を正確に再構成した。

# 17. 再現性識別子

```text
Study ID: NAP-AGTC-2026-08-25-v1
Scientific snapshot: 051c9c27bb3dec2a8f1409d25549b1441dfad097
Geometry SHA-256: 46ef4dd475ec7645d78130722e8ddfcae9f51c6244ce95dc22ea9f7dcaa6609d
Integrated result SHA-256: 98ec61082c6f8321511a937bac774f7ccd2b3504f8e87aba6de5c3abbde80291
Endpoint summary SHA-256: 1da189a7626986e730f339405d19af2bfb7d7f9b1bbeed96f2f0603e16ca29e3
Formal result SHA-256: e8a866171f5018d6e3f2b98e6455d6a8e851ac21ad31eee1d24f044da47e20fc
Adversarial audit SHA-256: 763cb0bdfc05923e4c54dab9643efc145635f465f94b8c49214065edc3adf89c
Planning units: 193
Formal outcome: PARTIALLY_SUPPORTED
```

# 18. リポジトリ内の主要資料

研究計画と確定記録:

```text
doc/aso-grassland-temporal-change/ASO_GRASSLAND_TEMPORAL_CHANGE_PROSPECTIVE_PROTOCOL.md
doc/aso-grassland-temporal-change/PREEXEC_AMENDMENT_01.md
analysis/aso-grassland-temporal-change/prereg/STAGE_1_FORMAL_SPEC.json
```

取得記録:

```text
analysis/aso-grassland-temporal-change/acquisition/L1_acquisition_manifest.json
analysis/aso-grassland-temporal-change/acquisition/S2_acquisition_manifest.json
analysis/aso-grassland-temporal-change/acquisition/C1_acquisition_manifest.json
analysis/aso-grassland-temporal-change/acquisition/R1_access_state.json
```

結果と監査:

```text
analysis/aso-grassland-temporal-change/results/study08_integrated_planning_unit_results.csv
analysis/aso-grassland-temporal-change/results/study08_endpoint_summary.json
analysis/aso-grassland-temporal-change/results/study08_formal_result.json
analysis/aso-grassland-temporal-change/results/study08_classification_audit.json
analysis/aso-grassland-temporal-change/results/study08_adversarial_audit.json
analysis/aso-grassland-temporal-change/results/study08_scientific_state_snapshot.json
```

# 19. 結論

研究08は、一般公開されたオンライン情報だけを用い、阿蘇の193の計画単位について長期・近年の光学方向とC1の地図上の分類の推移を事前に確定した規則で推定した。Landsatでは、多くの単位で3つの指標がすべて増加方向だったが、Sentinel-2では混合型の判定が多数であり、センサー間一致は限定的だった。C1では草地の持続と整合する単位と変化中の単位が各95、草地への適合性が低下した単位が3で、厳しい条件を満たす木本侵入に似た変化は0だった。

R1が`ACCESS_LIMITED`、H1が全件`NOT_COMPARABLE`であることを保持したため、正式判定は`PARTIALLY_SUPPORTED`である。この判定は、欠測を埋めたり、閾値を緩めたり、管理・因果・現地植生の主張へ拡張した結果ではない。

# 用語

- **計画単位（planning unit）**: 本研究で範囲と識別情報を事前に確定した193の空間単位。
- **光学指標の変化方向（optical direction）**: NDVI・NDMI・NBRのTheil–Sen法による傾きと、期間の最初と最後の差を使って判定した方向。
- **草地と整合する地図上の状態（grassland-compatible）**: C1で明示的に草地とした分類に基づく、地図上の状態。
- **木本侵入に似た変化（woody-encroachment-like）**: 事前に定めた面積・割合・連結したまとまりの条件を満たす、地図上の分類の推移。現地確認済み木本侵入ではない。
- **ACCESS_LIMITED**: 必要な公開情報源の事前に定めた探索の深さを再現可能に実行できなかった状態。
- **NOT_COMPARABLE**: 定義、観測時点、資料が対象を十分に覆うかどうか、解像度等により、凍結済み範囲で比較できない状態。

# 使用した主な方法と先行資料

- USGS Landsat Collection 2: https://www.usgs.gov/landsat-missions/landsat-collection-2
- Copernicus Sentinel-2: https://dataspace.copernicus.eu/explore-data/data-collections/sentinel-data/sentinel-2
- JAXA High-Resolution Land-Use and Land-Cover Map of Japan v25.04: https://www.eorc.jaxa.jp/ALOS/jp/dataset/lulc/lulc_v2504_j.htm
- JAXA PALSAR-2/PALSAR Forest/Non-Forest Map: https://www.eorc.jaxa.jp/ALOS/en/dataset/fnf_e.htm

# 引用時の推奨表記

```text
Natural Area Planning / NAP-AGTC-2026-08-25-v1 (2026).
Public Research Report: 阿蘇草原の時系列変化・木本侵入様構造転換研究1.
Version 1.0.1, editorial revision 2026-09-28; scientific result 2026-09-16.
Formal outcome: PARTIALLY_SUPPORTED.
Study snapshot: nkkmd/natural-area-planning @ 051c9c27bb3dec2a8f1409d25549b1441dfad097.
```