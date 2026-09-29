# Natural Area Planning / NAP-OEA-2026-08-16-v1 — 公開研究報告書

**運用手順の試験で未解決だった入力を、固定した判定時点でどこまで解消できるか**  
**― 出典・時間・地理・権限の条件を先に定め、証拠を取得する ―**

- レポート版: **v1.0.1**
- 日本語表現の改訂: **2026-09-28（科学的結果・正式判定は変更なし）**
- 作成日: **2026-08-24 JST**
- 研究ID: `NAP-OEA-2026-08-16-v1`
- 研究状態: **COMPLETE / FROZEN**
- 正式判定: **`PARTIAL_TARGET_INPUT_RESOLUTION`**
- 正式評価時点: **2026-08-24 12:00 JST**
- 科学的結果を確定した時点: **`3788ba409956cc9806d0877a3bfa94e6fdd6258a`**
- 本文の性格: **外部公開用・単体完結型研究報告**

この文書は、元のGitHubリポジトリや内部の成果物を参照しなくても、本研究の背景、問い、方法、主要結果、限界、再現性、解釈境界を理解できるように構成している。出典と処理を追跡できる資料、機械で読み取れる正式な資料は、末尾に示す研究計画・正式結果・進捗記録などに収めている。


## 初めて読む方へ

この報告書は、研究05で未解決だった運用情報30件を、決められた時点までにどこまで確認できるか調べた研究です。気象に関する2件を解決し、28件は未解決でした。正式判定は `PARTIAL_TARGET_INPUT_RESOLUTION`（対象となる入力の一部を解決）です。管理の推奨や安全性の確認を意味するものではありません。

本文の研究ID、正式判定コード、数値、出典識別子は、研究結果と照合できるよう原表記を残しています。

# 要旨

先行する運用手順の試験では、不足・未検証の情報を安全性や許可の確認済み情報と取り違えず、意思決定支援の手順で扱えることを示した。しかし、必須入力192件のうち実際に使える情報は0件だった。そこで本研究は、未解決の入力そのものを、追加の資料によってどこまで解決できるかを調べた。

先行研究の結果は変更せず、値を見る前に30件の対象となる入力を選んだ。法令上利用できる公開・地域・利用制限付きの情報、または手順に従った直接観察を証拠の候補とし、固定した判断時点 T0 = 2026-08-24T12:00:00+09:00 における情報の有効性を確認した。

結果は次のとおりである。

```text
target cells = 30
resolved = 2
unresolved = 28
blockers released = 2
EA1-EA11 = PASS
adversarial cases = 22 / 22 PASS
formal outcome = PARTIAL_TARGET_INPUT_RESOLUTION
```

解決できた2件はいずれも現時点の気象に関する入力で、気象庁のアメダス「阿蘇乙姫」（86111）を、事前に定めた最も近い公式の参照気象情報として使った。残る28件は規則を緩めず未解決のまま保持した。

この結果は、出典、時間、地理的な結び付き、情報の権限に関する条件を守りながら、事前に選んだ入力の一部を判断時点で確認できたことを示す。**管理行為の推奨・順位付け、安全性、許可、生態学的な効果、人による受容性を示すものではない。**

# 1. 研究の背景

Natural Area Planningでは、公開情報だけで管理方法を明示した計画へ進む際の証拠上の限界をNAP-001で検証し、その後NAP-002 Study 1で、管理行為を推奨せずに管理の検討対象、判断を妨げる要因、次に必要な情報を表現する意思決定支援の手順を構築した。

NAP-002 Study 2Aはその表現を人間参加者を使わずに事前検証し、G4 Response-Transfer Validation Study v1は元の調査地点で得られた生態学的応答を別の場所へ適用するための独立した検証の証拠を評価した。G4 v1は条件を満たす独立した検証対象が0で `INDETERMINATE` となった。

Operational Pilot v1はさらに、地域固有・現時点の運用情報を手順につなぐ方法を結果を見る前に定めて検証を行った。その正式判定は `WORKFLOW_VALIDATED_WITHIN_PILOT_SCOPE` だったが、使用できる必須入力は0/192で、30件の試験事例のいずれも運用上の判断に必要な条件を満たさなかった。

そのため次の科学的問いとして、**未解決の運用入力そのものを、事前固定したルールのもとで実際にどこまで解消できるか**を独立した研究として検証する必要が生じた。

# 2. 研究対象

本研究の研究対象は、Operational Pilot v1で未解決だった必須の運用入力のうち、値を見ずに結果を見る前に選択した30件である。

対象には次の運用情報の領域が含まれた。

```text
LOCAL_AUTHORITY_FEASIBILITY
LOCAL_ACTION_SPECIFICATION
LOCAL_ACCESS_FEASIBILITY
LOCAL_INFRASTRUCTURE_FEASIBILITY
CURRENT_PERMISSION_OR_RESTRICTION
CURRENT_SITE_CONDITION
CURRENT_WEATHER_CONDITION
CURRENT_FUEL_OR_BIOMASS_CONDITION
```

本研究の対象ではないものは次のとおりである。

```text
management recommendation
action ranking
ecological response estimation
planning-unit ecological coefficient
human-participant usability validation
G4 ecological transfer reinterpretation
optimization
```

# 3. 研究目的と中心的研究質問

中心的研究質問は次のとおりである。

> Operational Pilot v1で未解決だった運用入力のうち、結果を見る前に固定した対象となる30件の入力について、適法に利用可能で出典・時間・地理・権限の条件を満たす証拠を用いたとき、固定T0時点で何件を再現可能に解決できるか。

正式判定の区分は結果を見る前に固定され、すべての判定条件に合格した場合に `0 < resolved < targetCount` の場合は `PARTIAL_TARGET_INPUT_RESOLUTION` とするルールが採用された。

# 4. 先行研究との関係と新規性を主張できる範囲

本研究は、出典の記録や事前に定める研究手順、時間的な有効性、権限の優先順序、構造化した意思決定支援といった一般的方法論自体を新規発明として主張しない。

対象固有の新規性は、Natural Area Planningの確定済みの運用手順の試験結果から未解決の運用入力を値非依存で選択し、固定T0に対して、元データのバイト数と出典・処理の履歴、資料の権限、地理的な対応、確認対象ごとの情報の有効期間、未解決であることを明示した状態を同時に維持しながら正式な情報収集の結果を評価した点にある。

本研究は先行研究の否定的・結果なし・判定不能という結果を救済するための再解析ではない。

# 5. 使用した情報・使用しなかった情報

本研究では、事前に定めた研究手順で許可した、一般公開されている公式のオンライン情報を第一経路とした。適法に利用できる制限付き・地域の資料や事前手順に従った現地での直接観察も研究計画で認めた証拠の種類として定義されたが、正式な解決に必須ではなかった。

本研究では次を使用していない。

```text
human participant data
unlawfully accessed restricted data
repository privacyをaccess authorizationとみなした情報
valueを見た後に選択した代替target
favorable conditionを選ぶためのsource switching
weatherをfuel conditionへ代用した値
generic regional proxyをPU-specific evidenceとみなした値
post-T0 evidenceによるfrozen endpointの救済
```

# 6. 結果を見る前に確定した研究規則

新しい運用情報の値を確認する前に、少なくとも次を固定した。

```text
study identity
target-selection rules
30-cell target frame
evidence modes A-D
authority ceilings
raw provenance rules
lawful-access rules
temporal-validity rules
conflict hierarchy
missing/unresolved state vocabulary
direct-observation protocol
formal gates EA1-EA11
22 adversarial cases
formal outcome vocabulary
exact T0
Package 003 domain-specific freshness windows
weather station and spatial ceiling
```

実施前の検証は `PRE1-PRE11 = PASS`、T0を固定したことの検証もPASSした後に情報収集を開始できる状態になった。

# 7. 方法

## 7.1 対象となる入力

対象となる30件の入力はOperational Pilot v1の確定済みの状態から定めた規則に従って選択した。新しい地域固有・現時点の値は選択、件数調整、差し替えに使用していない。

資料群の構成は次のとおりである。

```text
Package 001: LOCAL_AUTHORITY_FEASIBILITY = 7 targets
Package 002: non-short-window operational inputs = 16 targets
Package 003: short-window current-condition inputs = 7 targets
```

## 7.2 出典の確認条件

正式な証拠として使用する元データは、解析前に少なくともバイト数とSHA-256を記録することを要求した。

```text
raw acquisition
-> byte count + SHA-256 materialization
-> parse
-> derived evidence state
```

検索結果の抜粋や候補探しだけに用いた資料は、正式な証拠として採用しなかった。

## 7.3 時間的な有効性

取得時刻と、情報の有効時刻・現象時刻・観測時刻を分離した。取得時刻を観測時刻の代用にはしていない。

資料群003の主な有効期間は次のとおりである。

```text
CURRENT_SITE_CONDITION
  2026-08-24 06:00–12:00 JST

fuel moisture / combustibility
  2026-08-24 09:00–12:00 JST

standing biomass / height / cover
  2026-08-23 12:00–2026-08-24 12:00 JST

CURRENT_WEATHER_CONDITION official observation
  2026-08-24 11:00–12:00 JST
```

## 7.4 気象データの選び方

気象については、値を見る前に観測所 `86111 / 阿蘇乙姫` を、対象の計画単位の範囲を囲む長方形の中心に最も近い気象庁アメダス観測所として固定した。

空間的な対応区分は次のとおりである。

```text
NEAREST_OFFICIAL_REFERENCE_WEATHER
```

これは観測所で得た公式の観測値を計画単位の参考値として使用する分類であり、計画単位内で観測した値やその場所の局所気象を正確に測った値ではない。

確認する気象項目は次の5種類に固定した。

```text
hourly precipitation
hourly air temperature
hourly relative humidity
hourly mean wind speed
hourly wind direction
```

11:00–12:00 JST内の最新の欠測のない公式の1時間ごとの観測値を使用し、予報での代用、都合の良い値の選択、観測所の変更を禁止した。

## 7.5 未解決の入力の扱い

凍結条件を満たす事例の場所と時点を特定できる公式記録を取得できない場合、条件を緩和して解決したことにせず、`NO_COMPLIANT_RECORD_ACQUIRED` 等の最終的に未解決となった状態を保持した。

# 8. 主要結果

正式な結果は次のとおりである。

```text
target cells = 30
resolved = 2
unresolved = 28
blockers released = 2
resolution rate = 2 / 30
EA1-EA11 = PASS
formal outcome = PARTIAL_TARGET_INPUT_RESOLUTION
```

資料群ごとの結果:

```text
Package 001 = 0 / 7 resolved
Package 002 = 0 / 16 resolved
Package 003 site = 0 / 3 resolved
Package 003 fuel / biomass = 0 / 2 resolved
Package 003 weather = 2 / 2 resolved
```

## 8.1 解決した2件

解決したのは、事前固定された2件の `CURRENT_WEATHER_CONDITION` のみである。

T0時点で気象庁から取得した元データについて、解析前に次の識別情報を記録した。

```text
raw bytes = 8375
SHA-256 = f7b7e2c570b8ea924619eb831bb23f5ed689a39ea10b7dddf7ea630fcc6eb0e2
```

事前に定めた11:00–12:00 JSTの時間帯内で利用可能だった最新の欠測のない1時間単位の観測値は11:00 JST観測だった。

```text
station = 86111 / 阿蘇乙姫
phenomenon time = 2026-08-24T11:00:00+09:00
1時間降水量 = 0.0 mm
気温 = 29.7 C
相対湿度 = 60 %
平均風速 = 1.2 m/s
風向コード = 11
verification ceiling = VERIFIED_PERMITTED_NONCONTROLLING_SOURCE
```

## 8.2 解決しなかった28件

資料群001の7件、資料群002の16件、資料群003の現地状態3件と燃料・バイオマス状態2件は解決しなかった。

条件を満たす記録を取得できなかった場合は条件を緩和せず未解決を維持した。`NO_COMPLIANT_RECORD_ACQUIRED` は、現実世界で情報、権限、現況、燃料状態が存在しないことを意味しない。

# 9. 本研究が支持すること

本研究は次を支持する。

1. 事前固定した未解決の運用入力30件のうち、厳格な証拠の確認規則を維持したままT0時点で2件を正式に解決できた。
2. 出典の確認、時間的な有効性、地理的に言える範囲、資料の権限、不明を不明のまま扱う規則を保持したまま正式な資料の作成を完了できた。
3. 28件について条件を満たす証拠が取得できなかった場合にも、対象の差し替えや代替値を認める条件の緩和を行わず未解決という状態を保持できた。
4. 最初の資料作成と独立した再計算が同一の30/2/28および正式判定を再現した。

# 10. 本研究が支持しないこと

本研究は次を支持しない。

```text
気象に関する2件が「管理に好都合な条件」だった
観測所の参考値が計画単位内の局所気象を正確に表す
判断を妨げる要因が2件減ったので管理行為を推奨できる
解決できた割合が管理行為の優先順位を表す
NO_COMPLIANT_RECORD_ACQUIRED が、情報や現地の状態が実際に存在しないことを表す
現時点の運用情報が生態学的な管理への応答を示す
G4の生態学的な応答を別の場所に適用できることが確かめられた
実在する人による検証が完了した
計画用の係数や最適化計算の入力が得られた
```

# 11. 実務的含意

本研究の実務的含意は、運用上の意思決定支援に必要な現時点・地域固有の事実を扱う際、**取得できた値だけでなく、取得できなかった状態を正式な判断を妨げる要因として保持する必要がある**という点にある。

また、公式の出典であっても地理的に参考値である場合には、その適用範囲の限界を明示して利用する必要がある。今回の気象の証拠はその例であり、公式の観測所での観測であることと計画単位内での観測であることは区別された。

# 12. 研究上の限界

主な限界は次のとおりである。

1. **証拠の対象範囲の限界**: 30件中28件は正式な解決に至らなかった。
2. **時間上の限界**: 現時点の状態を示す証拠は固定T0と短い有効期間に強く依存する。
3. **地理的な限界**: 気象の情報は最も近い公式観測所による参考値であり、計画単位内の観測ではない。
4. **資料の利用に関する限界**: 利用に制限のある地域資料が存在しても、適法な利用、事例との対応、有効期間、権限の条件を満たさなければ正式な証拠にはできない。
5. **直接観察に関する限界**: 現地での直接観察は手順上認められていたが、本研究の正式な解決を構成する必須経路ではなく、今回の解決2件は公開された公式の気象情報による。
6. **生態学上の限界**: 運用情報の収集は管理への応答や生態学的な有効性を測定しない。
7. **人間参加者による検証に関する限界**: 実務者や行政担当者を研究参加者としていない。
8. **資料の取得に関する限界**: 公開されたオンライン資料の検索・公開の時期によって、現実に存在する情報を取得できない可能性がある。記録が見つからないことは、実際に存在しないことを意味しない。

# 13. 第三者資料・データの取扱い

本研究では、リポジトリが非公開であることを適法な利用の根拠や再配布する権利とはみなしていない。利用に制限のある元データや機密の元データをリポジトリに登録することを原則にはしていない。

第三者の資料については、正式な結果の再現に必要な出典の識別情報、分析後の状態、ハッシュ値等を記録し、不必要な個人情報や利用に制限のある元資料の内容の再配布を避ける方針を採用した。

# 14. 後続研究との境界

OEA v1は科学的な結果を確定済みであり、T0の後に取得した証拠を追加して未解決の28件を救済してはならない。

後続研究で追加の運用情報の収集を行う場合は、新しい研究ID、新しい判定時点または期間、新しい対象範囲、新しい出典・利用規則を結果を見る前に確定する必要がある。

G4の後続研究、NAP-002 Study 2B、将来のStage A/B、NAP-003はそれぞれ別の研究経路であり、OEA v1の結果から自動的には開始されない。

# 15. 再現性・検証

正式な判定条件:

```text
EA1  PASS  target traceability
EA2  PASS  provenance identity
EA3  PASS  geographic / jurisdiction linkage
EA4  PASS  temporal validity
EA5  PASS  source / authority ceiling
EA6  PASS  state-transition integrity
EA7  PASS  evidence-only blocker release
EA8  PASS  missingness / conflict discipline
EA9  PASS  historical / ecological / human firewall
EA10 PASS  independent recomputation
EA11 PASS  registered adversarial cases
```

誤読を想定した検証:

```text
registered = 22
passed = 22
```

最初の資料作成と独立した再計算は、いずれも次を返した。

```text
30 total
2 resolved
28 unresolved
PARTIAL_TARGET_INPUT_RESOLUTION
```

# 16. 再現性識別子

```text
study ID = NAP-OEA-2026-08-16-v1
scientific-state snapshot = 3788ba409956cc9806d0877a3bfa94e6fdd6258a
exact T0 = 2026-08-24T12:00:00+09:00
formal outcome = PARTIAL_TARGET_INPUT_RESOLUTION
targets = 30
resolved = 2
unresolved = 28
blockers released = 2
materialization canonical SHA-256 = b5516c84628bb038b18fe6520e17bd01f85e47c7b84aeebe275330ca3c83ba89
T0 weather raw SHA-256 = f7b7e2c570b8ea924619eb831bb23f5ed689a39ea10b7dddf7ea630fcc6eb0e2
```

# 17. リポジトリ内の主要資料

## 研究計画と運用規則

- `doc/operational-evidence-acquisition/OPERATIONAL_EVIDENCE_ACQUISITION_PROSPECTIVE_PROTOCOL.md`
- `analysis/operational-evidence-acquisition/oea_design_registry.json`
- `analysis/operational-evidence-acquisition/oea_target_selection_rules.json`
- `analysis/operational-evidence-acquisition/oea_temporal_validity_rules.json`
- `analysis/operational-evidence-acquisition/oea_provenance_access_rules.json`
- `analysis/operational-evidence-acquisition/oea_t0_registry.json`

## パッケージ003の実行

- `analysis/operational-evidence-acquisition/oea_package_003_execution_rule.json`
- `analysis/operational-evidence-acquisition/oea_package_003_site_condition_status.json`
- `analysis/operational-evidence-acquisition/oea_package_003_fuel_biomass_status.json`
- `analysis/operational-evidence-acquisition/oea_pkg003_weather_t0_raw_identity.json`
- `analysis/operational-evidence-acquisition/oea_pkg003_weather_t0_result.json`
- `analysis/operational-evidence-acquisition/oea_package_003_formal_status.json`

## 正式結果と検証

- `analysis/operational-evidence-acquisition/oea_formal_result.json`
- `analysis/operational-evidence-acquisition/oea_formal_validation.json`
- `analysis/operational-evidence-acquisition/oea_formal_reproducibility.json`
- `doc/checkpoints/2026-08-24-operational-evidence-acquisition-formal-closure.md`
- `doc/operational-evidence-acquisition/CURRENT_STATUS.md`

# 18. 結論

事前に選んだ未解決の運用入力30件のうち、出典、時間、地域、権限の条件を守ったうえで、判断時点T0に正式に解決できたのは2件だった。残る28件は条件を緩めず未解決のまま保持した。正式判定は PARTIAL_TARGET_INPUT_RESOLUTION（対象となる入力の一部を解決）である。

これは気象に関する2件が管理上望ましい状態だったという意味ではない。**必要な形式の証拠を2件について取得・確認でき、ほかの28件については証拠不足を隠さず残した**ことが結果である。

---

# 用語

**T0**  
運用情報の証拠を評価するために、共通に定めた判断時点。本研究では2026-08-24 12:00 JST。

**NO_COMPLIANT_RECORD_ACQUIRED**  
事前に定めた出典・確認対象・地理・時間の条件を満たす記録を取得できなかった状態。現実に情報や現地の状態が存在しないという意味ではない。

**NEAREST_OFFICIAL_REFERENCE_WEATHER**  
対象となる計画単位について、事前に選んだ最も近い公式観測所の値を参考値として用いる区分。計画単位内での観測を意味しない。

**VERIFIED_PERMITTED_NONCONTROLLING_SOURCE**  
正式な手順で確認できる資料だが、対象となる現地の状況を直接示す資料ではない場合の確認上の区分。

**判断を妨げる要因の解除（blocker release）**  
必須入力が正式な証拠で解決し、対応する判断を妨げる要因を規則に従って解除すること。管理の推奨や優先順位を意味しない。

# 参考文献・関連する先行研究

本研究が用いた一般的な方法には、結果を見る前に研究規則を定めること、出典と処理の履歴を記録すること、情報の時間的な有効性と権限を確認すること、不明な状態を明示した意思決定支援がある。これらの方法そのものを新たに発明したとは主張しない。

本研究に直接つながる先行報告書は次のとおりである。

- `NAP001_PUBLIC_RESEARCH_REPORT.md`
- `NAP002_STUDY1_PUBLIC_RESEARCH_REPORT.md`
- `NAP002_STUDY2A_NONPARTICIPANT_PREVALIDATION_PUBLIC_REPORT.md`
- `G4_RESPONSE_TRANSFER_VALIDATION_PUBLIC_REPORT.md`
- `OPERATIONAL_PILOT_PUBLIC_REPORT.md`

# 引用時の推奨表記

```text
Natural Area Planning / NAP-OEA-2026-08-16-v1 (2026).
Public Research Report:
「運用手順の試験で未解決だった入力を、固定した判定時点でどこまで解消できるか
― 出典・時間・地理・権限の条件を先に定め、証拠を取得する ―」
Version 1.0.1, 日本語表現改訂 2026-09-28（科学的結果は2026-08-24確定）。
Formal outcome: PARTIAL_TARGET_INPUT_RESOLUTION.
Study snapshot: nkkmd/natural-area-planning @ 3788ba409956cc9806d0877a3bfa94e6fdd6258a.
```