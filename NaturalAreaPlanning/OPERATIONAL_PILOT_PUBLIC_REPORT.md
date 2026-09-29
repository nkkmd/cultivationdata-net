# Natural Area Planning / NAP-OP-2026-08-15-v1 — 公開研究報告書

**地域固有・現時点の運用情報を意思決定支援へ正しく接続できるか**  
**― 30事例・192件の必須入力を扱い、不明・未検証の情報を判断を妨げる理由として保持できるかを検証する ―**

- **レポート版:** v1.0.1
- 日本語表現の改訂: **2026-09-28（科学的結果・正式判定は変更なし）**
- **作成日:** 2026-08-15 JST
- **研究ID:** `NAP-OP-2026-08-15-v1`
- **研究状態:** `COMPLETE / FROZEN`
- **正式判定:** `WORKFLOW_VALIDATED_WITHIN_PILOT_SCOPE`
- **研究結果を確定したコミット:** `f1a1f63ed76e960da1355def19bd823027d29aa6`
- **基点となるmainのコミット:** `d3c930293de6fd0126b58233d706075f371c9726`
- **共通の判断時点:** `T0 = 2026-08-15T11:13:35+09:00`
- **本文の性格:** 外部公開用・単体完結型研究レポート
- **編集上の扱い:** 研究結果の確定後に公開用文書を作成した。正式な科学的結果は変更していない

> この文書は、GitHubリポジトリや内部の成果物を参照しなくても、本研究の背景、研究質問、方法、主要結果、限界、再現性、解釈境界を理解できるように構成している。出典と作業履歴の詳細を確認する場合は末尾のリポジトリ内の主要資料を参照されたい。

---


## 初めて読む方へ

この報告書は、許可や安全、現地の状況など、管理の判断に必要な運用情報を扱う手順を検証した研究です。30の試験事例で必要とされた入力192件のうち、実際に使えるものは0件でした。それでも、不明な入力を「安全」「実行可能」「許可済み」と誤読せず判断を止める手順は、事前に定めた試験の範囲で検証されました。管理行為を承認する結果ではありません。

本文の研究ID、正式判定コード、数値、出典識別子は、研究結果と照合できるよう原表記を残しています。

# 要旨

先行研究は、公開証拠の範囲内で管理の検討対象と判断を妨げる要因を示した。しかし、現実に管理を判断するには、その時点、その場所、その候補行動について、許可、安全、現地の状態、気象、資源、管理権限などを別途確認する必要がある。

こうした運用情報を加えるとき、不明なことを「問題なし」と扱ったり、古い情報を現時点でも有効とみなしたり、行政区域内にあることを許可と読み替えたりしてはならない。本研究は、先行研究の結果を変更せず、地域固有・現時点の運用情報を、その出典、権限、対象地域、有効時点を明示して収集し、未確認のまま判断を止める仕組みにつなげられるかを試験した。

結果を見る前に、運用上の10領域、出典と時間に関する規則、30件の試験事例、誤った解釈を想定した25事例、判定条件OP1–OP9を確定した。先行研究の計画単位の形状をハッシュ値で照合し、2026年1月1日時点の行政区域データを重ね合わせた。計画単位0・2・5・8は阿蘇市に、1・3は阿蘇市と産山村の両方に属するものとして扱った。

資料の取得経路と情報の鮮度を判定する規則を確定した後、共通の判断時点を次のとおり固定した。

```text
T0 = 2026-08-15T11:13:35+09:00
```

阿蘇市、産山村、熊本県阿蘇地域振興局、環境省、気象庁などの公式資料を調べた。今回の公開資料のみ・人間参加者なしの試験では、選んだ計画単位と候補行動について、権限、場所の特定、時間的な有効性をすべて満たす運用情報は得られなかった。現地での直接観察もしていない。正式な結果は次のとおりである。

```text
pilot cases                              = 30
operational domains                      = 10
case x domain rows                       = 300
required operational-input rows          = 192
not-required rows                        = 108
usable required inputs                   = 0 / 192
blocked required inputs                  = 192 / 192
operational-workflow-ready cases         = 0 / 30

required availability:
  AVAILABLE                              = 0
  UNKNOWN                                = 156
  UNAVAILABLE                            = 36

required blockers:
  BLOCKED_BY_MISSING_INFORMATION         = 114
  BLOCKED_BY_VERIFICATION                = 42
  BLOCKED_BY_UNAVAILABLE_INFORMATION     = 36
```

必須入力192件のうち使用できたものは0件で、30件の試験事例のいずれも運用上の判断に必要な条件を満たさなかった。ただし、研究が検証したのは、良い条件が見つかるかどうかではない。不明や利用不能という状態を、安全・実行可能・許可済みなどに読み替えず、判断を妨げる要因として正しく次の手順に伝えられるかである。

正式な検証では、データの構造、出典、時間的な有効性、状態の変化、判断を妨げる要因、先行研究との境界、再現性、誤読を想定した25事例について、OP1–OP9がすべて合格した。独立した2回の資料作成結果もバイト単位で一致した。そのため、事前に定めた規則による正式判定は次のとおりである。

```text
WORKFLOW_VALIDATED_WITHIN_PILOT_SCOPE
```

この判定が支持するのは、**30件の試験範囲における情報処理の手順**である。管理行為の実行可能性、許可、安全性、生態学的な望ましさ、管理への応答、推奨、順位、人にとっての使いやすさは示していない。G4の判定不能という先行結果と、人間参加者による検証が未着手であることも変わらない。

---

# 1. 研究の背景

## 1.1 Natural Area Planningで既に解決したこと

Natural Area Planningでは、公開情報に基づく計画研究を、証拠が示す範囲を超えて進めないことを基本原則としている。

NAP-001のステージCでは公開情報から得られる計画上の証拠を整理したが、計画単位ごとの管理への応答モデルや最適化係数の作成は承認しなかった。

NAP-002の研究1では、その証拠の限界を守りながら、

```text
WHERE      どこを確認対象として見るか
WHY        何が判断を止めているか
WHAT NEXT  次に何の情報が必要か
```

を示す意思決定支援の手順に変換した。

NAP-002の研究2Aでは、人間参加者を用いずに、出典の追跡可能性、証拠の限界の表示、基準との同等性、誤読への耐性、公開文書との整合性を事前に検証した。ただし正式判定は`INDETERMINATE`であり、実際の利用者による使いやすさは検証していない。

G4研究の第1版では、元の調査地点での管理への応答を別の場所に適用できる条件を事前に定めて検証したが、条件を満たす独立した検証対象が0件だったため`INDETERMINATE`で閉じた。

## 1.2 それでも実際の判断に不足するもの

これらの研究が揃っても、実際の候補行為を検討する時点では、過去の記録や生態学的な証拠とは別に、次のような運用上の情報が必要になる。

```text
候補行為の具体的な実施仕様
現地へのアクセス可否
必要インフラの存在・利用可否
誰が管理・許可・実施権限を持つか
人員・機材・予算などの資源
現在の現地状態
現在の気象条件
現在の燃料・バイオマス状態
現在の安全体制
現在の許可・規制
```

これらは「現時点で何が実行可能か」を考えるための情報であり、管理への生態学的応答の証拠とは異なる。

## 1.3 運用上の事実を足すだけでは危険な理由

運用情報は古くなる、取得できない、対象地域の範囲が粗い、管轄が重複する、出典の権限が異なる、といった特徴を持つ。

そのため、単に「検索して見つかった値」を手順へ追加すると、次の誤りが起こり得る。

```text
UNKNOWN -> 問題なし
UNAVAILABLE -> 制約なし
古い公式情報 -> CURRENT
資料の取得時刻 -> 情報が表す時刻
市町村内に位置する -> 市町村が管理者
一般的な許可制度 -> 個別ケースが許可済み
一般的な野焼き日程 -> 選定した計画単位の実施仕様
最寄りの気象観測所の値 -> 計画単位そのものの気象
現在の安全体制 -> 生態学的に安全
運用上の実行可能性 -> 生態学的な望ましさ
```

本研究は、この誤変換を防ぎつつ地域固有・現時点の情報を手順に接続できるかを独立に検証した。

---

# 2. 研究対象

本研究は、**地域固有・現時点の運用情報を扱う意思決定支援の手順**を対象とする。

正式な評価単位は次の三つの組合せとした。

```text
planning_unit_id
× candidate_action_id
× decision_time_snapshot
```

今回の主な試験範囲には、6つの計画単位と代表的な候補行為5種類を用いた。

計画単位:

```text
[0, 1, 2, 3, 5, 8]
```

代表的な候補行為:

```text
CR_BURN_ONLY
CR_MOW_JULY
CR_BURN_GRAZE_INTENSITY_UNRESOLVED
CR_GRAZE_WITHOUT_BURN_INTENSITY_UNRESOLVED
CR_ACTIVE_MANAGEMENT_UNRESOLVED
```

これらは検討の候補であり、推奨や優先順位を表さない。

本研究の主な対象ではないものは次のとおりである。

```text
生態学的な応答の検証
管理の有効性
生物多様性への便益
管理行為の推奨
行為の順位付け・優先順位付け
最適化計算の実行
人にとっての使いやすさ
実務者による受け入れ
人間参加者を対象とする研究
```

---

# 3. 研究目的と中心的研究質問

研究目的は結果を見る前に次のように定めた。

> 実際に判断する時点で、計画単位と候補行為ごとに必要な地域固有・現時点の運用情報を、出典、権限、対象地域、情報が表す時点、有効期限を明示して取得・分類できるか。また、不明・利用不能・未検証・古い情報を都合よく補わず、既存の意思決定支援の手順に再現可能な形で接続できるか。

正式判定の区分は、少なくとも次を区別する設計とした。

```text
WORKFLOW_VALIDATED_WITHIN_PILOT_SCOPE
WORKFLOW_NOT_VALIDATED
INDETERMINATE
```

重要なのは、`WORKFLOW_VALIDATED_WITHIN_PILOT_SCOPE`が「候補行為が実行可能だった」を意味しないことである。

---

# 4. 先行研究・新規性を主張できる範囲

出典の追跡可能性、時間的な有効性、不確実性の扱い、構造化された意思決定、順応的管理、運用上の準備状況、状況認識などは既存の方法論・実務概念である。

たとえばW3C PROVは、実体・活動・行為者の関係を用いて出典と作業履歴を表現する標準的枠組みを提供する。OGC Observations, Measurements and Samplesは観測の対象時点・結果の公表時点・観測対象などを区別する。ISO 19157-1は地理空間データの品質の一般原則を扱う。USGSのstructured decision making / adaptive managementの文献も、不確実性を明示しながら意思決定の過程を構成する一般的枠組みを提供している。

したがって、本研究はこれらの一般概念自体を新規発明として主張しない。

本研究で対象固有に実装・検証したのは、Natural Area Planningの既存の証拠の限界を守る意思決定支援の手順に対し、

```text
地域固有・現時点の運用情報
× 出典の権限と来歴
× 地理的な対象範囲
× 時間的な有効性と期限
× UNKNOWN / UNAVAILABLE / NOT_VERIFIED を明示的に区別する状態
× 判断を妨げる理由の定義
× 先行研究・生態学的な結果との境界
```

を一体化し、「値を取得できない場合でも誤った推論をせずに手順を終了できるか」を正式な試験として検証した点である。

---

# 5. 使用した情報 / 使用しなかった情報

## 5.1 使用した先行研究の確定済み入力

試験事例と必須入力の定義には、NAP-002の研究1で確定した成果物を先行研究の入力として参照した。

これらは再解析して確定済みの結果を変更するためではなく、

```text
先行研究で確定した意思決定支援の状態
-> 今回の事前計画に基づく運用試験の入力
```

として用いた。

## 5.2 計画単位の形状の正確な照合

場所に応じた情報収集の前に、先行研究の計画単位の形状を同一データから正確に再取得した。

```text
file = p001_p4_aso_pastures_193.geojson
byte size = 1,619,871
SHA-256 = 46ef4dd475ec7645d78130722e8ddfcae9f51c6244ce95dc22ea9f7dcaa6609d
features = 193
ID field = pu_id
```

ファイルのハッシュ値が先行研究で確定した値と一致することを確認してからデータの構造を確認した。

## 5.3 行政区域のデータ

市町村の管轄を推測で割り当てないため、国土交通省「国土数値情報（行政区域）」の2026年1月1日時点・熊本県公開データを用いた。

```text
file = N03-20260101_43_GML.zip
byte size = 9,780,499
SHA-256 = e38cdc6102af404f05c2bac5f5219858c3c1d401fb9ff0acf410edd70ae88bd0
snapshot date = 2026-01-01
```

## 5.4 正式に使用する資料の取得経路

T0以降の正式な情報収集では、主に次の公式な資料の取得経路を使用した。

```text
阿蘇市 経済部 農政課
阿蘇市 土木部 建設課
阿蘇市 総務部 危機管理防災課
阿蘇市 土木部 住環境課
阿蘇市 農業委員会事務局
産山村 経済建設課
産山村 農業委員会
熊本県 阿蘇地域振興局 農林部
熊本県 阿蘇地域振興局 土木部
環境省 阿蘇くじゅう国立公園管理事務所
気象庁 地域気象観測システム（アメダス）
```

## 5.5 使用しなかった情報

本研究の第1版では次を使用していない。

```text
人間参加者のデータ
実務者への面接・調査
利用を承認されていない地域の記録
牧野管理者の非公開記録
事前に定めた手順に沿った現地観察
結果を見てからの有利な資料への差し替え
T0前に偶然見えた運用情報の値
```

T0前の資料調査では、検索結果の抜粋に運用日程や現地の状態、気象の値が見えたが、すべて`QUARANTINED_NOT_FORMAL_DATA`として正式な情報収集から除外し、T0後に同じ資料を使う場合も改めて取得することとした。

---

# 6. 結果を見る前に確定した研究規則

結果を見る前に、次を確定した。

```text
study identity
scientific question
scope / non-scope
pilot population
operational unit
10 operational domains
source provenance rule
source authority ceiling
geographic-scope rule
retrieval/effective/phenomenon-time distinction
freshness / expiry rule
state vocabulary
blocker semantics
pilot case frame
workflow output
success / failure criteria
25 adversarial cases
reproducibility firewall
historical/ecological firewall
```

特に、次の状態を別々に保持した。

```text
availability
verification
temporal validity
workflow use
blocker
```

単一の「可／不可」にまとめないことで、`UNKNOWN`と`UNAVAILABLE`、`NOT_VERIFIED`、`STALE`等を区別できるようにした。

---

# 7. 運用情報の領域

運用情報を扱う10領域は次のとおりである。

| 領域の判定コード | 確認する内容 |
|---|---|
| `LOCAL_ACTION_SPECIFICATION` | 候補行為の具体的な実施仕様 |
| `LOCAL_ACCESS_FEASIBILITY` | 現地への到達経路と道路の状態 |
| `LOCAL_INFRASTRUCTURE_FEASIBILITY` | 必要な設備・施設・インフラ |
| `LOCAL_AUTHORITY_FEASIBILITY` | 土地・管理・行為についての権限 |
| `LOCAL_RESOURCE_CAPACITY` | 人員・機材・予算などの資源 |
| `CURRENT_SITE_CONDITION` | 判断時点に近い現地の状態 |
| `CURRENT_WEATHER_CONDITION` | 判断時・実施時の気象 |
| `CURRENT_FUEL_OR_BIOMASS_CONDITION` | 燃料・バイオマス状態 |
| `CURRENT_SAFETY_ARRANGEMENT` | 候補行為に応じた安全体制 |
| `CURRENT_PERMISSION_OR_RESTRICTION` | 現在の許可・規制・制約 |

これらはすべて運用情報の領域であり、管理への生態学的な応答を示すものではない。

---

# 8. 計画単位の形状と管轄の固定

## 8.1 なぜ行政区域を重ね合わせた確認が必要だったか

計画単位の中心点だけで自治体を割り当てると、行政界をまたぐ部分が見落とされる。許可、道路の管理権限、条例などを確認する際には、面積が小さい側の自治体も重要になり得る。

そこで、計画単位の正確な形状と国土交通省の行政区域データを重ね合わせ、**面積のある重なりをすべて保持**した。

## 8.2 結果

```text
PU 0: 阿蘇市                       100%
PU 1: 阿蘇市 99.1456% + 産山村 0.8544%
PU 2: 阿蘇市                       100%
PU 3: 阿蘇市 99.4090% + 産山村 0.5910%
PU 5: 阿蘇市                       100%
PU 8: 阿蘇市                       100%
```

したがって、

```text
single-municipality units = [0,2,5,8]
multi-municipality units  = [1,3]
```

と固定した。

ここから導けるのは「市町村地理範囲が重なる」という事実だけである。

```text
municipal containment
!= land ownership
!= pasture management authority
!= permission
```

---

# 9. 出典と権限の確認規則

正式な運用情報として使う資料には、可能な限り次を要求した。

```text
source identity
source URI / identifier
source class
access level
authority status
issuing / owning authority
retrieval timestamp
effective / phenomenon timestamp
result / publication timestamp
validity start
validity end / expiry condition
geographic scope
verification state
snapshot / hash method
normalization provenance
```

資料を判断に使えるかどうかは、秘密性ではなく、**その運用情報についての権限と対象範囲**で決まる。

したがって、

```text
restricted source
!= intrinsically stronger scientific evidence
```

とした。

元が同じ資料の複製は独立した確認に数えない。同等の権限を持つ資料が矛盾し、事前に定めた優先規則でも解決できなければ`CONFLICTING_SOURCES`とし、都合の良い資料を選択しない。

---

# 10. 時間的な有効性の確認規則

地域固有・現時点の情報では、「いつ取得したか」と「いつの状態を表すか」を分離した。

```text
retrieval time
!= effective / phenomenon time
!= result / publication time
```

資料を取得した時刻を、その情報が表す時刻の代わりにはしなかった。

また、全領域に一律の有効期限を後付けせず、資料が明示する有効期間を優先した。必要な領域だけに、結果を見る前に情報の鮮度の条件を定めた。

例:

```text
current site direct observation        <= 6 h before T0
current weather observation            <= 1 h before T0
fuel moisture / combustibility         <= 3 h before T0
standing biomass / height / cover      <= 24 h before T0
infrastructure direct observation      <= 24 h before T0
```

資料に記された有効期間がある場合はそれを優先した。有効期間を確認できない場合は`VALIDITY_UNKNOWN`とし、最後に分かっていた値を自動的に現時点でも有効とみなさない。

---

# 11. 共通の判断時点T0

資料の取得経路と情報の鮮度に関する規則が継続的な検証に合格し、実施前に残る唯一の障害が`COMMON_T0_NOT_FROZEN`になったことを確認してから、

```text
T0 = 2026-08-15T11:13:35+09:00
```

を固定した。

T0確定後の実施前検証は、

```text
designPackagePassed = true
pilotExecutionAuthorized = true
localCurrentDataAcquisitionAuthorized = true
executionBlockers = []
```

となり、その後に初めて正式な情報収集を開始した。

---

# 12. 正式な情報収集

正式な情報収集では、T0前に偶然見えた値を再利用せず、事前に定めた取得経路からT0後に改めて取得した。

しかし、公式ページが存在しても、選んだ計画単位と候補行為に直接使える運用情報が得られるとは限らない。

代表例は次のとおりである。

## 12.1 一斉野焼き情報

阿蘇市の公式のお知らせは地域の野焼き実施に関する重要な行政情報であるが、牧野組合ごとに実施時刻等が異なり、選んだ計画単位と候補行為の実施内容、管理者、許可、安全体制を直接確定するものではなかった。

したがって、一般的な情報を個別の試験事例に当てはめなかった。

## 12.2 道路と現地へのアクセス

阿蘇市・熊本県には公式な道路情報の取得経路がある。しかし計画単位の形状だけでは、各地点への実際の進入路とその管理権限を、結果を見る前に確定できなかった。

したがって、近隣の道路が通行可能に見えることを`LOCAL_ACCESS_FEASIBILITY=AVAILABLE`へ変換しなかった。

## 12.3 許可

阿蘇市には許可や相談の窓口があり、産山村には火入れに関する条例がある。しかし、一般的な制度・条例が存在することは選んだ計画単位と候補行為が許可済みであることを意味しない。

産山村の火入れ制度では、火入地、地図、所有者・管理者の承諾等、個別案件に結び付く情報が必要になる。今回の正式な情報収集では、個別の事例に対応する許可記録や確認済みの土地・管理者情報を取得していない。

したがって、

```text
public no-record
!= approval
!= confirmed absence of restriction
```

を維持した。

## 12.4 国立公園の規制が適用されるか

環境省の公式資料は確認したが、公開された区域図だけでは、最近の拡張部分を含む正確な境界を判断できないという制約があり、各計画単位への自然公園法の適用を地図の見た目から推定しなかった。

## 12.5 気象

気象庁のアメダスは公式の一次観測資料である。しかし観測所の値を各計画単位の気象として使うには、その場所を代表できる根拠を事前に定める必要がある。

今回、観測値を見てからその根拠を追加せず、観測所の値を選んだ計画単位の気象値とはみなさなかった。

## 12.6 現地での直接観察

研究計画に沿った現地での直接観察は実施しなかった。

したがって、現時点の現地状態、燃料・バイオマスの状態、施設などについて、観察していない値を推測で補わなかった。

---

# 13. 主要結果

## 13.1 正式な評価対象

```text
planning units                    = 6
representative actions            = 5
pilot cases                       = 30
operational domains               = 10
case x domain rows                = 300
required rows                     = 192
not-required rows                 = 108
```

## 13.2 必須入力を利用できるか

```text
AVAILABLE                         = 0
UNKNOWN                           = 156
UNAVAILABLE                       = 36
```

## 13.3 判断を妨げる要因の分布

```text
BLOCKED_BY_MISSING_INFORMATION     = 114
BLOCKED_BY_VERIFICATION            = 42
BLOCKED_BY_UNAVAILABLE_INFORMATION = 36
```

## 13.4 手順上の準備状況

```text
usable required inputs             = 0 / 192
blocked required inputs            = 192 / 192
operational-workflow-ready cases   = 0 / 30
```

## 13.5 正式な判定条件

```text
OP1_SCHEMA_COMPLETENESS                 PASS
OP2_PROVENANCE_INTEGRITY               PASS
OP3_TEMPORAL_VALIDITY_INTEGRITY        PASS
OP4_STATE_TRANSITION_INTEGRITY         PASS
OP5_BLOCKER_SEMANTICS_INTEGRITY        PASS
OP6_WORKFLOW_CONNECTION_INTEGRITY      PASS
OP7_HISTORICAL_AND_ECOLOGICAL_FIREWALL PASS
OP8_REPRODUCIBILITY                     PASS
OP9_ADVERSARIAL_CONSISTENCY            PASS
```

誤読を想定した25事例すべてを評価し、事前に定めた期待結果と一致した。

## 13.6 正式判定

以上により、正式判定は、

```text
WORKFLOW_VALIDATED_WITHIN_PILOT_SCOPE
```

となった。

---

# 14. なぜ「使用可能な情報0件」でも手順の検証は合格なのか

この点は本研究で最も誤解されやすい。

もし研究の判定対象が、

> 30事例のうち何件を実行できるか

であれば、準備が整った事例が0件という結果には別の意味がある。

しかし本研究の判定対象は、

> 運用情報を事前に定めた証拠の規則で扱い、取得不能・未検証・古い情報を「安全」「実行可能」「許可済み」に読み替えず、判断を妨げる理由として手順へ接続できるか

である。

したがって、情報不足の多い環境では、正しい手順は多数の`UNKNOWN`や`UNAVAILABLE`を返す可能性がある。

実際、今回の結果は、

```text
UNKNOWN / UNAVAILABLEを埋めなかった
-> required inputsはすべてblockされた
-> 0 casesがreadyになった
-> それでもschema/provenance/time/state/blocker/firewall/reproducibilityはすべてPASSした
```

というものである。

これは「管理可能性が高い」という結果ではなく、**不足する情報を不足するまま表現できた**という手順の検証結果である。

---

# 15. 本研究が支持すること

本研究は、事前に定めた試験の範囲で、次を支持する。

1. 地域固有・現時点の運用情報を、生態学的な証拠とは分けて扱える。
2. 出典、権限、対象地域、時間的な有効性を正式な手順に組み込める。
3. 計画単位が行政界をまたぐ場合、面積の小さい側の自治体も記録できる。
4. `UNKNOWN`、`UNAVAILABLE`、`NOT_VERIFIED`、`VALIDITY_UNKNOWN`を補完せず保持できる。
5. 必須入力が利用できなければ、判断を妨げる理由として一定の規則で示せる。
6. 判断を妨げる理由を、候補行為に必要な入力と結び付けられる。
7. 不利な結果や欠測でも、先行研究の結果と生態学的証拠の限界を守れる。
8. 同じ確定済み入力から正式な結果を再現できる。
9. 誤った推論を誘う25事例でも判断を止められる。

---

# 16. 本研究が支持しないこと

本研究は次を支持しない。

```text
どのcandidate actionが実行可能か
どのcandidate actionが安全か
どのcandidate actionが許可されているか
どのcandidate actionを選ぶべきか
candidate actionのranking / priority
management recommendation
planning-unit ecological response
management effectiveness
biodiversity benefit
ecological desirability
optimizer coefficient
human usability
practitioner acceptance
public-document compatibilityのhuman benefitへの転換
```

特に、

```text
operational feasibility
!= ecological desirability

current safety / permission
!= management-response evidence

local/current facts
!= ecological response evidence
```

である。

---

# 17. 先行研究との関係

本研究は先行研究の結果を変更しない。

結果の確定時点でも次の状態に変わりはない。

```text
NAP-001 public-only Stage C  COMPLETE / FROZEN
NAP-002 Study 1             COMPLETE / FROZEN
NAP-002 Study 2A            COMPLETE / FROZEN / INDETERMINATE
NAP-002 Study 2B            DEFERRED / NOT STARTED
G4 Response-Transfer v1     COMPLETE / FROZEN / INDETERMINATE
human validation            NOT PERFORMED
```

G4については、

```text
NO_INDEPENDENT_VALIDATION_EVIDENCE
!= TRANSFER_NOT_SUPPORTED
```

を維持する。

本研究で運用情報を扱う手順が検証に合格しても、G4の管理への応答の転用可能性を支持・否定したことにはならない。

先行研究の設定:

```text
transfer_to_zone_contribution = false
```

も変更していない。

---

# 18. 実務的含意

## 18.1 「情報が足りない」を正式な出力にできる

実務支援の仕組みでは、「値がない」ことをエラーとして捨てると、人間が空欄を都合よく解釈する余地が生まれる。

本研究では、不足・利用不能・未検証を明示的な状態と、判断を妨げる理由にした。

たとえば、

```text
必要なpermission recordが見つからない
```

場合、出力は「許可なし」でも「許可済み」でもなく、

```text
UNKNOWN
BLOCKED_BY_MISSING_INFORMATION
```

となる。

## 18.2 運用上の準備が整ったと急いで判断しない

今回、準備が整った事例が30件中0件だったことは、公開資料だけでは個別の事例に必要な現地の運用情報が不足したという観察結果であるである。

実際の計画へ進むには、今後、適法に利用できる現地の管理記録、土地・管理者の情報、実際の進入路、行為に応じた安全計画、許可、研究計画に沿った現地観察等が必要になり得る。

ただし、それらを追加する場合は本研究の第1版を後から書き換えず、別の後続研究として扱う必要がある。

---

# 19. 研究上の限界

## 19.1 公開資料だけで到達できる限界

今回の正式な情報収集は公式の公開資料を中心とした。現地の管理者の記録、非公開の運用計画、利用に制限のある資料などは使用していない。

したがって、「必要情報が存在しない」と結論したのではなく、**今回確定した情報収集の範囲では正式に利用できる情報を得られなかった**と解釈すべきである。

## 19.2 現地での直接観察未実施

現地の状態、燃料・バイオマス、施設などについて現地観察を実施していない。

このため`UNAVAILABLE`が多く発生した。

## 19.3 実在する人による検証未実施

実際の実務者や行政の判断担当者にとって、この手順が分かりやすく、実務で使え、役立つかは検証していない。

```text
workflow validation
!= human usability validation
```

である。

## 19.4 特定時点の記録

正式な判断時点は2026-08-15 11:13:35 JSTである。運用情報は時間とともに変化するため、別の日には結果が異なり得る。

本研究の正式判定を、別の日に得た情報でさかのぼって更新してはならない。

## 19.5 試験の対象範囲の限定

対象は6つの計画単位と代表的な候補行為5種類を組み合わせた30事例である。

他の計画単位、地域、管理体制にも成り立つかは別途検証が必要である。

## 19.6 資料の取得経路を網羅できたか

資料の取得経路は結果を見る前に確定したが、すべての権限者、管理者、非公開の運用記録まで調べたわけではない。

## 19.7 生態学的な検証ではない

本研究の肯定的な正式判定は、運用情報を扱う手順に限られ、生態学的な結果を評価したものではない。

よって、管理への応答、種・生息地・景観への効果などを導くことはできない。

---

# 20. 第三者資料・データの取扱い

本研究では、行政機関が公開する資料や第三者の地理空間データ、公式ウェブ資料を出典として参照した。

計画単位の元データと国土交通省の公開データはハッシュ値を記録したが、公開報告書の本文には第三者データの全文を再配布しない。

正式な出典監査では、必要な資料の識別情報、URI、対象範囲、判断に使える範囲を記録し、公式ページの全文複製は行わない。

個人情報、人間参加者のデータや牧野の管理者の非公開記録は含まれていない。

---

# 21. 実装上の問題

最初の正式な継続的検証 `31858950145`では、Pythonの実行処理にJSONの真偽値 `false`を用いた実装ミスがあり、正式な結果の作成が完了する前に停止した。また結果を作る処理に`pipefail`がなく、エラー発生時の即時停止が不足していた。

この実行では正式な科学的結果を作成していない。

修正は、

```text
false -> False
provenance validatorのfield参照を既存凍結keyへ整合
materialization pipelineへpipefail追加
```

に限定した。

試験事例の範囲、資料の取得経路、情報の鮮度に関する規則、T0、状態の定義、判定条件、正式判定の規則、解釈上の境界は変更していない。

修正後の正式な実行 `31858992089` で、すべての判定条件を評価した。

---

# 22. 再現性・検証

正式な検証の成功記録:

```text
GitHub Actions run ID = 31858992089
job ID = 94948791967
conclusion = success
artifact ID = 9239914641
artifact ZIP SHA-256 = d42993da91032d9c320f738192c4e751d5fd605ca9042060c1726c53e3387c25
```

正式な処理を独立に2回実行し、OP8で出力がバイト単位で一致することを確認した。

主要な出力の識別情報:

```text
operational_input_snapshot.csv
SHA-256 = d490ae1d2625729ef7602d91aba8b4054140aa302ebf9fb917081a47bffb7338
bytes = 110,672

operational_blocker_matrix.csv
SHA-256 = fc3a445f415437121c983878a89f176418540bb434775e0a1d3dbfa93f83577f
bytes = 4,531

operational_formal_summary.json
SHA-256 = 9129ffc1134eb4d9c44aab40b330665d53c6c0d163dc599560ab42beb75d531f
bytes = 901

operational_formal_manifest.json
SHA-256 = 925957ceeabb481ecc3dc5d236a67d42a35377d238a81b1cbb650f400f7ca73a
bytes = 591

operational_pilot_formal_validation.json
SHA-256 = 10d2557e0d653b5a84fc2f9efdbe426d53398917e4f2a67cbe5740f9644d56b7
bytes = 1,276
```

---

# 23. 再現性識別子

```text
Study ID:
NAP-OP-2026-08-15-v1

Formal run ID:
NAP-OP-FORMAL-2026-08-15-v1

Scientific-state snapshot:
f1a1f63ed76e960da1355def19bd823027d29aa6

Base main snapshot:
d3c930293de6fd0126b58233d706075f371c9726

T0:
2026-08-15T11:13:35+09:00

Historical M1 geometry:
46ef4dd475ec7645d78130722e8ddfcae9f51c6244ce95dc22ea9f7dcaa6609d

MLIT administrative archive:
e38cdc6102af404f05c2bac5f5219858c3c1d401fb9ff0acf410edd70ae88bd0

Formal cases:
30

Required operational inputs:
192

Usable required inputs:
0

Operational-workflow-ready cases:
0

Adversarial cases:
25

Formal outcome:
WORKFLOW_VALIDATED_WITHIN_PILOT_SCOPE
```

---

# 24. リポジトリ内の主要資料

## 研究計画と事前に定めた方法

```text
doc/operational-pilot/OPERATIONAL_PILOT_PROSPECTIVE_PROTOCOL.md
analysis/operational-pilot/operational_pilot_design_registry.json
analysis/operational-pilot/operational_input_taxonomy.json
analysis/operational-pilot/operational_state_vocabulary.json
analysis/operational-pilot/operational_source_provenance_rules.json
analysis/operational-pilot/operational_temporal_validity_rules.json
analysis/operational-pilot/operational_adversarial_expected_cases.csv
```

## 試験の対象と空間情報との対応

```text
analysis/operational-pilot/operational_pilot_case_registry.csv
analysis/operational-pilot/operational_pilot_case_geometry_manifest.json
analysis/operational-pilot/operational_pilot_case_geometry_rehydration_verification.json
analysis/operational-pilot/operational_case_jurisdiction_overlay.json
```

## 出典と判定時点の確定

```text
analysis/operational-pilot/operational_source_acquisition_plan.csv
analysis/operational-pilot/operational_case_source_freshness_registry.json
analysis/operational-pilot/operational_t0_registry.json
analysis/operational-pilot/operational_preexecution_incidental_exposure_audit.json
```

## 正式な情報収集と実施

```text
analysis/operational-pilot/operational_formal_source_acquisition_audit.json
analysis/operational-pilot/run_operational_pilot_formal.py
analysis/operational-pilot/validate_operational_pilot_formal.py
analysis/operational-pilot/operational_formal_summary.json
analysis/operational-pilot/operational_formal_manifest.json
analysis/operational-pilot/operational_pilot_formal_validation.json
analysis/operational-pilot/operational_pilot_formal_result.json
```

## 進捗記録

```text
doc/checkpoints/2026-08-15-operational-pilot-prospective-design-freeze.md
doc/checkpoints/2026-08-15-operational-pilot-geometry-rehydration-closure.md
doc/checkpoints/2026-08-15-operational-pilot-jurisdiction-overlay-freeze.md
doc/checkpoints/2026-08-15-operational-pilot-formal-closure.md
```

---

# 25. 後続研究との境界

本研究の第1版は正式な結果を確定している。地域の追加記録、直接観察、人間を対象とする調査、生態学的な検証を後から組み込んで、この結果を書き換えない。

将来の候補は、独立した後続研究として、たとえば次を扱い得る。

```text
利用を承認された地域の運用記録を含む検証
事前に定めた現地観察を含む運用情報の検証
実際の牧野管理者と土地の権限者を結び付ける調査
実務者を対象とした使いやすさの検証
新しい独立した地点での管理への応答の転用検証
```

ただし、いずれも本研究の正式判定をさかのぼって書き換えない。

NAP-002 Study 2Bは本研究とは独立に、

```text
DEFERRED / NOT STARTED
```

のままである。

---

# 26. 結論

本研究は、地域固有・現時点の運用情報を、出典、権限、対象地域、時間的な有効性、不確実性を保ったまま意思決定支援につなげられるか検証した。事前に定めた30事例では、必須入力192件のうち使えた情報は0件で、すべての事例で運用上の判断が止まった。

手順は不明な入力156件と利用不能な入力36件をそのまま保持した。判断を妨げる要因として、情報不足114件、確認待ち42件、情報を利用できないもの36件に分類した。誤読を想定した25事例を含む判定条件OP1–OP9はすべて合格し、別々に作成した結果も一致した。正式判定は WORKFLOW_VALIDATED_WITHIN_PILOT_SCOPE である。

これは管理行為を実行できるという判定ではない。**情報不足を安全・許可済み・実行可能・生態学的に望ましいと読み替えず、判断を止める理由として再現可能に示せた**という、試験範囲に限った結果である。

```text
WORKFLOW_VALIDATED_WITHIN_PILOT_SCOPE
```

---

# 用語

**運用上の情報（operational fact）**  
現地で候補行為を検討・実施するときに必要な、地域固有・現時点の実務条件。生態学的な応答の証拠とは区別する。

**T0**  
試験全体に共通する判断時点。本研究では`2026-08-15T11:13:35+09:00`。

**UNKNOWN**  
必要な情報の真偽や状態を判定できないこと。「問題なし」「安全」「実行可能」を意味しない。

**UNAVAILABLE**  
事前に定めた規則に沿った取得・観測ができないか、今回の調査範囲に利用できる情報がない状態。制約がないことを意味しない。

**NOT_VERIFIED**  
出典の権限、対象範囲、識別情報などを事前の規則で確認できていない状態。

**VALIDITY_UNKNOWN**  
情報が表す時点や有効期限を確定できず、現時点で有効な情報として使えない状態。

**判断を妨げる理由（blocker）**  
必須入力を意思決定支援に使えない理由を示す状態。推奨や優先順位の点数ではない。

**WORKFLOW_VALIDATED_WITHIN_PILOT_SCOPE**  
事前に定めた試験の範囲でOP1–OP9を満たし、運用情報の表示、出典、時点、判断を妨げる理由、先行研究との境界、再現性を検証できた状態。候補行為の実行可能性や生態学的な望ましさは示さない。

---

# 参考文献・関連する先行研究

- World Wide Web Consortium (W3C). *PROV-O: The PROV Ontology*. W3C Recommendation.
- Open Geospatial Consortium (OGC). *OGC Abstract Specification Topic 20: Observations, Measurements and Samples*.
- ISO. *ISO 19157-1:2023 Geographic information — Data quality — Part 1: General requirements*.
- Runge, M.C. & Bean, E. (2020). *Decision Analysis for Natural Resource Management*. U.S. Geological Survey.
- Williams, B.K., Szaro, R.C., & Shapiro, C.D. (2009). *Adaptive Management: The U.S. Department of the Interior Technical Guide*. U.S. Department of the Interior.
- 国土交通省. 国土数値情報「行政区域」2026年版・熊本県.
- 阿蘇市、産山村、熊本県、環境省、気象庁の公式な運用・行政情報の取得経路。個々の資料の識別情報と、正式な判断に使える範囲は、リポジトリ内の出典監査を参照。

---

# 引用時の推奨表記

```text
Natural Area Planning / NAP-OP-2026-08-15-v1 (2026).
公開研究報告書：地域固有・現時点の運用情報を意思決定支援へ正しく接続できるか
― 30事例・192件の必須入力を扱い、不明・未検証の情報を判断を妨げる理由として保持できるかを検証する ―.
Version 1.0.1, 日本語表現改訂 2026-09-28（科学的結果は2026-08-15確定）。
Formal outcome: WORKFLOW_VALIDATED_WITHIN_PILOT_SCOPE.
Study snapshot: nkkmd/natural-area-planning @ f1a1f63ed76e960da1355def19bd823027d29aa6.
```