# Natural Area Planning / NAP-POERT-2026-08-24-v1 — 公開研究報告書

**公開オンライン情報による生態学的な管理効果の転用可能性と地域の証拠の検証**  
**― 独立した応答の証拠、阿蘇の植生情報、他地域への適用条件を分けて評価する ―**

- レポート版: **v1.0.1**
- 日本語表現の改訂: **2026-09-28（科学的結果・正式判定は変更なし）**
- 作成日: **2026-08-25 JST**
- 研究ID: `NAP-POERT-2026-08-24-v1`
- 研究状態: **COMPLETE / FROZEN**
- 応答の転用に関する正式判定: **INDETERMINATE**
- 地域への適用可能性に関する正式判定: **PARTIALLY_SUPPORTED**
- 研究全体の正式判定: **INDETERMINATE**
- 科学的結果を確定した時点: `nkkmd/natural-area-planning @ dc1633205b84e6bf9409c9fb360278bee9cb840b`
- 本文の性格: **単体公開用研究レポート**

この文書は、GitHubリポジトリや内部の成果物を参照しなくても、本研究の背景、研究質問、事前に確定した研究計画、使用した公開情報、主要結果、限界、再現性、解釈境界、および今後の研究課題を理解できるように構成している。

## 初めて読む方へ

この報告書は、一般公開されたオンライン資料から、管理への応答を別の場所に適用するための独立した証拠と、阿蘇の地域に結び付く生態学的な証拠を探した研究です。地域の植生図に基づく状態は一部確認できました（`PARTIALLY_SUPPORTED`）。一方、事前に定めた検索の深さを満たせなかったため、応答の転用可能性と研究全体の正式判定は `INDETERMINATE`（判定不能）です。

本文の研究ID、正式判定コード、数値、出典識別子は、研究結果と照合できるよう原表記を残しています。

# 要旨

先行するG4研究では、管理への応答を別の場所に適用できるか独立に検証するための適格な対象を確保できず、正式判定をINDETERMINATE（判定不能）とした。これは適用の失敗を示さない。本研究はその確定済みの結果を変更せず、一般公開されたオンライン情報だけを使って、独立した管理への応答の証拠と、阿蘇の地域に関する生態学的な証拠を新たに探した。行政への照会、管理主体への問い合わせ、現地調査、非公開資料、人間参加者の調査は行っていない。

結果を見る前に、Track R（応答の転用に関する証拠）とTrack L（地域の生態学的な証拠）を分け、検索語14系列、出典の類型4系列、資料の適格性、独立性、重複、必要な検索範囲、正式判定の条件などを確定した。

Track Rでは、応答の方向を調べる前に候補資料の構造を監査した。G4-RF-01（管理の継続と停止に対する草原群集の組成・遷移の応答）について、三瓶山に関するTakahashiらの2014年の研究と、関東のススキ草地に関するYamamotoらの1997年の研究を、独立した検証用資料2件として適格と判断した。両方とも、阿蘇で元々確認した応答と変化の方向が一致した。

```text
RF01 eligible independent held-out = 2
RF01 concordant = 2
RF01 discordant = 0
```

ただし、得られた2件だけで正式な支持判定には進めなかった。事前の規則は、検索語と検索サービスの組合せごとに、重複を除いた上位100件（100件未満なら全件）を確認するよう求めていた。今回の検索環境では検索サービス固有のページ送りを安定して再現できず、56/56の検索枠で検索を終了したものの、**規則が求める検索の深さを満たした枠は0/56**だった。未調査の範囲に、方向が反対、同じ、または効果のない適格な資料が残る可能性を除けない。Track R全体の判定はINDETERMINATEとした。

Track Lでは、NAP-001で確定済みの環境省「現存植生図2024」と193の計画単位を、元データを変更せずに照合した。193/193単位で地図上の重なりを確認し、植生構成について計画単位と結び付けた状態（PU_LINKED_STATE）を示せた。地図上で開放・半自然草原に分類された候補面積は14,551.751418 haで、対象となる計画単位の62.286442%だった。この面積は地図に記された状態であり、管理への応答、生物多様性の点数、目標の達成度、管理の推奨ではない。植生図の作成根拠は2001・2007・2022年にまたがり、製品名に含まれる「2024」を共通の観測年とみなしていない。Track L全体はPARTIALLY_SUPPORTED（一部支持）とした。

また、RF05で対象とする植物名について、研究で確定した「ケルリソウ / Cynoglossum asperrimum」と、元の一次資料での「ケルリソウ / Trigonotis radicans」が一致しないことを確認した。結果を見てから対象種を黙って直すことは事前の規則に反するため、RF05はNON_ESTIMABLE（推定不能）とした。

研究全体の正式結果は次のとおりである。

```text
responseTransferOutcome = INDETERMINATE
localApplicabilityOutcome = PARTIALLY_SUPPORTED
studyOutcome = INDETERMINATE
```

公開された資料から一部の独立した応答の証拠と、阿蘇の計画単位に結び付いた植生情報は得られた。**公開資料が存在することだけでは、管理効果を別の場所に適用できるという正式な検証にはならない。** 本研究はその境界を保持した。

# 1. 研究の背景

## 1.1 先行研究から残った問題

G4研究の第1版では、元の調査地点での生態学的な応答を、独立した別の調査地点で再現できるかを、結果を見る前に定めた規則で検証した。ただし、当時確定した資料の範囲と規則では、条件を満たす独立した検証対象は0件だった。

G4第1版の正式判定は現在も次のままである。

```text
G4 v1
  COMPLETE / FROZEN
  formal outcome = INDETERMINATE
  eligible independent held-out contexts = 0
```

この0件は、

```text
transfer failure
```

ではない。

正しい解釈は、

```text
under the frozen G4 v1 evidence universe and rules,
response-transfer validation could not be estimated
```

である。

また運用情報取得研究の第1版では、対象30件のうち2件を確認し、28件は未解決のまま `PARTIAL_TARGET_INPUT_RESOLUTION` で閉じた。ただし、現時点の運用情報と管理への生態学的な応答の証拠は別物である。

## 1.2 本研究を独立研究とした理由

本研究で新しい公開資料が見つかっても、G4第1版に後から加え、当時も条件を満たす資料があったと書き換えることはできない。そのため、検索範囲、資料の適格性、出典群の重複、独立した検証対象の定義、正式判定を新たに事前確定する独立研究として開始した。

# 2. 研究対象

本研究の対象は、阿蘇の自然地域計画に関する次の2種類の証拠である。

```text
Track R = RESPONSE_TRANSFER
Track L = LOCAL_ECOLOGICAL_EVIDENCE
```

Track Rは管理方法と生態学的な応答の関係が、独立した地点でも再現するかを扱う。

Track Lは阿蘇の生態学的状態、種・生息地の状態、管理履歴、環境条件、空間的・時間的な適用範囲を扱う。

両者は代替関係にない。

```text
Track L evidence != Track R validation
environmental similarity != response-transfer validation
remote-sensing similarity != management-response evidence
```

# 3. 研究目的と中心的研究質問

中心的研究質問は次のとおりである。

> 結果を見る前に定めた公開オンライン資料の範囲で、阿蘇の管理方法と生態学的な応答について、独立した検証対象を取得・評価できるか。また別に、阿蘇の地域の生態学的な状態やその適用範囲をどこまで確認できるか。現地の状態、環境や衛星観測上の類似性を、管理への応答を別の場所へ適用できるという検証の代わりにしないで、それぞれの証拠から言える範囲を示せるか。

# 4. 先行研究との関係と新規性の範囲

本研究は、外部での検証、転用可能性、同一研究系列の資料をまとめる方法、応答を調べる前に適格性を判定する方法を新規発明として主張しない。

本研究固有の検証対象は、既に阿蘇Natural Area Planningで確定済みの管理方法と生態学的な応答の8類型、および地域の生態学的な状態について、公開オンライン資料だけで事前に定めた判定条件をどこまで満たせるかである。

# 5. 使用した情報と使用しなかった情報

## 5.1 使用した情報

使用する資料は、一般公開され、個別の許可、直接の問い合わせ、利用資格を必要としないものに限定した。

主な資料の種類は次のとおりである。

- 査読付きの一次研究
- J-STAGEなどで公開された学術記録
- 公開された機関リポジトリ
- 国・自治体の公開文書
- 農研機構などの公開研究成果
- 公開GIS・地理空間データ
- 公開された衛星観測データ
- 生物多様性・植生・生態系の公開情報
- 公開された学会要旨
- 出典を再現可能な形で記録できる公開API・資料目録

## 5.2 使用しなかった情報・手段

```text
行政照会
行政・管理主体への直接問い合わせ
現地確認
field visit
直接観測
field measurement
private communication
human participant interaction
restricted-access records
credential-gated local data
個別許可が必要な非公開資料
```

たとえば、関連性の高い論文で公開された全文が取得できず、ResearchGateなどで著者に本文を請求する経路だけが存在した場合、その請求は行わなかった。

# 6. 結果を見る前に確定した研究計画

正式な資料収集の前に次を固定した。

- 研究IDとTrack R・Track Lの区別
- 分析単位、証拠の7区分、応答の8類型、地域の状態の8項目
- 使用する資料の種類、検索語14系列、検索サービス4群
- 検索の深さと終了条件
- 資料の適格性と管理方法・測定結果の一致条件
- 独立性と同一研究系列の扱い、検証用資料の条件
- 地域との結び付き、時間的な有効性、欠測・矛盾の扱い
- 正式判定の区分、誤読を想定した24事例、先行研究の結果を変更しない規則

応答の方向を見た後で資料の適格性の条件を緩めることは禁止した。

# 7. 方法

## 7.1 Track Rの独立した評価単位

独立した評価単位は論文の件数ではなく、

```text
relation family
× underlying study-site-context
× management-contrast cluster
× ecological-response construct
```

とした。

同じ場所、実験、調査、対象集団を共有する複数の論文は、原則として一つの研究系列にまとめた。

## 7.2 応答を見る前に行う構造の事前分析

独立した検証用資料の応答を正式に調べる前に、少なくとも以下を判定した。

```text
source identity
publication family / duplicate lineage
management exposure
comparator
response construct
measurement compatibility
mandatory context completeness
spatial domain
temporal window
independence
held-out eligibility
```

この構造上の条件を満たさない候補は、応答が元の研究と一致しそうでも検証資料に採用しなかった。

## 7.3 Track Lで空間的に言える範囲

地域との結び付きについて次を区別した。

```text
PU_LINKED_STATE
ASO_LOCAL
REGIONAL_CONTEXT
EXTERNAL_CONTEXT
UNRESOLVED_SPATIAL_LINKAGE
```

`PU_LINKED_STATE`は計画単位の形状と再現可能な形で結び付く状態を示すが、管理への応答ではない。

## 7.4 資料の検索方法

検索語14系列と検索サービス4群の組合せを事前に確定した。

```text
14 query families × 4 service groups = 56 frozen cells
```

検索停止は支持する証拠が見つかった時点ではなく、すべての検索枠が終了状態になることとした。

# 8. 主要結果

## 8.1 検索の終了

```text
frozen cells = 56
terminal cells = 56
formal-depth satisfied cells = 0
terminal state = ACCESS_ROUTE_UNAVAILABLE
```

使用した検索環境では、J-STAGE、CiNii Research、国立国会図書館サーチ、出版者やDOIのページ、公式サイト、オープンデータの目録、一般的なウェブ検索から候補を見つけ、出典を確認できた。一方、事前に定めた「検索語とサービスの組合せごとに重複を除く上位100件、100件未満なら全件」という深さを再現可能な形で証明できるページ送りの方法が利用できなかった。

したがって、

```text
search stopping rule satisfied = true
search universe exhausted = false
```

である。

## 8.2 RF01 — 植生遷移と群集組成の応答

RF01は、管理の継続と停止・放棄を比較したときの、群集組成と植生遷移の応答を対象とする。

本研究の構造上の条件を満たした独立した検証対象は次の2件であった。

1. Takahashiら（2014）— 三瓶山のススキ型半自然草原
2. Yamamotoら（1997）— 関東のススキ型草原での長期的な人工的圧力に関する実験

両資料について、管理方法と背景、直接測定された組成・遷移、観測期間、気候や地域条件を、応答を読み取る前に確認した。

正式に応答を読み取った後は次のとおりであった。

```text
Aso frozen source direction = DECREASE
Sanbe held-out direction = DECREASE
Kanto held-out direction = DECREASE

eligible held-out = 2
concordant = 2
discordant = 0
```

ここで`DECREASE`は、確定済みの比較方向に照らして、管理を継続した側で遷移の進行が小さいことを表す。

得られた2件は、全面的な支持に必要な件数と方向の一致という条件を満たした。しかし未調査の資料に異なる結果がある可能性を除けないため、正式判定は `INDETERMINATE` とした。

## 8.3 RF02 — 開放草原の構造

三瓶山の研究系列1件が条件を満たした。

元の研究と検証用資料で直接測定した草原の構造は、草丈、優占度、バイオマス、枯れ草などが一方向に揃う単一の数値ではない。そこで重み付きの総合点を作らず、結果を `MIXED_OR_NONMONOTONIC` とした。

```text
eligible held-out = 1
concordant = 1
formal outcome = INDETERMINATE
```

検索を完了できたとしても、検証対象1件では事前に定めた全面支持の条件には達しない。

## 8.4 RF03 / RF04 / RF06 / RF07 / RF08

今回取得した候補資料からは条件を満たす独立した検証対象を確認できなかった。

ただし検索深度未達のため、これを

```text
NO_ELIGIBLE_INDEPENDENT_CONTEXTS
```

とはしない。

正式判定はすべて `INDETERMINATE` とした。

除外理由には、管理時期や背景の不一致、対象分類群の不一致、同一研究系列の重複、同じ場所の再利用、測定結果の不一致、必要な地域条件の不足などがあった。

## 8.5 RF05 — 対象種の同定に関する不一致

RF05では応答を調べる前に、対象種の同定に問題が見つかった。

事前に確定した関係と測定対象の定義:

```text
ケルリソウ / Cynoglossum asperrimum
```

A03の公開一次資料:

```text
ケルリソウ = Trigonotis radicans
```

現在の学名:

```text
Trigonotis radicans var. radicans
```

対象種が正確に一致するかはRF05の必須条件である。研究開始後に学名を黙って修正して判定することはできない。

```text
RF05 formal outcome = NON_ESTIMABLE
```

とした。

## 8.6 Track L — 計画単位に結び付けた生態学的状態

NAP-001で公開資料から作成した現存植生図と計画単位の重ね合わせ結果を、元データを変更せずに監査した。

```text
planning units = 193
planning units with mapped coverage = 193
planning units passing area-closure QA = 193
positive-area intersections = 4255
```

計画単位内の地図上の植生分類は次のとおりである。

```text
total planning-unit area                 23,362.630734 ha
OPEN_SEMINATURAL_GRASSLAND_CANDIDATE     14,551.751418 ha  62.286442%
OTHER_GRASSLAND_OR_MODIFIED_GRASSLAND     3,170.322441 ha  13.570058%
WOODY_OR_NON_GRASSLAND                    5,483.641581 ha  23.471850%
UNRESOLVED_OR_UNMAPPED                      156.915294 ha   0.671651%
```

植生図作成の根拠となった年:

```text
2001
2007
2022
```

であり、すべて2024年に同時に観測されたものではない。

L-01（植生の構成・状態）は計画単位に結び付いた植生図上の分類として `SUPPORTED_WITHIN_FROZEN_SCOPE` とした。

L-02は植生図上の開放草原の有無・状態まで確認できるが、草丈、木本の割合、枯れ草など直接測った構造ではないため `PARTIALLY_SUPPORTED` とした。

その他のL-03～L-08も、元の調査地点、阿蘇地域、周辺地域、観測所を参照した値、過去の状態、代理指標といった証拠の適用範囲を守って `PARTIALLY_SUPPORTED` とした。

# 9. 正式結果

## 9.1 Track R

| 関係の類型 | 採点した独立検証資料 | 得られた資料での結果 | 正式判定 |
|---|---:|---|---|
| RF01 | 2 | 方向が一致2件・不一致0件 | `INDETERMINATE` |
| RF02 | 1 | 方向が一致1件 | `INDETERMINATE` |
| RF03 | 0 | 取得資料に適格な検証対象なし | `INDETERMINATE` |
| RF04 | 0 | 取得資料に適格な検証対象なし | `INDETERMINATE` |
| RF05 | 0 | 元の定義と対象種の同定が不一致 | `NON_ESTIMABLE` |
| RF06 | 0 | 新たな適格な独立資料なし | `INDETERMINATE` |
| RF07 | 0 | 新たな適格な独立資料なし | `INDETERMINATE` |
| RF08 | 0 | 新たな適格な独立資料なし | `INDETERMINATE` |

Track R:

```text
responseTransferOutcome = INDETERMINATE
```

## 9.2 Track L

| 地域の状態 | 確認できた最も詳細な地域との結び付き | 正式判定 |
|---|---|---|
| L-01 植生の構成・状態 | `PU_LINKED_STATE` | `SUPPORTED_WITHIN_FROZEN_SCOPE` |
| L-02 植生図上の開放草原の状態 | `PU_LINKED_STATE` | `PARTIALLY_SUPPORTED` |
| L-03 対象種の状態 | `ASO_LOCAL` | `PARTIALLY_SUPPORTED` |
| L-04 チョウ類群集の状態 | `ASO_LOCAL` | `PARTIALLY_SUPPORTED` |
| L-05 希少な草原性チョウ類の状態 | `ASO_LOCAL` | `PARTIALLY_SUPPORTED` |
| L-06 管理方法と背景条件 | `ASO_LOCAL` | `PARTIALLY_SUPPORTED` |
| L-07 環境条件 | `ASO_LOCAL` | `PARTIALLY_SUPPORTED` |
| L-08 時間的な条件 | `PU_LINKED_STATE` | `PARTIALLY_SUPPORTED` |

Track L:

```text
localApplicabilityOutcome = PARTIALLY_SUPPORTED
```

## 9.3 研究全体

```text
studyOutcome = INDETERMINATE
```

Track Lで一部が支持されても、Track Rの判定不能という結果は変わらない。

# 10. 本研究で確認できたこと

本研究で確認したのは、次の点である。

1. 公開されたオンライン資料だけでも、阿蘇の生態学的な状態の一部を計画単位の形状と再現可能な形で結び付けられる。
2. 管理への応答の転用を調べる資料は、論文数ではなく独立した調査地点・条件で数えられる。
3. RF01では独立した検証資料2件の応答方向が元の研究と一致し、取得できた範囲に独立の応答の証拠が存在した。
4. 地域の状態と応答の転用に関する証拠を分ければ、衛星観測や環境条件の類似性を応答の検証と取り違えずに利用できる。
5. 元の研究で使った対象種の同定の問題を、応答の方向とは別の定義上の問題として発見できる。

# 11. 本研究が支持しないこと

本研究は以下を支持しない。

```text
RF01 transfer is formally proven
all relevant public evidence was exhausted
no discordant evidence exists
no eligible RF03/RF04/RF06/RF07/RF08 context exists
mapped vegetation class = management response
PU_LINKED_STATE = PU_MANAGEMENT_RESPONSE
environmental similarity = response validation
NDVI = direct open-grassland structure
local occurrence = management response
evidence found = management recommended
```

また、以下は一切生成していない。

```text
management recommendation
action ranking
optimization coefficient
planning-unit exact management response
ecological safety claim
permission claim
operational feasibility claim
human usability / practitioner acceptance claim
transfer_to_zone_contribution = true
```

# 12. 実務的含意

公開されたオンライン資料で、計画の検討に使う**生態学的な状態と環境条件**について情報を補える。特に植生図上の構成は、193の計画単位すべてに再現可能な形で対応付けられる。

一方、管理行為の効果を計画単位ごとの応答へ当てはめることは依然として別問題である。RF01で独立した資料に応答方向の一致が見られたことは科学的に重要だが、これをそのまま管理効果の係数や候補行為の推奨へ変換することはできない。

# 13. 研究上の限界

## 13.1 最大の限界 — 検索の深さ

最大の限界は、結果を見る前に定めた検索の深さを、使用した検索環境で満たせなかったことである。

得られた一致そのものは残るが、関連する公開資料を調べ尽くしたとは言えない。

## 13.2 オンラインで公開されているか

書誌情報が公開されていても、一次資料の全文は公開されていない場合がある。著者への請求や資格が必要な経路は使わなかったため、その資料は応答の採点に進めなかった。

## 13.3 地域の証拠の時間的不均一性

現存植生図の製品名に「2024」が含まれていても、計画単位に使われた図の作成根拠は2001年、2007年、2022年に分かれる。同時点の現状を直接示すものではない。

## 13.4 対象種と現在の状態に関する不足

対象種、チョウ類群集、希少なチョウ類について、現在の状態を計画単位ごとに示す公開された観測データは得られていない。

## 13.5 RF05 分類学上の同定

RF05では元の研究で確定した対象種の同定が一致しないため、第1版の途中で修正できない。

# 14. 第三者資料・データの取扱い

本研究は第三者の論文、政府資料、公開GISなどを出典として利用したが、この報告書では第三者の本文や図表、利用に制限のある位置情報を再配布しない。

希少種の詳細な生息地を推測・公開することも行っていない。

# 15. 後続研究との境界

少なくとも次の課題を後続研究に残す。

1. **Public-online response-transfer successor**  
   検索サービス固有のページ送りやAPIを使って事前に定めた検索の深さを達成できる環境で、新たな研究として検証する。

2. **Trigonotis radicans var. radicans response study**  
   正しい対象種を研究開始前に確定し、刈取りへの応答を別研究で検証する。

3. **FUTURE / DEFERRED / PRESERVED routes**  
   行政への照会、現地確認、直接観察と測定、適法に利用できる地域の資料、人間参加者による検証。

これらはすべて別の研究IDで実施し、本研究やG4第1版の結果をさかのぼって書き換えない。

# 16. 再現性・検証

正式な結果の検証:

```text
PASS
```

正式な判定条件:

```text
PE0–PE10 = PASS within named scope
PE11 = PASS FOR CLOSURE WITH MATERIAL SEARCH-COVERAGE LIMITATION
```

誤読を想定した監査:

```text
registered = 24
passed = 24
failed = 0
```

主な監査内容は、同じ研究系列の論文や同じ場所の重複計上、管理方法の不一致、代理指標や地域の類似性を応答の証拠へ格上げする誤り、広域の情報を計画単位に当てはめる誤り、支持する結果を見つけた時点での検索打ち切り、結果を見た後の条件緩和、先行研究の結果の書き換え、総合点への安易な集約である。

# 17. 再現性識別子

```text
Study ID:
  NAP-POERT-2026-08-24-v1

Base main:
  1656c54e505bd23838e5876981ade8ef1938db78

Scientific-state snapshot:
  dc1633205b84e6bf9409c9fb360278bee9cb840b

Formal result blob:
  ccfdd67a82019878a33f039ec21242a4704f8ea9

Planning-unit geometry SHA-256:
  46ef4dd475ec7645d78130722e8ddfcae9f51c6244ce95dc22ea9f7dcaa6609d

Frozen planning_unit_vegetation_composition.csv SHA-256:
  ac01c133cf8d366dc02d0da2b8e1ff1334e5b997f31b74553cd60f0afc4b5413

Frozen planning_unit_open_grassland_state.csv SHA-256:
  c6aee6d304e223189289e8b2f8bcbf5f42042b037304741365091eea77a4a93c

Search cells:
  56 terminal / 0 formal-depth-satisfied

Formal outcomes:
  responseTransferOutcome = INDETERMINATE
  localApplicabilityOutcome = PARTIALLY_SUPPORTED
  studyOutcome = INDETERMINATE
```

# 18. リポジトリ内の主要資料

## 研究計画

```text
doc/public-online-ecological-transfer/PUBLIC_ONLINE_ECOLOGICAL_RESPONSE_TRANSFER_PROSPECTIVE_PROTOCOL.md
analysis/public-online-ecological-transfer/study_spec.json
analysis/public-online-ecological-transfer/search_strategy.json
analysis/public-online-ecological-transfer/relation_anchor_registry.csv
analysis/public-online-ecological-transfer/local_construct_registry.csv
```

## 検索と資料の取得

```text
analysis/public-online-ecological-transfer/acquisition_start.json
analysis/public-online-ecological-transfer/search_execution_log.csv
analysis/public-online-ecological-transfer/search_matrix_terminalization.csv
analysis/public-online-ecological-transfer/search_service_access_audit.json
analysis/public-online-ecological-transfer/search_closure.json
```

## 結果

```text
analysis/public-online-ecological-transfer/formal_result.json
analysis/public-online-ecological-transfer/formal_relation_results.csv
analysis/public-online-ecological-transfer/formal_local_construct_results.csv
analysis/public-online-ecological-transfer/response_extraction_batch5.csv
analysis/public-online-ecological-transfer/track_l_historical_spatial_inheritance_audit.json
analysis/public-online-ecological-transfer/track_l_conflict_audit.json
analysis/public-online-ecological-transfer/historical_anchor_identity_audit.json
```

## 検証

```text
analysis/public-online-ecological-transfer/formal_validation.json
analysis/public-online-ecological-transfer/adversarial_expected_cases.csv
analysis/public-online-ecological-transfer/adversarial_closure_audit.json
analysis/public-online-ecological-transfer/validate_formal_closure.py
```

## 進捗記録

```text
doc/checkpoints/2026-08-24-public-online-ecological-transfer-design-freeze.md
doc/checkpoints/2026-08-25-public-online-ecological-transfer-acquisition-start.md
doc/checkpoints/2026-08-25-public-online-ecological-transfer-formal-closure.md
```

# 19. 結論

一般公開されたオンライン資料から、阿蘇の計画単位に結び付いた植生情報と、一部の管理への応答について独立した証拠を得た。193の計画単位の地図上の植生状態を確認し、地域の証拠に関するTrack Lは PARTIALLY_SUPPORTED（一部支持）とした。

応答の転用に関するTrack Rでは、RF01の独立した検証用資料2件がともに阿蘇の元の応答と同じ方向を示した。ただし、結果を見る前に定めた検索の深さを満たせなかったため、得られた2件だけで正式な全面支持とは判定できない。応答の転用に関する判定と研究全体の判定は INDETERMINATE（判定不能）である。

**判定不能は転用の失敗を意味しない。また、得られた一致をなかったことにする判定でもない。** 未調査の範囲に異なる証拠が残る可能性を除けないため、正式な結論を確定しなかった。

```text
responseTransferOutcome = INDETERMINATE
localApplicabilityOutcome = PARTIALLY_SUPPORTED
studyOutcome = INDETERMINATE
```

---

## 用語

**PUBLIC-ONLINE ONLY**  
個別の許可や直接連絡、特別な利用資格を必要としない公開資料だけを、正式な証拠の対象とする方針。

**held-out context**  
元の研究とデータの出自が独立し、管理方法・測定結果・必要な地域条件について、事前に定めた条件を満たす検証対象。

**PU_LINKED_STATE**  
確定済みの計画単位の形状と再現可能な形で結び付けた生態学的な状態。管理への応答は示さない。

**INDETERMINATE**  
支持・不支持のどちらも意味せず、事前に定めた規則では正式な結論を出せない状態。

**NON_ESTIMABLE**  
推定する対象や対象種の同定が研究で確定した定義と一致せず、その関係を正しく推定できない状態。

## 参考文献・関連する先行研究

- Wenger, S. J. & Olden, J. D. (2012). Assessing transferability of ecological models across space and time. *Methods in Ecology and Evolution*.
- Bareinboim, E. & Pearl, J. (2013). A general algorithm for deciding transportability of experimental results. *JMLR Workshop and Conference Proceedings / PMLR*.
- Dahabreh, I. J. et al. (2020). Methods for transporting trial results to target populations. *Statistics in Medicine*.
- Yamamoto, Y. et al. (2002). 阿蘇地域の半自然草地における火入れ中止にともなう植生の変化. *日本草地学会誌* 48(5):416–420. DOI `10.14941/grass.48.416`.
- Yamamoto, K. et al. (1997). Ordination of Vegetation of Miscanthus-type Grassland under the Some Artificial Pressure. DOI `10.14941/grass.42.307`.
- Takahashi et al. (2014). Effect of Cattle Grazing Associated with Burning on Vegetation and Species Diversity in Miscanthus-type Grassland at the Foot of Mount Sanbe. DOI `10.14941/grass.60.102`.
- Yasunaka et al. (2015). Assessing the effect of controlled burning and grazing on vegetation change in the grasslands of Aso region using satellite image analyses. DOI `10.14962/jass.31.4_117`.
- 環境省生物多様性センター. 現存植生図2024 — 九州沖縄ブロック.

## 引用時の推奨表記

```text
Natural Area Planning / NAP-POERT-2026-08-24-v1 (2026).
Public Research Report:
「公開オンライン情報による生態学的応答転移・局所生態証拠の探索と検証」.
Version 1.0.1, 日本語表現改訂 2026-09-28（科学的結果は2026-08-25確定）。
Formal outcome: INDETERMINATE
(response transfer: INDETERMINATE;
 local applicability: PARTIALLY_SUPPORTED).
Study snapshot: nkkmd/natural-area-planning @ dc1633205b84e6bf9409c9fb360278bee9cb840b.
```