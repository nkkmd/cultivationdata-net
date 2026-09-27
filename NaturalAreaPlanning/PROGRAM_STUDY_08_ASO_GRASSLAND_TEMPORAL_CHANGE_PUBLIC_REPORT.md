# Natural Area Planning / NAP-AGTC-2026-08-25-v1 — Public Research Report

**阿蘇草原の時系列変化・木本侵入様構造転換研究1**  
**— 公開オンラインremote-sensingによるplanning-unit-level grassland persistence, temporal change, and woody-encroachment-like structural transition —**

- レポート版: **v1.0**
- 作成日: **2026-09-16 JST**
- Program Study No.: **08**
- Study ID: **NAP-AGTC-2026-08-25-v1**
- 研究状態: **COMPLETE / FROZEN / INTEGRATED TO MAIN**
- Formal outcome: **PARTIALLY_SUPPORTED**
- 科学的結果snapshot: **nkkmd/natural-area-planning @ 051c9c27bb3dec2a8f1409d25549b1441dfad097**
- 本文の性格: **単体公開用研究レポート**

この文書は、元のGitHub repositoryや内部artifactを参照しなくても、研究の背景、問い、方法、主要結果、限界、再現性、今後の研究境界を理解できるように構成している。

## 要旨

阿蘇の193 planning unitsについて、1985–2025年のLandsat、2017–2025年のSentinel-2、JAXA高解像度土地利用土地被覆図日本域版v25.04の2020・2022・2024年、および既存の公開植生図集計を用い、長期的な光学的変化方向と近年の草地・木本クラスの地図上の推移を評価した。解析対象、季節、品質管理、指数、閾値、欠測・不一致の扱いは結果確認前に凍結した。

Landsatでは174/193単位が長期方向判定の条件を満たし、156単位が`OPTICAL_ALL_INCREASING`、2単位が`OPTICAL_ALL_DECREASING`、16単位が`OPTICAL_MIXED`、19単位が`OPTICAL_INSUFFICIENT`だった。Sentinel-2では41単位が`OPTICAL_ALL_INCREASING`、9単位が`OPTICAL_ALL_DECREASING`、143単位が`OPTICAL_MIXED`だった。両センサーの近年方向比較は`CONCORDANT` 16、`DISCORDANT` 7、`PARTIAL` 151、`NOT_COMPARABLE` 19だった。

JAXA HRLULCの凍結済み規則では、`PERSISTENT_GRASSLAND_COMPATIBLE` 95、`DECLINING_GRASSLAND_COMPATIBILITY` 3、`TRANSITIONING` 95であり、`WOODY_ENCROACHMENT_LIKE_STRUCTURAL_CHANGE`の全条件を満たした単位は0だった。これは木本侵入が存在しないことの証明ではない。PALSAR-2 FNF Ver.2.1.0の指定16ファイルは認証後UIでも取得できず、R1を`ACCESS_LIMITED`として保持した。歴史植生図は共通日付・凍結済みカテゴリcrosswalkがないため、全193単位を`NOT_COMPARABLE`とした。

L1・S2・C1の主要endpointは推定できた一方、独立SAR構造診断が利用できず、歴史植生図との同一カテゴリ比較も成立しなかったため、研究全体のformal outcomeは`PARTIALLY_SUPPORTED`である。remote-sensing上の変化から、管理行為、因果的管理効果、生物多様性変化、現地確認済み木本侵入、または管理推奨を導いていない。

# 1. 研究の背景

過去のNatural Area Planning研究は、対象区域の空間枠、既存植生図との重ね合わせ、planning-unit単位の公開情報整理を構築した。一方、それらは阿蘇草原の長期的なスペクトル変化や、近年の草地・木本クラスの推移を同一のprospective protocolで評価していなかった。

Study 08は、この未解決部分をpublic-online remote sensingだけで検討する独立研究として開始した。凍結済みhistorical studyの判定、閾値、endpoint、`historical transfer_to_zone_contribution = false`は変更対象にしなかった。

# 2. 研究対象

研究対象は、凍結済みGeoJSONに含まれる阿蘇の193 planning unitsである。空間identityはSHA-256 `46ef4dd475ec7645d78130722e8ddfcae9f51c6244ce95dc22ea9f7dcaa6609d`で固定した。

本研究の対象はremote-sensingと公開地図上の時系列的な状態・方向である。現地植生、個別の管理行為、土地所有者・管理者の意図、管理の効果、生物多様性応答は直接測定していない。

# 3. 研究目的と中心的研究質問

中心的研究質問は次のとおりである。

> 公開オンラインで再現可能な衛星・土地被覆資料を用いた場合、阿蘇の193 planning unitsについて、長期光学的変化、近年の草地適合性、木本クラスへの持続的地図遷移、センサー間不一致、歴史植生図との比較可能性を、凍結済み規則の範囲でどこまで推定できるか。

Study-level outcomeは`SUPPORTED_WITHIN_FROZEN_SCOPE`、`PARTIALLY_SUPPORTED`、`NOT_SUPPORTED`、`INDETERMINATE`、`NON_ESTIMABLE`、`ACCESS_LIMITED`、`STRUCTURALLY_UNAVAILABLE`、`INSUFFICIENT_TEMPORAL_COVERAGE`のいずれかとした。

# 4. 先行研究とnovelty boundary

NDVI、NDMI、NBR、Theil–Sen傾き、Landsat、Sentinel-2、PALSAR-2 FNF、土地被覆分類は既存の一般的方法・公開データであり、本研究はそれ自体の発明を主張しない。本研究の対象固有の貢献は、凍結済み193単位とprospective ruleの下で、複数sourceの取得、欠測、不一致、比較不能を救済せずに統合した点にある。

# 5. 使用した情報と使用しなかった情報

使用した情報はすべて`PUBLIC-ONLINE ONLY`である。

| Role | 情報源 | 期間・版 | 役割 |
|---|---|---|---|
| L1 | USGS Landsat Collection 2 Level-2 SR（Earth Engine経由） | 1985–2025 | 長期光学primary |
| S2 | Copernicus Sentinel-2 L2A harmonized（Earth Engine経由） | 2017–2025 | 近年光学secondary |
| C1 | JAXA HRLULC Japan v25.04 | 2020・2022・2024 | 草地・木本クラスの地図遷移proxy |
| R1 | JAXA PALSAR-2 FNF Ver.2.1.0 | 2017–2020 | SAR構造診断。取得不能のため`ACCESS_LIMITED` |
| H1 | 既存公開植生図のplanning-unit集計 | source creation year 2001・2007・2022 | read-only comparator |

行政照会、現地確認、直接観測、非公開local records、human researchは使用していない。JAXAおよびGoogle Earth Engineの登録は公開・無料datasetへのアクセス手段として扱い、認証情報は記録・commitしていない。

# 6. Prospective governanceとfreeze

正式Study ID、193単位のidentity、source role、対象期間、品質管理、光学指数、Theil–Sen方向規則、C1のクラス・面積・割合・patch閾値、欠測・不一致の扱い、outcome vocabularyを結果確認前に固定した。pre-execution validationはP1–P12すべてPASSだった。

Landsat年次全期間exportがEarth Engineでtimeoutしたため、1985–1991、1992–1998、1999–2005、2006–2012、2013–2019、2020–2025の6区間へ時間分割した。product、season、mask、index、geometry、reducerは変更していない。6区間は41年を欠落・重複なく再結合した。

# 7. 方法

## 7.1 Landsat

1985–2025年の7月1日–9月30日を対象に、Collection 2 Level-2 surface reflectanceからNDVI、NDMI、NBRの年次pixel medianを作成した。fill、cloud、cloud shadow、snow、cirrus、radiometric saturationを除外し、pixel-yearは2観測以上を要求した。planning-unit集計は30 m inward bufferと50% retained-area ruleを用いた。

各indexについて、20年以上の有限年次値と3時代すべてのsupportを要求し、Theil–Sen傾きと最初・最後の各5有効年medianの符号で方向を分類した。

## 7.2 Sentinel-2

2017–2025年の同一季節を対象に、`COPERNICUS/S2_SR_HARMONIZED`と`COPERNICUS/S2_CLOUD_PROBABILITY`を使用した。cloud probabilityは40%未満、10 m inward buffer、50% retained-area ruleを用いた。6年以上かつ6暦年以上のsupportを方向判定条件とした。

LandsatとSentinel-2の値は結合・平均せず、近年方向の一致、不一致、部分一致、比較不能を報告した。

## 7.3 JAXA HRLULC

v25.04の2020・2022・2024年を同一10 m gridで解析した。grassland classは5、woody classesは6・7・8・9・11とした。2020年草地から2022・2024年とも木本classへ移ったpixelについて、1.0 ha以上、2020年草地面積の5%以上、8-connected最大patch 0.5 ha以上をすべて要求した。

## 7.4 R1とH1

FNFは指定4 tiles×4 yearsを認証後UIで探索したが、必要なdownload linkが提供されなかったため`ACCESS_LIMITED`とした。代替version・year・classifierは用いていない。

H1には2001・2007・2022の異なるvintageが混在し、C1との共通日付・凍結済みカテゴリcrosswalkがない。このため、新たな結果依存crosswalkを作らず、全単位を`NOT_COMPARABLE`とした。

# 8. 主要結果

## 8.1 Endpoint A — temporal coverage

- Landsat eligible: **174/193（90.2%）**
- Landsat edge-retention/temporal insufficient: **19/193（9.8%）**
- Sentinel-2 eligible: **193/193（100%）**
- C1 three-epoch complete: **193/193（100%）**
- R1 eligible: **0/193、ACCESS_LIMITED**

## 8.2 Endpoint B — optical temporal trajectory

| 状態 | Landsat | Sentinel-2 |
|---|---:|---:|
| `OPTICAL_ALL_INCREASING` | 156 | 41 |
| `OPTICAL_ALL_DECREASING` | 2 | 9 |
| `OPTICAL_MIXED` | 16 | 143 |
| `OPTICAL_INSUFFICIENT` | 19 | 0 |

これらはspectral directionであり、草地状態、木本侵入、管理効果、生物多様性変化を直接表さない。

## 8.3 Endpoint C — grassland / woody-like map transition

| 状態 | planning units |
|---|---:|
| `PERSISTENT_GRASSLAND_COMPATIBLE` | 95 |
| `DECLINING_GRASSLAND_COMPATIBILITY` | 3 |
| `TRANSITIONING` | 95 |
| `WOODY_ENCROACHMENT_LIKE_STRUCTURAL_CHANGE` | 0 |

強い木本侵入様classが0であったことは、凍結済みC1 map-class ruleを満たす単位がなかったという結果である。現地の木本侵入がないことを示さない。

## 8.4 Endpoint D — uncertainty and validation

| Landsat/Sentinel recent-direction validation | planning units |
|---|---:|
| `CONCORDANT` | 16 |
| `DISCORDANT` | 7 |
| `PARTIAL` | 151 |
| `NOT_COMPARABLE` | 19 |

R1は`ACCESS_LIMITED`、SARとのvalidationは`NOT_COMPARABLE`である。センサー不一致は平均化して消していない。

## 8.5 Endpoint E — historical map comparison

`NOT_COMPARABLE`は193/193だった。これは歴史植生図が誤りという意味ではなく、異なるvintageと定義を同一カテゴリとして比較する凍結済み規則がなかったためである。

# 9. Formal outcome

```text
Study 08 outcome = PARTIALLY_SUPPORTED
```

L1、S2、C1から、長期・近年のspectral directionと2020–2024年のC1 map-class trajectoryは推定できた。一方、独立SAR構造診断R1が取得不能であり、H1比較も`NOT_COMPARABLE`だった。したがって、凍結済みscopeの一部は実行・検証できたが、要求された構造・validation componentの一部が欠ける場合に対応する`PARTIALLY_SUPPORTED`を適用した。

# 10. 本研究が支持すること

- 凍結済み193単位でLandsatの長期spectral directionを174単位について推定できる。
- Sentinel-2の近年方向を193単位について推定できる。
- 両光学センサーの方向は一様に一致せず、discordant・partial stateを明示する必要がある。
- C1 v25.04の3時点map-class trajectoryでは、95 persistent、3 declining、95 transitioningとなる。
- 凍結済み強判定条件を満たすwoody-encroachment-like transitionは0だった。
- R1欠測とH1比較不能を残したまま、研究をnegative/partial completionとして閉じられる。

# 11. 本研究が支持しないこと

- remote-sensing changeから特定の管理行為を同定すること
- vegetation trajectoryから因果的管理効果を推定すること
- spectral changeから火入れ、採草、放牧を識別すること
- C1 map-class trajectoryを現地確認済み木本侵入とみなすこと
- optical increase/decreaseを生物多様性の改善/悪化とみなすこと
- 後年衛星結果だけで歴史植生図を誤りと判定すること
- planning-unitごとの管理推奨を行うこと
- human validationが実施されたとみなすこと
- NAP-003を承認すること

# 12. 実務的含意

本結果は、193単位のどこで長期光学情報が十分か、C1上で近年のgrassland-compatible stateがどの分類になったか、センサー間でどの程度一致しないかを監査可能な形で示す。planningや追加調査の情報整理には使えるが、個別管理行為の選択や優先順位を直接決める根拠ではない。

# 13. 限界

1. R1 FNFが取得できず、独立L-band SAR構造診断を実行できなかった。
2. C1は複数sensorを使う外部produced mapであり、L1/S2から完全に独立したfield truthではない。
3. 2022 C1のpost-processingは2020/2024 class agreementに依存し得る。
4. Landsatは30 m inward bufferにより19単位が不足状態になった。
5. LandsatとSentinel-2はsensor、resolution、期間が異なり、値の直接結合を行っていない。
6. H1はheterogeneous vintageで、C1との凍結済みcategorical crosswalkがない。
7. slope GeoTIFFは同名既存Drive objectと現在task outputを区別できなかったため、SHA一致と来歴制約をmanifestへ記録し、formal PU optical-direction processorでは使用しなかった。
8. 現地確認、管理履歴、restricted local records、human validationは含まれない。
9. L1/S2 source-specific manifestのfreeze前に、header確認のためCSV先頭データ行が表示された。凍結済みthreshold、source、rule、codeはその後変更していないが、取得順序のprotocol deviationとしてmanifestとformal resultへ記録した。このため、manifest schemaの`resultValuesInspectedBeforeManifestFreeze = false` gateを満たしたとは主張しない。

# 14. 第三者資料・データの取扱い

大容量のEarth Engine exportとJAXA raster archiveはrepositoryへ再配布していない。repositoryには取得仕様、filename、byte size、SHA-256、processing scripts、集計結果を保存した。password、confirmation URL、登録情報、email contentsは保存していない。

# 15. 後続研究との境界

Study 08の科学的結果はsnapshot commitで凍結され、`main`へ統合された。Program Study 09は`PLANNED / NOT STARTED`であり、別のprospective start gateを必要とする。Study 09その他の後続研究は、Study 08やhistorical studyのformal resultを遡及的に書き換えてはならない。

`NAP-002 Study 2B = DEFERRED / NOT STARTED`、`human validation = NOT PERFORMED`、`Future NAP-003 = NOT AUTHORIZED`を維持する。

# 16. 再現性・検証

- Pre-execution validation: **P1–P12 PASS**
- Classification audit: **PASS**
- Adversarial audit: **PASS**
- Integrated planning-unit result: **193 rows / 193 unique pu_id**
- Historical firewall: **PASS**
- `historical transfer_to_zone_contribution`: **false**
- main integration: **COMPLETE AFTER SCIENTIFIC SNAPSHOT**

大容量raw bytesはGit外のpersistent local storageに保存し、L1/S2/C1 manifestへhashを記録した。Landsat分割年次CSVは1985–2025の41年を正確に再構成した。

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

# 18. Repository内の主要資料

Protocolとfreeze:

```text
doc/aso-grassland-temporal-change/ASO_GRASSLAND_TEMPORAL_CHANGE_PROSPECTIVE_PROTOCOL.md
doc/aso-grassland-temporal-change/PREEXEC_AMENDMENT_01.md
analysis/aso-grassland-temporal-change/prereg/STAGE_1_FORMAL_SPEC.json
```

Acquisition:

```text
analysis/aso-grassland-temporal-change/acquisition/L1_acquisition_manifest.json
analysis/aso-grassland-temporal-change/acquisition/S2_acquisition_manifest.json
analysis/aso-grassland-temporal-change/acquisition/C1_acquisition_manifest.json
analysis/aso-grassland-temporal-change/acquisition/R1_access_state.json
```

Results and audits:

```text
analysis/aso-grassland-temporal-change/results/study08_integrated_planning_unit_results.csv
analysis/aso-grassland-temporal-change/results/study08_endpoint_summary.json
analysis/aso-grassland-temporal-change/results/study08_formal_result.json
analysis/aso-grassland-temporal-change/results/study08_classification_audit.json
analysis/aso-grassland-temporal-change/results/study08_adversarial_audit.json
analysis/aso-grassland-temporal-change/results/study08_scientific_state_snapshot.json
```

# 19. 結論

Study 08は、公開オンライン証拠だけを用い、阿蘇の193 planning unitsについて長期・近年の光学方向とC1 map-class trajectoryを凍結済み規則で推定した。Landsatでは多くの単位が3指数すべて増加方向だったが、Sentinel-2ではmixedが多数であり、センサー間一致は限定的だった。C1ではpersistentとtransitioningが各95単位、decliningが3単位で、強いwoody-encroachment-like classは0だった。

R1が`ACCESS_LIMITED`、H1が全件`NOT_COMPARABLE`であることを保持したため、formal outcomeは`PARTIALLY_SUPPORTED`である。この完了状態は、欠測を埋めたり、閾値を緩めたり、管理・因果・現地植生の主張へ拡張した結果ではない。

# 用語

- **planning unit**: 本研究でidentityを凍結した193の空間単位。
- **optical direction**: NDVI・NDMI・NBRのTheil–Sen傾きとepoch差によるspectral direction。
- **grassland-compatible**: C1の明示的grassland classに基づく地図上の適合状態。
- **woody-encroachment-like**: 凍結済み面積・割合・patch条件を満たすmap-class trajectory。現地確認済み木本侵入ではない。
- **ACCESS_LIMITED**: 必要な公開sourceの凍結済みretrieval depthを再現可能に実行できなかった状態。
- **NOT_COMPARABLE**: 定義、時点、support、resolution等により、凍結済み範囲で比較できない状態。

# Selected methodological references / prior art

- USGS Landsat Collection 2: https://www.usgs.gov/landsat-missions/landsat-collection-2
- Copernicus Sentinel-2: https://dataspace.copernicus.eu/explore-data/data-collections/sentinel-data/sentinel-2
- JAXA High-Resolution Land-Use and Land-Cover Map of Japan v25.04: https://www.eorc.jaxa.jp/ALOS/jp/dataset/lulc/lulc_v2504_j.htm
- JAXA PALSAR-2/PALSAR Forest/Non-Forest Map: https://www.eorc.jaxa.jp/ALOS/en/dataset/fnf_e.htm

# 引用時の推奨表記

```text
Natural Area Planning / NAP-AGTC-2026-08-25-v1 (2026).
Public Research Report: 阿蘇草原の時系列変化・木本侵入様構造転換研究1.
Version 1.0, 2026-09-16.
Formal outcome: PARTIALLY_SUPPORTED.
Study snapshot: nkkmd/natural-area-planning @ 051c9c27bb3dec2a8f1409d25549b1441dfad097.
```