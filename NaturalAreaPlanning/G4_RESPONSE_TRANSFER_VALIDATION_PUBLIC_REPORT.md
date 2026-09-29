# Natural Area Planning / G4-RTV-2026-08-14-v1 — 公開研究報告書

**元の調査地点で得られた管理への応答は別の場所に適用できるか**  
**― 検証条件を先に決めた結果、公開情報だけでは独立した検証対象を確保できなかった ―**

- **レポート版:** v1.0.1
- 日本語表現の改訂: **2026-09-28（科学的結果・正式判定は変更なし）**
- **作成日:** 2026-08-14 JST
- **研究ID:** `G4-RTV-2026-08-14-v1`
- **研究状態:** `COMPLETE / FROZEN`
- **正式判定:** `INDETERMINATE`
- **正式判定の理由:** `NO_ELIGIBLE_INDEPENDENT_HELDOUT_RESPONSE_VALIDATION_CONTEXTS`
- **研究結果を確定したコミット:** `1e56878979d3163638768a7b769408a82c4b3629`
- **基点となるmainのコミット:** `2087e6c40108e991d586174b5619ad16dfd9176e`
- **本文の性格:** 外部公開用・単体完結型研究レポート
- **編集上の扱い:** 研究結果を確定した上記コミットの後に公開用として編集した文書であり、正式な科学的結果は変更していない

> この文書は、GitHubリポジトリや内部の成果物を参照しなくても、本研究の背景、問い、方法、主要結果、限界、再現性、解釈境界を理解できるように構成している。出典と作業履歴の詳細を確認する場合は末尾のリポジトリ内の主要資料を参照されたい。

---


## 初めて読む方へ

この報告書は、ある調査地点で観察された管理への応答を、別の場所に適用できるか検証した研究です。事前に定めた条件に合う独立した検証対象は0件だったため、正式判定は `INDETERMINATE`（判定不能）です。管理効果の適用が失敗したと判定したものではありません。

本文の研究ID、正式判定コード、数値、出典識別子は、研究結果と照合できるよう原表記を残しています。

# 要旨

先行研究では、元の調査地点で観察された管理への応答を、阿蘇の各計画単位でも成り立つ応答として自動的に扱えないことが分かった。NAP-002の研究1は、この境界をG4のDO_NOT_INFER（推論しない）という判定に反映し、確定済みの transfer_to_zone_contribution=false を維持した。

本研究は、管理への応答を別の場所に適用できるか、その条件を独立に検証した。研究の目的はG4を合格にすることではない。適用してよい条件と判断を止める条件を結果を見る前に決め、その規則に従って公開証拠を確認することである。

研究開始前に、管理方法と測定する結果の定義、元の調査地点と適用先の条件、出典の重複、適用可否の判定区分、不合格時の扱い、検証と再現の方法を確定した。主要な関係を8類型、外部の候補資料を6件に定めた。一次資料のPDFを公式の公開経路から取得してハッシュ値を確定できた資料は5件だった。残る1件は公式の出版者の経路がHTTP 403となり、取得未完了として扱った。

第7段階では、生態学的な応答の方向を採点する前に、出典・独立性・管理方法と結果の定義の一致・必要な現地条件が揃うかを監査した。結果は次のとおりである。

```text
external candidate sources                  = 6
public-primary sources hash-frozen          = 5
acquisition-incomplete sources              = 1
external source x relation rows             = 12
eligible held-out source x relation rows    = 0
eligible independent held-out clusters      = 0
structurally excluded rows                  = 12
held-out ecological response values read    = false
```

事前に定めた条件を満たす独立した検証用資料は0件だった。そこで8類型すべてを次の状態とした。

```text
NO_INDEPENDENT_VALIDATION_EVIDENCE
```

これは独立した検証の証拠がないことを表す。**TRANSFER_NOT_SUPPORTED（適用は支持されない）とは判定していない。** 応答の適用に失敗したのではなく、その成否を独立に検証できる対象がなかったためである。

第8段階の事前規則に従い、研究全体の正式判定は次のとおりとした。

```text
INDETERMINATE
```

公開情報から管理への応答を別の場所に適用できることも、できないことも示していない。管理方法の名称や場所が似ているだけでは足りず、管理内容、測定結果、適用先の条件、出典の独立性を同時に確認する必要がある。今回定めた第1版の資料群では、その条件を満たす独立した証拠を確保できなかった。

先行研究の transfer_to_zone_contribution=false は変更していない。計画単位ごとの生態学的応答、管理の推奨、区域への寄与量の係数、最適化の入力、人にとっての使いやすさや実務上の効果も承認していない。人間を対象としたNAP-002の研究2Bは未着手である。

---

# 1. 研究の背景

## 1.1 先行研究で残ったG4の課題

NAP-001のステージCでは、公開情報を用いて阿蘇半自然草原の管理方法を明示した計画へ進める範囲を検証し、次の結果で閉じた。

```text
Q3 planning-response features = 0
Q4 local response models = 0
zone contribution rows = 0
formal optimizer authorized = false
```

ここで重要だったのは、元の調査地点で観察された管理への応答が存在することと、計画単位でその応答が成立することは別の主張だという点である。

NAP-002の研究1は、その証拠から言える範囲を壊さずに意思決定支援へ翻訳した。G3で出典に基づく管理への応答の証拠が`SUPPORTED_SOURCE_LOCAL`になっても、G4では、

```text
SUPPORTED_SOURCE_LOCAL
-> DO_NOT_INFER + RESPONSE_TRANSFER_VALIDATION
```

と扱った。

つまり、

```text
source-local response
!=
planning-unit response
```

が研究全体に残る課題だった。

## 1.2 なぜ独立研究が必要だったか

この障壁を解消するには、既存の研究1で定めた規則を結果に合わせて緩めるのではなく、**管理への応答を別の場所へ適用できるかを、結果を見る前に計画した独立研究で検証する**必要がある。

本研究は、NAP-001、NAP-002 Study 1、NAP-002の研究2Aの確定済みの結果を変更・救済・再解釈するための研究ではない。

また、NAP-002の研究2Bが扱う人にとっての使いやすさとは科学的問いが異なる。

```text
human usability
!=
ecological response transferability
```

---

# 2. 研究対象

本研究が対象としたのは、**管理方法と生態学的な応答の関係を異なる場所へ適用できるか**である。

基本単位は、概念的には次の組合せとして定義した。

```text
source context
x source cluster
x management exposure definition
x comparator definition
x ecological outcome construct
x outcome target
x measurement definition
x observation window
x response precision
```

主に判定する応答の精度は、

```text
DIRECTIONAL_RESPONSE
```

とした。

本研究の主たる研究対象ではないものは次のとおりである。

```text
human usability
practitioner preference
workflow fit
management recommendation
operational feasibility
safety / permission
planning-unit optimization coefficient
```

---

# 3. 研究目的と中心的研究質問

中心的研究質問は、結果を見る前に確定した研究計画で次の趣旨として固定した。

> 元の調査地点で観察された管理への応答を、管理方法・測定する結果・元の調査地点と適用先の条件について、事前に定めた一致の条件のもとで、独立した検証対象へ同じ精度で適用できるか。また、その条件を満たさない場合、どの適用が支持されない状態や証拠不足の状態として閉じるべきか。

結果の状態は、単純な二択 `transferable / not transferable`ではなく、次を含む形で事前に定めた。

```text
SUPPORTED_FOR_TRANSFER
CONDITIONAL_TRANSFER
TRANSFER_NOT_SUPPORTED
INSUFFICIENT_CONTEXT
INCOMPATIBLE_MANAGEMENT
INCOMPATIBLE_OUTCOME
NO_INDEPENDENT_VALIDATION_EVIDENCE
INDETERMINATE
```

不支持、条件を満たさない状態、証拠不足、判定不能のいずれも正式な科学的結果になり得る設計とした。

---

# 4. 先行研究・新規性を主張できる範囲

管理への応答の転用、外的妥当性、一般化可能性、転用可能性は新しい概念ではない。

生態学ではWenger & Olden (2012)が、通常の無作為な分割だけではなく、空間・時間・その他の異なる群を意図的に検証用に残すことで、別の場所・時期・データへの適用可能性を評価する重要性を論じている。

因果推論ではBareinboim & Pearl (2013)が、条件の異なる元の集団から対象の集団へ効果を移せる条件を形式的に扱っている。Dahabreh et al. (2020)も、元の集団から対象の集団へ推論を拡張する際に、参加の有無、対象集団の違い、効果を変える要因を明示的に扱う枠組みを示している。

より近年の生態学でも、Dumandan et al. (2024)は新たな生物学的条件で生態予測モデルを適用できるかを長期実験で直接評価している。

したがって、本研究は「別の場所への適用可能性」という概念そのものを新規のものとは主張しない。

本研究で独自に実装した対象固有の部分は、Natural Area Planningに残ったG4の課題に対し、

```text
management-definition compatibility
x outcome-definition compatibility
x relation-specific context-domain rule
x source independence / duplicate firewall
x explicit non-transfer / insufficient-evidence states
x historical-endpoint firewall
```

を結果を見る前に定めた一連の判定条件として実装し、公開情報に基づいて実際に判定できるかを検証した点にある。

---

# 5. 使用した情報 / 使用しなかった情報

## 5.1 先行研究で確定した入力

NAP-001とNAP-002の既存の成果物は、結果を書き換えずに参照した。

```text
historical frozen artifact
-> new G4 study input
```

主な先行研究の入力には次が含まれる。

```text
analysis/nap001/t2_t4_management_response_transfer_evidence.csv
analysis/nap001/source_exposure_regime_crosswalk.csv
analysis/nap001/regime_feature_evidence_relations.csv
analysis/nap001/management_regimes.csv
analysis/nap001/conservation_features.csv
analysis/nap002/g3_evidence_class_definitions.csv
analysis/nap002/g2_g5_transformation_rules.csv
```

## 5.2 公開情報から選んだ外部候補資料

第7段階では、次の6件を外部資料の候補として確定した。

| 資料ID | DOI・識別子 | 候補となる主な関係 | 第7段階の出典確認 |
|---|---|---|---|
| `NAP-T24-EXT-001` | `10.14941/grass.42.307` | T2/T4・人工的な圧力 | 公開された一次資料のPDFを取得しハッシュ値を確定 |
| `NAP-T24-EXT-002` | `10.14941/grass.53.28` | 刈取り・火入れ | 公開された一次資料のPDFを取得しハッシュ値を確定 |
| `G4-EXT-003` | `10.14941/grass.60.102` | 火入れ・放牧・植生 | 公開された一次資料のPDFを取得しハッシュ値を確定 |
| `G4-EXT-004` | `10.14941/grass.51.143` | 管理継続地と放棄地の草原 | 公開された一次資料のPDFを取得しハッシュ値を確定 |
| `G4-EXT-005` | `10.20848/kontyu.6.2_89` | *Shijimiaeoides divinus asonis* 生息地・個体群 | 公開された一次資料のPDFを取得しハッシュ値を確定 |
| `G4-EXT-006` | `10.1111/1440-1703.12494` | 放牧・チョウ類群集 | `ACQUISITION_INCOMPLETE_OFFICIAL_ROUTE_403` |

## 5.3 使用しなかった情報

本研究では次を使用していない。

```text
restricted/local non-public data
real-person participant data
Study 2B human-validation data
planning-unit direct ecological response panel
post-Phase-7 rescue source
excluded source response values for G4 scoring
LLM-generated ecological effect estimate
```

第7段階で資料が構造上の条件を満たさないと判定された後、その資料の応答の方向を見て適格性の規則を緩めていない。

---

# 6. 結果を見る前に確定した研究規則

## 6.1 独立した研究ID

研究開始時に、

```text
Study ID = G4-RTV-2026-08-14-v1
Study type = prospective independent public-only response-transfer validation
```

としてNAP-001 / NAP-002とは独立した研究の識別情報を作成した。

## 6.2 結果より前に固定した事項

検証用に残した資料の応答を採点する前に、少なくとも次を確定した。

- 主要な関係の類型
- 管理方法の一致に関する条件
- 測定結果の一致に関する条件
- 適用先の条件が判定に必要か
- 出典の重複と独立性の扱い
- 公開された一次資料の出典に関する条件
- 欠測の扱い
- 適用可否に関する判定状態
- 全面的な支持と判定する最低条件
- 条件不適合や証拠不足の場合の規則
- 適用先の条件について分かる範囲の限界
- 誤読を想定した事例
- 応答を確認する前に規則を固定する条件

## 6.3 支持と判定する条件

`SUPPORTED_FOR_TRANSFER`（転用を全面的に支持）と判定するための最低条件を、概ね次のように事前に定めた。

```text
>= 1 derivation/source context
>= 2 independent assessable held-out contexts
all assessable in-domain validation contexts concordant
any in-domain discordance blocks full support
mandatory management/outcome/context gates must pass
```

これは普遍的な生態法則としてのしきい値ではなく、本研究で応答を別の場所へ適用する全面的な承認を与えるための慎重な規則である。

## 6.4 重複する出典を除外する規則

論文数を独立した反復検証の件数に変換しないため、出典群を事前に固定した。

例として、

```text
A-04 + A-05 + Murata/Nohara 2003
-> one conservative Aso Shijimiaeoides research-program cluster
```

とし、応答を見る前に確認できる研究方法の情報から独立性を証明できない限り複数の検証対象に数えないこととした。

---

# 7. 方法

## 7.1 8つの主要な関係の類型

本研究は次の8類型を対象とした。

| ID | 管理方法の比較 | 生態学的な結果 |
|---|---|---|
| `G4-RF-01` | 管理の継続と停止・放棄 | T2の遷移・種組成 |
| `G4-RF-02` | 管理の継続と停止・放棄 | T4の開放草原の構造 |
| `G4-RF-03` | 刈取りの時期・頻度 | T2の遷移・種組成 |
| `G4-RF-04` | 刈取りの時期・頻度 | *Primula sieboldii* |
| `G4-RF-05` | 刈取りの時期・頻度 | ケルリソウ / *Cynoglossum asperrimum* |
| `G4-RF-06` | 放牧の強度 | *Shijimiaeoides divinus asonis* |
| `G4-RF-07` | 放牧の強度 | チョウ類群集の応答 |
| `G4-RF-08` | 放牧の強度 | 希少な草原性チョウ類の応答 |

## 7.2 管理方法の定義が一致するか

「同じ放牧」「同じ火入れ」「同じ刈取り」という名称だけで適合とは判定しなかった。

関係の類型に応じて、次を必ず確認する観点として扱った。

```text
management type
intensity
timing
frequency
duration / history
background burning
grazing background
mowing background
biomass removal
cessation / continuation state
livestock type
comparator definition
```

特に刈取りでは、

```text
July
September
twice-yearly
biennial
```

を一律に「刈取り」とまとめることを禁止した。

A-04/A-05由来の放牧の強度でも、二択の `grazed`だけからLOW / CUSTOMARY / HIGHへ割り当てることを禁止した。

## 7.3 測定する結果が一致するか

応答として測定する変数について、

```text
same construct?
same target?
same unit / measurement meaning?
same temporal scale?
same comparator orientation?
```

を関係の類型ごとに監査した。

特に次の区別を守った。

```text
NDVI != direct T4 open-grassland structure
generic species richness != T2 succession/composition
focal butterfly species != butterfly community
occurrence != target-species population response
non-significance != zero / neutral / safe
```

## 7.4 適用先の条件が一致するか

重み付きの総合類似度は使用しなかった。

代わりに、関係の類型ごとに必要な適用先の条件を、

```text
MANDATORY_MATERIAL
OPTIONAL_DESCRIPTIVE
NOT_MATERIAL_FOR_THIS_RELATION
```

として事前固定した。

必ず確認する条件の例は次である。

```text
vegetation/ecological state
management history
background disturbance
observation window
climate/weather regime
target-species presence
phenology
host-plant context
nectar-resource context
landscape setting
```

必須の条件が不明な場合、類似の値で補わず`INSUFFICIENT_CONTEXT`とした。

## 7.5 適用先となる計画対象地の条件

NAP-001 計画単位にはP3で用いた公開GIS、P4の衛星観測から得た状態等の公開情報から分かる条件が存在する。

しかし、G4で主に測る結果と一致する計画単位ごとの直接的な生態学的応答データは、第1版の研究開始時点で利用可能と確認された証拠として存在しなかった。

したがって、

```text
planning-unit context similarity
!=
planning-unit response validation
```

とした。

## 7.6 Phase 7: 応答を調べる前の適格性監査

外部資料の取得後、その応答を採点する前に、

1. 一次資料の出典と取得履歴
2. 出典の重複と独立性
3. 管理方法の一致
4. 測定結果の定義の一致
5. 必要な地域条件が揃っているか

を評価した。

条件を満たす独立した検証対象になるには、少なくとも、

```text
public primary provenance frozen
management compatibility = PASS
outcome compatibility = PASS
context = IN_DOMAIN
source cluster = independent
```

をすべて満たす必要があった。

## 7.7 Phase 8: 検証対象が0件の場合の規則

第7段階で条件を満たす独立した検証対象が0件だったため、除外した資料の応答を開いて救済するのではなく、結果の確定より前に次の規則を確定した。

```text
if eligible independent held-out context count == 0:
    relation_state = NO_INDEPENDENT_VALIDATION_EVIDENCE
    transfer_authorization = NOT_AUTHORIZED
```

さらに、8類型すべてがこの状態なら、

```text
formalOutcome = INDETERMINATE
```

とした。

---

# 8. 主要結果

## 8.1 Phase 7 証拠の適格性

```text
external candidate sources                  = 6
public-primary sources hash-frozen          = 5
acquisition-incomplete sources              = 1
external source x relation rows             = 12
eligible held-out source x relation rows    = 0
eligible independent held-out clusters      = 0
structurally excluded rows                  = 12
```

## 8.2 構造上の条件による除外の主な理由

第7段階では、管理への応答の良し悪しではなく、応答を調べる前に確認する構造により候補が除外された。

例を挙げると、次のような問題があった。

- 関東の長期的な人工的圧力に関する研究はT2の種組成に関係する測定結果を持つ一方、RF01で必要な背景の管理と管理履歴や必要な地域条件を十分に確認できなかった。
- 刈取りと火入れの比較研究は明示的な管理方法の比較が存在するが、RF01/RF02の管理の継続と停止の比較そのものではなかった。
- 三瓶山の研究は植生の構造を直接測定しており、RF02の結果の定義には適合する可能性があった。しかし、管理内容・背景の管理・必要な地域条件を第1版の規則に照らして十分に確認できなかった。
- 中部日本における管理を続けた場所と放棄した場所の比較では、継続側では火入れ・刈取り・放牧が組み合わされており、単一の管理方法について継続と停止を比べた研究としては扱えなかった。
- Murata/Nohara 2003はA-04/A-05と同じ阿蘇の *Shijimiaeoides* に関する同一研究系列として保守的に扱い、独立した反復検証には数えなかった。
- `G4-EXT-006`は出版社の公式経路で一次資料を再現可能に取得できず、`ACQUISITION_INCOMPLETE`となった。

## 8.3 関係ごとの正式結果

```text
G4-RF-01  NO_INDEPENDENT_VALIDATION_EVIDENCE
G4-RF-02  NO_INDEPENDENT_VALIDATION_EVIDENCE
G4-RF-03  NO_INDEPENDENT_VALIDATION_EVIDENCE
G4-RF-04  NO_INDEPENDENT_VALIDATION_EVIDENCE
G4-RF-05  NO_INDEPENDENT_VALIDATION_EVIDENCE
G4-RF-06  NO_INDEPENDENT_VALIDATION_EVIDENCE
G4-RF-07  NO_INDEPENDENT_VALIDATION_EVIDENCE
G4-RF-08  NO_INDEPENDENT_VALIDATION_EVIDENCE
```

すべての類型で、

```text
transfer authorization = NOT_AUTHORIZED
```

となった。

## 8.4 研究全体の正式結果

```text
formal outcome = INDETERMINATE
formal outcome reason = NO_ELIGIBLE_INDEPENDENT_HELDOUT_RESPONSE_VALIDATION_CONTEXTS
```

これは完了した研究の正式判定であり、未完了の分析ではない。

## 8.5 応答の採点は実施していない

```text
held-out response values read for G4 scoring = false
ecological response concordance computed     = false
excluded-source response rescue              = false
```

したがって、本研究の`INDETERMINATE`は、管理への応答の転用効果の推定値が不確かであることではなく、**応答の転用に関する検証を実行できる条件を満たす独立した証拠が0だったこと**に由来する。

---

# 9. 本研究が支持すること

本研究は、少なくとも次を支持する。

1. source-local responseをplanning contextへ転移するには、management labelの一致だけでは不十分である。
2. management intensity、timing、frequency、duration/history、background management、comparator等を明示的に合わせる必要がある。
3. outcome targetとmeasurement constructも独立に合わせる必要がある。
4. context similarityをweighted scoreへまとめるだけでは、ecological response validationの代替にならない。
5. publication数を独立した再現数へ変換してはいけない。
6. 公開資料の出典、管理方法、測定結果、地域条件、資料の独立性を事前に定めた条件で確認すると、利用できる検証資料が0件になる場合もある。
7. その場合、`TRANSFER_NOT_SUPPORTED`ではなく`NO_INDEPENDENT_VALIDATION_EVIDENCE`として閉じる方が科学的に正確である。
8. `INDETERMINATE`（判定不能）は、事前に定めた規則に従って得られる正式な完了結果にもなり得る。

---

# 10. 本研究が支持しないこと

本研究は次を支持しない。

```text
G4 transfer is supported
G4 transfer is not supported
planning-unit ecological response is known
source-local effect is zero outside source context
unknown response is neutral or safe
context similarity validates ecological response
candidate action is a recommendation
management-review scope is action priority
operational feasibility is ecological desirability
current safety/permission is response evidence
human usability has been validated
practitioner benefit has been demonstrated
Study 2B is complete
transfer_to_zone_contribution=true
zone contribution coefficient is available
formal optimizer input is available
```

特に、

```text
NO_INDEPENDENT_VALIDATION_EVIDENCE
!=
TRANSFER_NOT_SUPPORTED
```

である。

---

# 11. 実務的含意

実務では、外部研究で得られた管理への応答を現地の計画に適用する前に、最低限、次の点を確認する必要がある。

```text
何を管理したのか
どれくらいの強度か
いつ・何回・何年間か
同時に何が管理されていたか
何をresponseとして測ったのか
どの時間scaleで測ったのか
sourceとtargetで何がmaterially違うのか
sourceは本当に独立replicationか
```

これらが不明な場合、数値を補って計画モデルを完成させるのではなく、

```text
transfer not authorized
```

（転用を認めない）と明示する必要がある。

---

# 12. 研究上の限界

## 12.1 第1版の対象資料の限界

本研究の最も大きな限界は、最初に確定した公開資料の範囲では、条件を満たす独立した検証対象を一つも確保できなかったことである。

したがって、管理への応答を別の場所へ適用できるかを、観測された応答に基づいて採点できていない。

## 12.2 慎重な判定規則による判定可能性低下

管理方法・背景・地域条件の規則と重複の扱いは意図的に保守的である。

このため、より緩い研究設計なら比較可能とみなす資料も、本研究では除外され得る。

ただし、この保守性は結果を見て導入したものではなく、証拠に見合わない精度の判断を避けるために事前に設定した。

## 12.3 計画単位で直接確認した応答の不足

阿蘇の計画単位には公開GISや衛星観測から得た情報があるが、主要な生態学的応答と対応する計画単位ごとの直接検証データは、確定済みの公開入力には存在しなかった。

したがって、将来、異なる調査地点間で転用可能性が支持されても、それだけで各計画単位の応答が確定するわけではない。

## 12.4 資料取得上の制約

1件は出版社の公式経路でHTTP 403となり、事前に定めた規則に沿って一次資料を取得できなかった。

非公式な複製で穴埋めしなかったため、利用できる公開証拠の範囲はその分縮小した。

## 12.5 応答の採点による検証は実施していない

条件を満たす検証対象が0件だったため、応答方向の一致、感度分析、負の対照を用いた採点など、応答そのものの検証は実施していない。

実行できない検証を「実施済み」とは扱っていない。

## 12.6 より広い先行研究で第1版の結果を書き換えていない

第7段階の確定後に追加文献が見つかり得ること自体は否定しない。

しかし、条件を満たす資料が0件という結果を見てから資料の範囲を広げると、結果に合わせた後付けの救済になるため、第1版には追加していない。

追加資料を評価する場合は、新たな事前計画に基づく後続研究が必要である。

---

# 13. 第三者資料・データの取扱い

本研究は公開一次資料の識別情報、DOI、出版社の取得経路、ハッシュ値などを再現性情報として管理した。

第三者PDFそのものをリポジトリに再配布することを研究成果の要件とはしていない。

公開報告書にも第三者論文の長文転載、図表転載、個人情報、利用に制限のあるデータは含めていない。

---

# 14. 後続研究との境界

## 14.1 G4 v1は閉鎖済み

G4第1版の対象資料群は閉じている。

```text
G4-RTV-2026-08-14-v1
COMPLETE / FROZEN
formal outcome = INDETERMINATE
```

追加資料をv1へ入れて結果を救済してはいけない。

## 14.2 公開証拠を広げる後続研究

新しい公開一次資料を評価する価値がある場合は、

```text
G4 extension / successor study
```

として、対象資料の範囲、適格性、重複、地域条件に関する規則を応答を見る前に確定する必要がある。

その研究が支持する結果を得ても、G4第1版で確定した結果は変更しない。

## 14.3 Study 2B

NAP-002の研究2Bは引き続き、

```text
Practitioner / Administrative Decision-Support Validation
DEFERRED / NOT STARTED
```

である。

G4 v1の完了は人間を対象とした検証の完了を意味しない。

## 14.4 利用に制限のある地域資料と事前計画による現地の証拠

公開情報から得た証拠だけでは管理履歴や対象地での応答を十分に確認できない場合、利用に制限のある現地の実測データや事前計画に基づく生態学的モニタリングが将来的に必要となる可能性がある。

ただし、それらは独立した新規研究として管理する必要がある。

---

# 15. 再現性・検証

## 15.1 第7段階の確定

```text
passed = true
eligible held-out source x relation rows = 0
eligible independent clusters = 0
held-out response values read = false
```

## 15.2 正式結果の検証

```text
passed = true
errors = []
relation rows validated = 8
formal outcome = INDETERMINATE
```

## 15.3 再現性監査

```text
passed = true
errors = []
recomputed relation states = 8 x NO_INDEPENDENT_VALIDATION_EVIDENCE
recomputed formal outcome = INDETERMINATE
```

## 15.4 誤読を想定した終了時の監査

```text
passed = true
registered adversarial cases = 24
response-scoring adversarial execution performed = false
```

応答を採点する誤読検証の経路を実行しなかったのは、条件を満たす検証対象が0であり、応答を採点する処理自体が科学的に不要・未認可だったためである。

構造上の条件を変えた反実仮想の試験では、

```text
eligibleCount = 0 -> NO_INDEPENDENT_VALIDATION_EVIDENCE
eligibleCount = 1 -> ABORT_ZERO_EVIDENCE_MATERIALIZER
eligibleCount = 2 -> ABORT_ZERO_EVIDENCE_MATERIALIZER
```

となることを確認した。

## 15.5 GitHub Actions

科学的結果を確定したコミットに対する検証実行:

```text
run ID = 31771397548
head   = 1e56878979d3163638768a7b769408a82c4b3629
study-validation job = PASS
external provenance re-acquisition job = PASS
```

成果物:

```text
g4-study-validation
  artifact ID = 9208252017
  digest = sha256:1dea8e5185b622b73e0295ffd9845f2ed060b82de58bc4cd49f272672dbb213c

g4-phase7-external-provenance
  artifact ID = 9208260068
  digest = sha256:ef6c577be3dfc66dd87dd51240d01555c31566d9aab247d5324cf1d7cda414cb
```

---

# 16. 再現性識別子

```text
Study ID:
G4-RTV-2026-08-14-v1

Scientific-state snapshot:
1e56878979d3163638768a7b769408a82c4b3629

Base main snapshot:
2087e6c40108e991d586174b5619ad16dfd9176e

Formal outcome:
INDETERMINATE

Formal outcome reason:
NO_ELIGIBLE_INDEPENDENT_HELDOUT_RESPONSE_VALIDATION_CONTEXTS

Primary relation families:
8

Eligible independent held-out clusters:
0

Formal relation-result SHA-256:
cf9143e376ec4ec7fb01b7b5f4bcf1310b88c5d80c4852a629c9da400a2d64d4

Formal result SHA-256:
2fef26ad26d1edb95cfbca1c2aae3f479072ff155d282f7e7244d5c159c90eac

Formal validation SHA-256:
77323b94aa46c85b3a8751a5b51cd1730fe4c17bb171884a9d4e133676116ae6

Reproducibility audit SHA-256:
1a9a8d8093a1f781ab162f70e30bf56355f976cb3f51a3f21b5b44d66ef11481

Adversarial closure audit SHA-256:
060c1393caf40970285757e894c92c5f37a0a4d7a7dab67aa09407ffe360c925
```

---

# 17. リポジトリ内の主要資料

## 研究計画と事前確定した規則

- `doc/g4/G4_RESPONSE_TRANSFER_VALIDATION_PROSPECTIVE_PROTOCOL.md`
- `doc/g4/G4_PHASE7_EVIDENCE_DISCOVERY_FREEZE.md`
- `doc/checkpoints/2026-08-14-g4-response-transfer-prospective-design-freeze.md`
- `doc/checkpoints/2026-08-14-g4-phase7-acquisition-incomplete-exclusion-rule.md`
- `doc/checkpoints/2026-08-14-g4-phase8-zero-validation-result-rule-freeze.md`

## 第7段階の登録資料

- `analysis/g4/g4_relation_family_registry.csv`
- `analysis/g4/g4_evidence_identity_registry.csv`
- `analysis/g4/g4_source_cluster_registry.csv`
- `analysis/g4/g4_management_compatibility_rules.csv`
- `analysis/g4/g4_outcome_compatibility_rules.csv`
- `analysis/g4/g4_context_dimension_materiality_registry.csv`
- `analysis/g4/g4_target_context_availability.csv`
- `analysis/g4/g4_source_preanalysis_eligibility_registry.csv`
- `analysis/g4/g4_methods_only_audit_registry.csv`
- `analysis/g4/g4_external_evidence_acquisition_manifest.json`
- `analysis/g4/g4_phase7_closure_validation.json`

## 正式結果と監査

- `analysis/g4/g4_phase8_result_rules.json`
- `analysis/g4/g4_formal_relation_results.csv`
- `analysis/g4/g4_formal_result.json`
- `analysis/g4/g4_formal_result_validation.json`
- `analysis/g4/g4_reproducibility_audit.json`
- `analysis/g4/g4_adversarial_closure_audit.json`
- `analysis/g4/g4_study_closure_registry.json`

## 実装

- `analysis/g4/acquire_g4_external_evidence.py`
- `analysis/g4/validate_g4_preanalysis_package.py`
- `analysis/g4/materialize_g4_formal_result.py`
- `analysis/g4/validate_g4_formal_result.py`
- `analysis/g4/audit_g4_formal_closure.py`

## 進捗記録と状態

- `doc/checkpoints/2026-08-14-g4-phase7-preanalysis-closure.md`
- `doc/checkpoints/2026-08-14-g4-response-transfer-formal-closure.md`
- `doc/g4/CURRENT_STATUS.md`

---

# 18. 結論

本研究は、元の調査地点で観察された管理への応答を、別の計画対象地へ適用できる条件を結果を見る前に決めて検証した。しかし、出典の独立性、管理方法、測定結果、必要な地域条件をすべて満たす独立した検証対象は0件だった。したがって、転用が成功したとも失敗したとも判定していない。

最終結果は COMPLETE / FROZEN、正式判定はINDETERMINATE、理由は NO_ELIGIBLE_INDEPENDENT_HELDOUT_RESPONSE_VALIDATION_CONTEXTS である。**比較に必要な条件が満たされないときは、元の調査地点での応答を計画単位での応答と推測せず、判断を止める**という境界を明確にした。

先行研究の transfer_to_zone_contribution=false は変更していない。計画単位ごとの応答、管理の推奨、最適化の入力、人間を対象とした検証も新たに承認していない。

```text
G4-RTV-2026-08-14-v1
COMPLETE / FROZEN
formal outcome = INDETERMINATE
reason = NO_ELIGIBLE_INDEPENDENT_HELDOUT_RESPONSE_VALIDATION_CONTEXTS
```

---

# 用語

**元の調査地点での応答（source-local response）**  
特定の研究・場所・管理条件・測定条件で観察された管理への応答。そのまま計画単位での応答とはみなさない。

**独立した検証対象の条件（held-out context）**  
元の調査地点とは独立して、転用可能性の検証に用いる調査条件。

**条件を満たす独立した検証対象**  
公開一次資料の出典、独立性、管理方法、測定結果、必要な地域条件について、結果を見る前に定めた条件を満たす検証対象。

**NO_INDEPENDENT_VALIDATION_EVIDENCE**  
独立した検証対象がないため、転用の成否を判定できないことを示す、関係の類型ごとの状態。

**INDETERMINATE**  
本研究全体の正式判定。本研究では8類型すべてが `NO_INDEPENDENT_VALIDATION_EVIDENCE`（独立した検証の証拠なし）となったため、判定不能として研究を完了した。

**管理への応答の転用可否（transfer authorization）**  
事前に確定した規則に基づき、元の調査地点で観察された応答を対象とする条件へ転用してよいかを示す状態。本研究の8類型はすべて `NOT_AUTHORIZED`（転用を認めない）である。

---

# 参考文献・関連する先行研究

1. Wenger, S. J., & Olden, J. D. (2012). *Assessing transferability of ecological models: an underappreciated aspect of statistical validation*. Methods in Ecology and Evolution, 3, 260–267. DOI: `10.1111/j.2041-210X.2011.00170.x`.
2. Bareinboim, E., & Pearl, J. (2013). *Meta-Transportability of Causal Effects: A Formal Approach*. Proceedings of the Sixteenth International Conference on Artificial Intelligence and Statistics, PMLR 31, 135–143.
3. Dahabreh, I. J., Robertson, S. E., Steingrimsson, J. A., Stuart, E. A., & Hernán, M. A. (2020). *Extending inferences from a randomized trial to a new target population*. Statistics in Medicine, 39, 1999–2014. DOI: `10.1002/sim.8426`.
4. Dumandan, P. K. T., Simonis, J. L., Yenni, G. M., Ernest, S. K. M., & White, E. P. (2024). *Transferability of ecological forecasting models to novel biotic conditions in a long-term experimental study*. Ecology, 105(11), e4406. DOI: `10.1002/ecy.4406`.

## G4第1版で出典情報を確定した主な外部資料

- Yamamoto et al. DOI: `10.14941/grass.42.307`.
- Yamamoto et al. DOI: `10.14941/grass.53.28`.
- Takahashi et al. DOI: `10.14941/grass.60.102`.
- Chen et al. DOI: `10.14941/grass.51.143`.
- Murata & Nohara. DOI: `10.20848/kontyu.6.2_89`.
- Nakahama et al. DOI: `10.1111/1440-1703.12494` — G4 v1では出版社の公式経路からの取得が未完了であり、検証資料として使用していない。

---

# 引用時の推奨表記

> Natural Area Planning / G4-RTV-2026-08-14-v1 (2026). **公開研究報告書：元の調査地点で得られた管理への応答は別の場所に適用できるか ― 検証条件を先に決めた結果、公開情報だけでは独立した検証対象を確保できなかった ―**. Version 1.0.1, 日本語表現改訂 2026-09-28（科学的結果は2026-08-14確定）。 Formal outcome: INDETERMINATE. Study snapshot: nkkmd/natural-area-planning @ `1e56878979d3163638768a7b769408a82c4b3629`.