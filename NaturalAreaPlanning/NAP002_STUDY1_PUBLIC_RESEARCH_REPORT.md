# Natural Area Planning / NAP-002 Study 1 — 公開研究報告書

**公開情報だけで阿蘇半自然草原の管理判断をどこまで支援できるか**  
**― 「何をすべきか」を断定せず、「何が判断を止めているか」を明示する ―**

- レポート版: **v1.0.2**
- 作成日: **2026-08-13 JST**
- 研究プロジェクト: **Natural Area Planning / NAP-002 Study 1**
- 研究状態: **研究1完了・結果確定済み（公開証拠の範囲内での意思決定支援）**
- 研究結果を確定した時点: `nkkmd/natural-area-planning` / コミット `93a6ab91c0dbcbac2dfa32c4ff11700f745770fc`
- 本文の性格: **単体公開用研究レポート**
- 編集改訂: **v1.0.1で引用情報を更新。v1.0.2で日本語表現を改訂（2026-09-28）。科学的結果は変更なし**

> この文書は、元のGitHubリポジトリ、内部の研究ログや進捗記録、CSV、コードを参照しなくても、NAP-002 Study 1の背景、問い、方法、主要結果、限界、再現性、実務上の意味、今後の研究課題を理解できるように構成している。GitHub外へこのファイル単体をコピーして公開しても、研究レポートとして成立することを意図している。

---

## 初めて読む方へ

研究01で見つかった証拠の不足を前提に、「どこを検討し、何が判断を止め、次に何を調べるか」を示す方法を作った報告書です。193の計画単位のうち188は管理を検討する対象と判定できました。しかし、管理行為をどの土地で実施すべきかという推奨や最適配置は示していません。

## 要旨

半自然草原の管理では、「どこを保全すべきか」だけでなく、「どの管理を、どこで、どの条件で行うべきか」が実務上の問題になる。しかし、その問いに答えるには、対象地の状態だけでなく、保全対象の存在、管理による応答、元の調査地点で得られた応答を別の場所へ適用できるか、生態学的な悪影響や競合を防ぐ条件、実行可能性、資源、当日の条件など、性質の異なる情報が必要である。

Natural Area Planning / NAP-001は、熊本県阿蘇地域の半自然草原を対象として、公開情報だけから管理方法を明示した体系的な保全計画をどこまで構築できるかを検討した。その結果、193の計画単位、管理方法・保全対象の構造、公開植生データから得た基礎的な状態、元の調査地点で確認された管理への応答、計画ソフトへの構造的写像までは構築できた一方、元の調査で得た管理への応答を計画単位へ適用する根拠が不足し、計画に直接利用できる管理への応答（Q3）= 0、地域の管理方法と条件を結ぶモデル（Q4）= 0、正式な最適化計算は **NOT AUTHORIZED** と判定して公開情報のみを用いたStage Cを閉じた。

NAP-002 Study 1は、この準備が整わなかったという結果を救済するために係数を補う研究ではない。研究質問を一段上流へ変更した。

> **管理効果を計画単位へ定量的に転移できない場合でも、証拠の限界を保持したまま、「どこを管理レビュー対象とするか」「何が候補行動の判断を止めているか」「次に何を確認する必要があるか」を再現可能な意思決定支援として表現できるか。**

Study 1では、意思決定をG1–G8という、ほかの条件では代替できない判定条件へ分解した。G1は管理の検討対象範囲、G2–G5は保全対象ごとの関連性・管理への応答を示す証拠・管理への応答を別の場所へ適用できるか・生態学的な悪影響・競合を防ぐ条件、G6–G8は地域で管理を実行できるか・資源と対応能力・現時点の運用条件を表す。生態学的証拠を対象別に保持するため、機械で読み取れる表現は `planning unit × candidate action × feature` のTier Eと、`planning unit × candidate action` のTier Aの二層とした。

結果として、G1では193の計画単位のうち188（97.41%）が `PASS_PUBLIC`、1が `UNRESOLVED`、4が `NOT_APPLICABLE`となり、公開空間情報だけでも広い管理の検討対象となる範囲を定義できた。一方、判断規則の全体はTier E 22,113件、Tier A 2,509件、計24,622件となり、検証時のエラーは0であったが、G4・G6・G7・G8の `PASS_PUBLIC` はすべて0だった。すべての出典で確認された管理への応答はG4で計画単位への適用を禁止され、地域での実行可能性や現時点の条件も公開情報だけでは確定できなかった。

したがって、**公開情報のみで管理の検討対象範囲はかなり具体化できるが、どの管理をどの計画単位へ割り当てるべきかは正当化できない**、というのがStudy 1の主要結果である。

本研究はこの状態を「情報不足」と一括しなかった。不足を、地域の保全対象との関連性、地域の生態学的な悪影響を防ぐ条件、管理への応答を別の場所へ適用できるかの検証、管理行為の内容、アクセス、設備、管理上の権限、資源と対応能力、現地の状態・天候・可燃物・安全・許可の現状等へ分解し、最終的な実務表現を次の三部構造として閉じた。

```text
WHERE
  Management Review Scope Map

WHY
  Candidate Action × Decision-Gate Blocker Matrix

WHAT NEXT
  Candidate Action × Required-Input Checklist
```

さらに、完全に架空の2例について、許可された地域固有・現時点の事実に関する入力をすべて満たした場合を検証したが、野焼き単独と年2回刈取りの両方で `RESEARCH_EVIDENCE_REQUIRED` が残った。これは、現場情報の充足が管理への応答を示す証拠や管理への応答を別の場所へ適用できるかを自動的に代替しないことを示す。

本研究の中心的成果は、推奨管理地図ではない。**「公開情報でどこまで進めるか」と「どこから先は地域固有の事実・現時点の事実・新しい科学的検証が必要か」を、不明をゼロに置き換えずに機械追跡可能な形で分離したこと**である。

---

# 1. 研究の背景

## 1.1 半自然草原では「保護する」だけでは管理問題を解けない

半自然草原は、長期間にわたる野焼き、放牧、採草・刈取りなどの人為管理と結びついて成立・維持されてきた場合がある。そのような生態系では、利用や攪乱を止めることが必ずしも保全と同義ではない。管理停止によってリター蓄積、植生遷移、木本化等が進む可能性がある一方、管理を強めれば常に良いわけでもない。

管理効果は、少なくとも次の要素に依存する。

```text
management effect
 = f(
     management type,
     intensity,
     timing,
     conservation target,
     background management,
     ecological context
   )
```

したがって、実務的な問いは単純な

```text
管理する / 管理しない
```

ではない。

より適切な問いは、

> **どの保全対象に対して、どの管理を、どの強度・時期・条件で検討できるのか。**

である。

## 1.2 NAP-001が明らかにした「計算より前の不足」

前身研究NAP-001では、公開情報だけを用いて阿蘇半自然草原の管理方法を明示した空間計画を構築しようとした。

その研究では、

- 193の計画単位
- 運用上の管理方法
- 保全対象別の保全計画の枠組み
- 13種類の候補となる管理方法
- 11 保全対象と補助対象
- 公開GIS・公開植生データから得た基礎的な状態
- 元の調査地点での管理への応答を示す証拠
- 計画ソフトへの構造上の対応付け

までを構築した。

しかし正式な空間配置には、それだけでは足りない。

たとえば、ある論文で特定の放牧強度や刈取り時期に対する反応が観察されても、その効果を別の計画単位へそのまま数値転移できるとは限らない。元の調査地点の履歴、背景管理、処理定義、測定対象、立地条件等が異なるためである。

NAP-001はこの点を、次のように閉じた。

```text
Q3 planning-response features           = 0
Q4 local management × context models   = 0
coefficient-ready regimes              = 0
zone contribution rows                 = 0
formal optimizer authorized            = false
```

重要なのは、最適化ソフトを動かせなかったのではなく、**最適化ソフトへ渡す数値を科学的に正当化できなかった**ことである。

## 1.3 NAP-002の出発点

この結果には実務上の問題が残る。

研究者が

> 「ここから先は証拠が足りない」

と正しく結論しても、行政担当者や現場管理者は依然として、

```text
どこを検討対象にするのか
どの候補管理について何が分かっているのか
何が判断を止めているのか
次に何を確認すべきなのか
```

を知る必要がある。

NAP-002は、この不足を仮の管理効果や実行可能性を示す単一の点数で埋めるのではなく、**不足する情報そのものを意思決定支援に使える形へ変換する**ことを目的とした。

---

# 2. 研究対象 — 阿蘇半自然草原

Study 1はNAP-001と同じ、熊本県阿蘇地域の凍結された193の計画単位を対象とする。

阿蘇は、野焼き、放牧、採草などの人間活動と長期的に関係しながら維持されてきた半自然草原を含む。そのため、単純な土地被覆図だけではなく、管理行為と保全対象の関係を意思決定へ接続する必要がある。

NAP-002は、新たな生態学的応答のデータを収集した研究ではない。NAP-001が凍結した公開証拠、管理方法の分類、保全対象の分類、別の場所への適用に関する限界、公開空間状態を継承し、**それらを意思決定上の判定条件へ変換する研究**である。

---

# 3. 研究目的と中心的研究質問

NAP-002 Study 1の中心的研究質問は次のとおりである。

> **定量的な管理効果の空間転移や最適配分を科学的に正当化できない状況においても、既存証拠の限界と不確実性を保持したまま、実務者が「どこで、どの管理について、次に何を確認・判断すべきか」を再現可能に提示する意思決定支援を構築できるか。**

より形式的には、

> **NAP-001が凍結した公開証拠から言える範囲を壊さず、計画単位ごとの生態学的効果や管理行為の推奨を捏造することなく、管理の検討対象範囲、判断を妨げる要因、次に必要な情報へ変換できるか。**

である。

Study 1の正式な回答は、

```text
YES
```

として閉じられた。

ただし、このYESは

```text
管理推奨ができる
```

という意味ではない。

支持された結果の範囲は、

```text
scope
+
blocker
+
information need
```

である。

---

# 4. 先行研究との関係

## 4.1 不確実性を伴う意思決定支援自体は新しくない

自然資源管理・保全分野では、構造化された意思決定（Structured Decision Making、SDM）、順応的管理、情報価値（Value of Information、VoI）、不確実性に強い意思決定、不確実性を考慮した空間的な保全計画、複数の管理候補の優先順位付け、不確実性の可視化、地図を使った意思決定支援について、幅広い先行研究がある。

したがってNAP-002は、次の一般概念を新規発明として主張しない。

```text
判断を要素に分けること
不確実性を明示すること
必要な情報を特定すること
地図で不確実性を示すこと
複数の候補行動を比較する枠組み
判断に必要な情報に基づき継続観測を設計すること
```

## 4.2 Value of Informationとの違い

VoIは、どの不確実性を解消することが意思決定価値を高めるかを評価する成熟した枠組みである。

しかしVoIを正式に計算するには、少なくとも管理行為、測定する結果、目的、不確実性の関係が十分に規定されている必要がある。

NAP-001の中心結果は、計画単位ごとの管理行為と応答の関係そのものが十分に閉じていないことだった。その状態で、判断を妨げる要因へ重みを付けて「重要度」を計算すると、新たな根拠のない見かけ上の精密さを導入する危険がある。

そのためStudy 1は、

```text
判断を妨げる要因を特定する
!=
その要因を解消する情報の価値を推定する
```

とした。

## 4.3 NAP-002が主張できる範囲

研究1で主張できる範囲は、一般理論の発明ではなく、次の証拠を実務の判断に結び付ける仕組みである。

```text
frozen evidence-readiness ceiling
+
anti-pseudo-precision rules
+
planning unit × candidate action × gate provenance
+
non-transferability retained as output
+
unknown / missing local facts retained as blockers
+
machine-readable ruleからpresentationを生成
```

この組合せを阿蘇の公開情報から得た証拠のつながりに適用し、実装・検証したことがStudy 1の位置づけである。

---

# 5. 公開情報だけを用いた研究設計

## 5.1 使用した情報

Study 1は、以下だけを研究入力として使用した。

- NAP-001で凍結済みの公開資料と証拠の構造
- 公開GIS由来の193の計画単位の識別情報と形状
- 公開植生情報から構築された凍結済み植生構成
- 公開植生情報から構築された開放草原の状態
- NAP-001で整理済みの13種類の候補となる管理方法
- NAP-001で整理済みの保全対象と補助対象
- NAP-001の管理方法と保全対象の証拠の関係
- NAP-001の応答を別の場所へ適用できるかの点検
- 架空の条件による検証例に用いる入力

## 5.2 使用しなかった情報

Study 1は以下を使用していない。

- 利用に制限のある生態学的資料
- 許可制・申請制の牧野カルテ等の地域の元データ
- 非公開の希少種の位置情報
- 非公開の生産者情報
- 新たな現地測定
- 実在の実務者から得た情報
- 実際の地域での実行可能性を示す値
- 実際の現時点の気象・安全・許可情報

したがって、Study 1は公開情報だけを用いた後続研究として完結している。

## 5.3 NAP-001の歴史状態を変更しない

Study 1の重要な研究結果を守る規則は、NAP-001の準備が整わなかったという結果を書き換えないことである。

最終監査では、

```text
analysis/nap001 files modified by NAP-002 = 0
```

であった。

また、全生態学的な判断記録で、

```text
transfer_to_zone_contribution = false
```

を変更しない条件として保持した。

---

# 6. 再現性の前提 — M1–M3のデータを正確に復元

NAP-002は、過去の計画単位の形状や植生情報の出力を「だいたい同じ」状態で復元して分析を始めなかった。

最初の実測資料に基づく計画単位の記録を作る前に、次の3つの先行研究で確定した識別情報を元データのバイト単位のSHA-256で正確に照合した。

## M1 — 計画単位の形状と識別情報

```text
p001_p4_aso_pastures_193.geojson
features = 193
unique pu_id = 193
SHA-256 = 46ef4dd475ec7645d78130722e8ddfcae9f51c6244ce95dc22ea9f7dcaa6609d
```

## M2 — 植生構成

```text
planning_unit_vegetation_composition.csv
rows = 1426
planning units = 193
SHA-256 = ac01c133cf8d366dc02d0da2b8e1ff1334e5b997f31b74553cd60f0afc4b5413
```

## M3 — 開放草原の状態

```text
planning_unit_open_grassland_state.csv
rows = 193
unique planning_unit_id = 193
SHA-256 = c6aee6d304e223189289e8b2f8bcbf5f42042b037304741365091eea77a4a93c
```

M1とM3の計画単位のIDの集合は完全一致し、M2のIDの集合もM1に完全に含まれた。

この照合条件を設けた理由は、地理データの再保存や再生成による微妙な変更を、Study 1の新しい実測資料に基づく状態として無意識に混入させないためである。

---

# 7. 方法 — 判断を段階ごとに確認する仕組み

## 7.1 なぜ実行可能性を一つの点数にしなかったのか

意思決定が進められない理由には、異なる種類がある。

```text
保全対象がいるか分からない
管理効果の証拠がない
元の調査地点での応答をこの場所へ適用できない
悪影響を防ぐ条件を確認できない
現地で実行できるか分からない
人員・予算・機械の対応能力が分からない
当日の状態や許可が分からない
```

これらを1つの0～100の単一の点数にまとめると、たとえば「強い証拠」が「未確認の安全条件」を相殺するような誤読を生む。

Study 1では、各判定条件を**相互に代替できないもの**として保持した。

## 7.2 G1–G8

| 判定条件 | 問い | 主な情報レベル |
|---|---|---|
| G1 | この計画単位は半自然草原の管理を検討する対象か | 公開情報から得た空間上の状態 |
| G2 | 関連する保全対象がこの場所に関係するか | 公開情報と地域の確認 |
| G3 | この候補行動に対する管理への応答を示す証拠があるか | 元の調査から得た証拠 |
| G4 | 元の調査地点で確認された応答を計画単位へ適用できるか | 管理への応答を別の場所へ適用できるかの検証 |
| G5 | 生態学的な悪影響・競合を防ぐ条件が閉じているか | 元の調査と地域で確認する条件 |
| G6 | 管理行為をこの場所で実行できるか | 地域固有の運用情報 |
| G7 | 必要な資源・対応能力があるか | 地域の対応能力 |
| G8 | 現時点の運用条件が満たされるか | 現時点で確認すべき事実 |

## 7.3 二層のデータ構造

G2–G5は保全対象によって状態が異なり得る。したがって、`planning unit × candidate action`だけに潰すと、保全対象によって異なる競合を失う。

このため二層とした。

```text
Tier E — ECOLOGICAL_FEATURE
planning_unit_id × candidate_action_id × feature_id
G2 target relevance
G3 management-response evidence
G4 response transferability
G5 ecological safeguard/conflict

Tier A — ACTION_CONTEXT
planning_unit_id × candidate_action_id
G1 management-review scope
G6 local operational feasibility
G7 resource/capacity feasibility
G8 current operational conditions
```

## 7.4 判定条件の状態区分

Study 1で使用した状態は次の8つである。

```text
PASS_PUBLIC
SUPPORTED_SOURCE_LOCAL
CONDITIONAL
UNRESOLVED
LOCAL_INPUT_REQUIRED
CURRENT_INPUT_REQUIRED
NOT_APPLICABLE
DO_NOT_INFER
```

ここで重要なのは、`SUPPORTED_SOURCE_LOCAL` がG3でのみ使われ、計画単位への適用可能性を意味しないことである。

```text
SUPPORTED_SOURCE_LOCAL at G3
!=
PASS_PUBLIC at G4
```

また、

```text
NOT_APPLICABLE
!=
SAFE
```

である。たとえばG5で `NOT_APPLICABLE` なら、「その記録についてG5に登録された競合がない」というだけで、候補行動全体の安全性を意味しない。

## 7.5 判断を止める状態

次を判断を妨げる要因として扱った。

```text
CONDITIONAL
UNRESOLVED
LOCAL_INPUT_REQUIRED
CURRENT_INPUT_REQUIRED
DO_NOT_INFER
```

不明をゼロ・中立・安全へ変換する一律の規則は設けていない。

---

# 8. G1 — 管理の検討対象範囲

## 8.1 結果を見る前に確定した規則

G1の最初の分類規則は、実際の分類結果の内訳を見る前に凍結した。

```text
mapped_open_grassland_area_m2 > 0
    -> PASS_PUBLIC

mapped_open_grassland_area_m2 == 0
and mapped_state_unknown_fraction > 0
    -> UNRESOLVED

mapped_open_grassland_area_m2 == 0
and mapped_state_unknown_fraction == 0
    -> NOT_APPLICABLE
```

`> 0` は管理の優先度を決めるしきい値ではない。公開地図上に面積がゼロでない開放・半自然草原の候補が存在するかという存在判定である。

## 8.2 結果

```text
PASS_PUBLIC      = 188 / 193 = 97.4093%
UNRESOLVED       =   1 / 193 =  0.5181%
NOT_APPLICABLE   =   4 / 193 =  2.0725%
```

したがって、公開空間情報だけでも、193の計画単位の大部分について半自然草原の管理を検討する範囲を定義できた。

これは、

```text
どこで野焼きすべきか
どこで放牧すべきか
どこで刈取りすべきか
```

を示す結果ではない。

G1が示すのは、**管理判断を検討する空間的な対象範囲**だけである。

リポジトリ版では、G1の地図を次のファイルに保存する。

`doc/figures/NAP002_G1_MANAGEMENT_REVIEW_SCOPE_MAP.svg`

## 8.3 計画単位189を結果に合わせて変更しなかった理由

最初の分類後に行った診断で、計画単位189の不明とされた部分は、実質的に分類不能な植生ではなく、浮動小数点計算で生じたごく小さな面積の残差のみであることが分かった。

しかし最初に定めた規則は結果を見る前に凍結していたため、Study 1は189を後から `NOT_APPLICABLE` へ変更しなかった。

これは、小さな数値残差を生態学的に重要視したという意味ではない。

むしろ、

> **最初の判定結果と、その後に行った診断を分離し、結果を見た後で規則を都合よく変更しない**

という結果に合わせて規則を変更しない原則を優先した。

---

# 9. G2–G5 — 生態学的な判定条件

Tier Eは、G1で `NOT_APPLICABLE` となった4単位を除く189単位、13種類の候補行動、9種類の判断に使う保全対象について構築した。

```text
189 × 13 × 9 = 22,113件
```

## 9.1 G2 — 保全対象との関連性

```text
PASS_PUBLIC          =  4,888
LOCAL_INPUT_REQUIRED = 14,742
UNRESOLVED           =     26
NOT_APPLICABLE       =  2,457
```

公開植生情報から得た状態から、T2の植生構成・遷移とT4の開放草原の構造については広い範囲での関連性を判断できる。

一方、特定の群集、希少種や保全上優先する種、草原に依存する動物等のT1/T3/T5については、計画単位ごとの地域における関連性を公開情報から確定しない。

ここでも、

```text
public no-record
!=
absence
```

を保持した。

## 9.2 G3 — 管理への応答を示す証拠

```text
SUPPORTED_SOURCE_LOCAL =  5,670
UNRESOLVED              = 15,687
DO_NOT_INFER            =    756
```

5,670件の記録では出典に基づく管理への応答の証拠が存在した。

しかしこれは、

```text
元の調査地点で管理への応答が観察された
```

ことを意味するだけで、

```text
この計画単位でも同じ応答が期待できる
```

ことを意味しない。

## 9.3 G4 — 管理への応答を別の場所へ適用できるか

```text
DO_NOT_INFER    =  5,670
NOT_APPLICABLE = 16,443
PASS_PUBLIC     =      0
```

Study 1の最も重要な境界の一つである。

G3で出典によって裏づけられた5,670件の記録は、**すべてG4で計画単位への適用を禁止された。**

つまり、

```text
source-local/source-relative response
!=
planning-unit response
```

というNAP-001の境界をそのまま保持した。

G3で証拠がないデータ行でG4が `NOT_APPLICABLE` なのは、別の場所への適用に関する問題が解決したという意味ではない。別の場所への適用を検討する前に、適用する元の調査地点での応答自体がないためである。

## 9.4 G5 — 悪影響や競合を防ぐ条件

```text
CONDITIONAL    =  1,323
UNRESOLVED     =  2,079
NOT_APPLICABLE = 18,711
```

G5は、保全対象ごとに異なる悪影響・競合の兆候と明示的な防止条件を保持する。

たとえば、管理の時期や強さが特定の保全対象に対して競合する場合があっても、それを1つの平均的な利益を表す点数で相殺しない。

---

# 10. 13種類の候補行動ごとの判断を妨げる要因

Study 1では、候補行動を「推奨候補」ではなく、検討対象となる管理行為の類型として扱う。

以下の数値は**証拠の範囲と判断を妨げる要因の構造**であり、管理行為の順位付けではない。

| 候補行動 | G3 証拠あり | G3 未解決 | G3 状況のみ | G4 転用の検証が必要 | G5 条件付き | G5 未解決 | G7 | G8 |
|---|---:|---:|---:|---:|---:|---:|---|---|
| 放牧を伴わない野焼き | 5 | 3 | 1 | 5 | 0 | 1 | LOCAL_INPUT_REQUIRED | CURRENT_INPUT_REQUIRED |
| 野焼きと低強度の放牧 | 3 | 6 | 0 | 3 | 0 | 1 | LOCAL_INPUT_REQUIRED | CURRENT_INPUT_REQUIRED |
| 野焼きと慣行的な放牧 | 3 | 6 | 0 | 3 | 0 | 1 | LOCAL_INPUT_REQUIRED | CURRENT_INPUT_REQUIRED |
| 野焼きと高強度の放牧 | 3 | 6 | 0 | 3 | 1 | 1 | LOCAL_INPUT_REQUIRED | CURRENT_INPUT_REQUIRED |
| 7月の刈取り | 3 | 6 | 0 | 3 | 2 | 0 | LOCAL_INPUT_REQUIRED | CURRENT_INPUT_REQUIRED |
| 9月の刈取り | 3 | 6 | 0 | 3 | 1 | 1 | LOCAL_INPUT_REQUIRED | CURRENT_INPUT_REQUIRED |
| 7月と9月の刈取り | 3 | 6 | 0 | 3 | 3 | 0 | LOCAL_INPUT_REQUIRED | CURRENT_INPUT_REQUIRED |
| 2年に1回の9月の刈取り | 2 | 7 | 0 | 2 | 0 | 1 | LOCAL_INPUT_REQUIRED | CURRENT_INPUT_REQUIRED |
| 野焼きと強度が未確定の放牧 | 0 | 8 | 1 | 0 | 0 | 1 | UNRESOLVED | CURRENT_INPUT_REQUIRED |
| 野焼きの記録がない強度未確定の放牧 | 0 | 8 | 1 | 0 | 0 | 1 | UNRESOLVED | CURRENT_INPUT_REQUIRED |
| 内容が未確定の積極的草原管理 | 2 | 7 | 0 | 2 | 0 | 1 | UNRESOLVED | NOT_APPLICABLE |
| 管理の停止と放棄後の変化 | 3 | 6 | 0 | 3 | 0 | 1 | NOT_APPLICABLE | NOT_APPLICABLE |
| 野焼き・放牧の記録がない状態 | 0 | 8 | 1 | 0 | 0 | 1 | UNRESOLVED | NOT_APPLICABLE |

すべての候補行動について、G1で除外されなかった計画単位のG6は `LOCAL_INPUT_REQUIRED` である。

また、出典で確認された保全対象数が多い候補行動を「より良い」「より推奨される」と解釈してはならない。たとえば野焼きのみは13種類の候補行動の中で出典で確認された証拠の範囲が最も広いが、その5種類の保全対象はすべてG4で、別の場所への適用に関する障壁に達する。

---

# 11. G6–G8 — 管理行為を取り巻く条件

Tier Aは193の計画単位 × 13種類の候補行動で構築した。

```text
193 × 13 = 2,509件
```

## 11.1 Tier AのG1判定の内訳

```text
PASS_PUBLIC    = 2,444  (= 188 × 13)
UNRESOLVED     =    13  (= 1 × 13)
NOT_APPLICABLE =   52  (= 4 × 13)
```

## 11.2 G6 — 地域で管理を実行できるか

```text
LOCAL_INPUT_REQUIRED = 2,457
NOT_APPLICABLE       =    52
PASS_PUBLIC          =     0
```

G6が必要とするのは、候補行動によって、

- 管理行為の内容
- 現地へのアクセス
- 必要な設備
- 管理上の権限と組織での実行可能性

等である。

公開された地域情報から、計画単位ごとの実行可能性を補完しなかった。

## 11.3 G7 — 資源と対応能力

```text
LOCAL_INPUT_REQUIRED = 1,512
UNRESOLVED           =   756
NOT_APPLICABLE       =   241
PASS_PUBLIC          =     0
```

人員、労働、家畜、機械、予算、組織の対応能力等を、地域全体の証拠から計画単位へ自動転移しない。

## 11.4 G8 — 現時点の運用条件

```text
CURRENT_INPUT_REQUIRED = 1,890
NOT_APPLICABLE         =   619
PASS_PUBLIC            =     0
```

特に現地での管理行為では、過去の公開資料では代替できない現時点を示す時刻付きの情報がある。

野焼きに関係する行為では、例として次を区別する。

```text
CURRENT_SITE_CONDITION
CURRENT_WEATHER_CONDITION
CURRENT_FUEL_OR_BIOMASS_CONDITION
CURRENT_SAFETY_ARRANGEMENT
CURRENT_PERMISSION_OR_RESTRICTION
```

Study 1はこれらを取得しておらず、当日の実施可否を判断する仕組みではない。

---

# 12. 判断規則の全体

Tier EとTier Aを統合した機械で読み取れる判断規則の全体は次の規模になった。

```text
Tier E — ECOLOGICAL_FEATURE = 22,113
Tier A — ACTION_CONTEXT     =  2,509
TOTAL                        = 24,622
```

判断規則全体の検証の結果は、

```text
records validated = 24,622
validation errors = 0
transfer_to_zone_contribution=true = 0
```

であった。

データ構造、候補行動の版、保全対象の識別情報、判断を妨げる要因の導出、必須入力と判定条件の対応、Tier AとTier Eの結び付き等を機械検査した。

---

# 13. 研究1の中心結果 — 実行を判断できる組合せは0件

G1で `NOT_APPLICABLE` ではない189単位について、13種類の候補行動を組み合わせると、

```text
189 × 13 = 2,457 planning-unit × candidate-action combinations
```

となる。

この2,457の組合せすべてで、

```text
ecological blocking feature count = 9 / 9
G6 local operational feasibility   = blocked
```

であった。

さらに、

```text
G4 PASS_PUBLIC = 0
G6 PASS_PUBLIC = 0
G7 PASS_PUBLIC = 0
G8 PASS_PUBLIC = 0
```

である。

したがって、

```text
public-only action-ready combinations = 0
```

と閉じた。

この結果を、

> すべての管理が不適切である

とは解釈しない。

正しい解釈は、

> **現在の公開証拠だけでは、計画単位ごとの管理行為の推奨に必要な条件が完全には閉じない。**

である。

---

# 14. 「情報不足」を次に必要な情報へ分解する

Study 1の実務的な進展は、単に

```text
more data are needed
```

と結論しなかった点にある。

不足を、性質の異なる情報へ分解した。

## 14.1 地域固有の生態学的な事実

```text
LOCAL_TARGET_RELEVANCE
LOCAL_SAFEGUARD_STATUS
```

これは、特定の保全対象がその計画単位に関係するか、地域の生態学的な悪影響を防ぐ条件がどうなっているかという現地の条件に関する事実である。

## 14.2 科学的な研究と検証

```text
RESPONSE_TRANSFER_VALIDATION
missing / unusable G3 management-response evidence
```

これは同日の現場の確認表で埋められる情報ではない。

元の調査地点で確認された応答を計画単位へ必要な精度で適用できることを正当化する新しい科学的検証が必要である。

## 14.3 地域固有の運用上の事実

```text
LOCAL_ACTION_SPECIFICATION
LOCAL_ACCESS_FEASIBILITY
LOCAL_INFRASTRUCTURE_FEASIBILITY
LOCAL_AUTHORITY_FEASIBILITY
```

候補となる管理方法の一部には、元の資料で定義されたものや、まだ内容が確定していない管理行為の要素が残る。したがって、管理名だけで「実行可能な管理行為の内容が確定している」と仮定しない。

## 14.4 地域の資源と対応能力

```text
LOCAL_RESOURCE_CAPACITY
```

地域に草原管理の歴史や支援制度があることと、特定計画単位で必要な人員・予算・家畜・機械・作業時間が確保できることは別問題である。

## 14.5 現時点で確認すべき事実

```text
CURRENT_SITE_CONDITION
CURRENT_WEATHER_CONDITION
CURRENT_FUEL_OR_BIOMASS_CONDITION
CURRENT_SAFETY_ARRANGEMENT
CURRENT_PERMISSION_OR_RESTRICTION
```

これらは過去の公開GISから推定して埋めるべきではない。

---

# 15. 最終的な実務表現 — WHERE / WHY / WHAT NEXT

Study 1の実務に示す主な成果は、一枚の管理行為の推奨地図ではなく、三つの役割を分けた構造である。

## WHERE — 管理の検討対象を示す地図

G1は、

> **どの計画単位を半自然草原の管理判断のレビュー対象に含めるか**

を示す。

## WHY — 判断を妨げる要因の一覧

候補行動とG2–G8の一覧は、

> **なぜその候補行動を現在の公開証拠だけでは選択できないのか**

を示す。

## WHAT NEXT — 次に必要な情報の確認表

確認表は、

> **その候補行動をさらに評価するなら、次に何を確認・取得・研究すべきか**

を示す。

この三部構造は、

```text
レビュー対象
判断不能理由
次に必要な情報
```

を分離する。

---

# 16. なぜ候補行動別の公開地図を13枚作らなかったのか

現在の公開情報のみから得た証拠では、同じ候補行動について、188のG1に合格した計画単位のG2–G8に関する判断を妨げる要因の内訳は同一である。

計画単位ごとの差を作るはずの情報、すなわち、

```text
local target occurrence
local safeguard status
validated response transfer
local action specification
local feasibility
local resources
current conditions
```

が、まさに未観測だからである。

この状態で13種類の候補行動別の地図を作ると、ほぼ同じG1で対象とされた範囲を異なる凡例で塗り直すことになる。

地図があることで管理行為ごとの空間的な違いが存在するように見える可能性があるため、Study 1はこれを**根拠のない見かけ上の空間的精密さ**として避けた。

「地図を作らない」という判断も、研究結果の一部である。

---

# 17. 実務での読み方

研究1の出力は、次の順序で読むことを想定する。

```text
1. G1の地図で計画単位を確認する。

2. NOT_APPLICABLEなら、
   現在の半自然草原の管理を検討する対象に含めない。

3. UNRESOLVEDなら、
   地図上の状態や関連性の不確実性を先に確認する。

4. PASS_PUBLICなら、
   候補行動を「承認済み」ではなく「検討対象」として扱う。

5. 判断を妨げる要因の一覧を読む。

6. 次に必要な情報の確認表で、
   地域・現時点の事実と科学的検証を区別する。

7. 情報不足を「条件を満たす」と読み替えない。
```

これにより、公開証拠から地域で次に行う判断作業への引き継ぎを明示できる。

---

# 18. 例 — 放牧を伴わない野焼き

G1が `PASS_PUBLIC` の計画単位で、

```text
CR_BURN_ONLY
Burning without grazing
```

をレビューするとする。

公開情報だけを用いた判断規則は概略として次を返す。

G1は検討対象か、G2～G5は生態学的証拠と転用の可否、G6～G8は実行に必要な地域・現時点の条件を示す。英大文字の値は正式な状態コードである。

```text
G1  management-review scope       PASS_PUBLIC

G2  target relevance              T2/T4はbroad public relevance
                                   T1/T3/T5はlocal relevanceが必要

G3  response evidence             5 / 9 source-supported
                                   3 / 9 unresolved
                                   1 / 9 context-only

G4  response transfer             5 source-supported featuresすべて
                                   transfer validationが必要

G5  safeguard/conflict            safeguard unresolved

G6  local feasibility             local input required

G7  resource capacity             local input required

G8  current conditions            current input required
```

このとき正しい出力は、

> **候補行動を選ぶ判断はまだできない。地域・現時点の条件の確認と、管理への応答を別の場所に適用できるかの科学的検証が必要である。**

である。

誤った出力は、

```text
野焼きを推奨する
野焼きが最適である
この計画単位では野焼きすべきである
野焼きは安全である
G1の合格は野焼きの許可を意味する
```

である。

---

# 19. 架空の条件を用いた判断手順の検証

## 19.1 なぜ架空の検証例を使ったのか

研究1では実際の地域固有・現時点の入力を取得していない。

それでも、判断の仕組みが、地域固有・現時点の事実に関する不足を埋めた後にどのように振る舞うかを検証する必要があった。

そこで完全に架空の2つの想定条件を事前定義した。

```text
S1  Burning without grazing
S2  July + September mowing
```

実在する計画単位のID、実際の天候、許可、保全対象の分布、安全に関する状態等は使用していない。

## 19.2 現場情報の充足と科学的証拠を分ける

架空の想定条件では、許可された地域固有・現時点の事実に関する必須条件を「すべて満たされた」と仮定した。

しかし、次は仮定しなかった。

```text
missing G3 management-response evidence
G4 response transferability
```

これらを現場の確認項目として架空の条件で合格させると、科学的証拠の不足を現場入力で偽装することになるためである。

## 19.3 結果

```text
S1 burn-only             -> RESEARCH_EVIDENCE_REQUIRED
S2 July+September mowing -> RESEARCH_EVIDENCE_REQUIRED
```

野焼きのみでは、地域固有・現時点の事実をすべて満たした後も、G3の未解決・状況のみとG4の転用に関する障壁が残った。

7月と9月の刈取りでも、G3の未解決状態とG4の転用に関する障壁が残った。

この検証例は、次を明示する。

> **現場情報をすべて集めれば、自動的に管理行為の推奨へ到達するわけではない。地域固有・現時点の事実と、管理への応答を示す科学的証拠は別の情報階層である。**

---

# 20. 再現性と検証

## 20.1 機械による検証

Study 1は、会話内の手計算や手作業の地図分類だけで閉じていない。

GitHub Actions上で、リポジトリ内の確定済み入力から資料の作成と検証を再実行した。

主な実行結果は次のとおりである。

```text
31669720153  G2-G5 validation                 SUCCESS
31670157556  full G1-G8 engine                SUCCESS
31670617847  blocker presentation             SUCCESS
31671128589  synthetic conditional prototype  SUCCESS
```

架空の検証例を含む最新の成果物:

```text
artifact id = 9169736427
SHA-256 = 65b99e38df61fd5e00dfd8672dce7f39cfc349d5ec2931e1c437cabf403f9475
```

## 20.2 判断規則全体の検証

```text
records validated = 24,622
record tiers:
  ECOLOGICAL_FEATURE = 22,113
  ACTION_CONTEXT     =  2,509

error_count = 0
transfer_to_zone_contribution_true_count = 0
```

## 20.3 誤った解釈を想定した監査

研究1の結果を確定したときには、再現性だけでなく、以下の誤った処理や解釈の可能性を明示的に監査した。

```text
NAP-001 historical evidenceの書換え
unknown -> zero / neutral / safe
public no-record -> ecological absence
Q2/source-local -> Q3 planning-unit response promotion
G4の暗黙pass
weighted actionability score
hidden ecological roll-up
action ranking
management recommendation
action authorization
manual post-result recoloring
real local/current valuesの混入
restricted/private empirical dataの混入
```

最終監査は `PASS` で閉じた。

---

# 21. 本研究が支持すること

NAP-002 Study 1は、少なくとも以下を支持する。

1. 公開植生情報から半自然草原の管理を検討する範囲を計画単位ごとに再現可能に定義できる。
2. 管理判断を保全対象との関連性、管理への応答の証拠、別の場所への適用可能性、悪影響を防ぐ条件、実行可能性、対応能力、現時点の条件へ分解できる。
3. 元の調査で確認された証拠と計画単位への適用可能性を別の判定条件として保持できる。
4. 保全対象ごとの生態学的証拠を一つの管理行為の平均点へ潰さず保持できる。
5. 不明・不足している地域固有・現時点の事実を判断を妨げる要因として機械で読み取れる形に表現できる。
6. 「より多くのデータが必要」を具体的な必要な入力の種類へ分解できる。
7. 公開証拠で空間差がないところに、候補行動別の地図を人工的に作らない見せ方の規則を実装できる。
8. 地域固有・現時点の事実をすべて満たした後も科学的証拠の不足が残り得ることを架空の検証例で示せる。
9. 準備が整わなかった状態を、実務で次に何を確認するかへ接続できる。
10. NAP-001の別の場所への適用に関する限界を変更せずに、より実務的な意思決定支援の表現へ進める。

---

# 22. 本研究が支持しないこと

Study 1は以下を主張しない。

-  `PASS_PUBLIC` と判定された188単位で何らかの管理を実行すべきである
- 野焼き、放牧、刈取りのどれかが最適である
- 出典で確認された保全対象数が多い候補行動ほど望ましい
- `NOT_APPLICABLE` が生態学的に安全を意味する
- G1 `PASS_PUBLIC` が管理行為の承認を意味する
- 公開記録がないことが保全対象の不在を意味する
- 地域全体の対応能力を示す資料が各計画単位の対応能力を意味する
- 過去の資料が現時点の気象・安全・許可情報を代替できる
- 元の調査地点に限った応答を計画単位へ直接転移できる
- 13種類の候補行動の順位を提示した
- 管理行為の適性を示す地図を構築した
- 最適な管理配置を構築した
- 当日の野焼き実施可否を判断する仕組みを構築した
- 実務者の判断の質を改善した
- 新しい一般的意思決定科学の理論を発明した

特に、**実務者にとっての有益さは研究1では測定していない。**

---

# 23. 実務的含意

NAP-002 Study 1の重要な実務的含意は、意思決定支援の仕組みが必ずしも「推奨」を返す必要はないことである。

不確実な人の利用が続く景観では、役立つ出力が、

```text
ここは管理の検討対象である
この候補行動にはこの証拠がある
元の調査地点で得た応答をこの場所へ適用する根拠がない
この悪影響を防ぐ条件が未確認である
この地域固有の情報が必要である
現時点のこの条件を確認する必要がある
この点には現場確認ではなく新しい研究が必要である
```

という**どこまで判断できるかの明示**である場合がある。

これは「判断を先送りする」こととは異なる。

何が決められないかを理由別に分解すれば、

- 行政が確認すべき地域固有の事実
- 現場が当日に確認すべき条件
- 研究者が新たに検証すべき管理への応答を別の場所に適用できるか

を混同せずに次の作業へ接続できる。

---

# 24. 研究上の限界

## 24.1 公開情報だけで到達できる限界は「世界に情報がない」という意味ではない

Study 1が示すのは、凍結された公開情報だけから得た証拠で判断できる範囲の限界である。

利用に制限のある地域の資料や新たな現地調査、最新の現場情報に追加情報が存在する可能性を否定しない。

## 24.2 G1は検討対象を示し、生息環境の質を示す点数ではない

G1の `PASS_PUBLIC` は地図上に開放・半自然草原の候補が面積ゼロではない状態を意味する。

面積の大小、生息環境の質、管理優先度、保全対象の価値を表さない。

## 24.3 G2–G8の空間差の少なさは、現在利用できる証拠の限界を示す

188 G1に合格した計画単位で候補行動ごとのG2–G8の内訳が同じであることは、阿蘇の全計画単位が実質的に同じという意味ではない。

それらを区別する地域固有・現時点の事実が今回利用できた公開資料にないことを意味する。

## 24.4 管理への応答を別の場所へ適用できるかの検証は未実施である

G4 `PASS_PUBLIC = 0` はStudy 1の重要な結果である。

将来、結果を見る前に計画した別の場所への適用に関する検証研究によって一部が進む可能性はあるが、Study 1の歴史結果を後から書き換えるものではない。

## 24.5 実務者にとっての使いやすさや有効性は未評価

透明性のある判断を妨げる要因の一覧や不確実性の表現が、人間の意思決定を実際に改善するとは自動的に言えない。

表示が複雑すぎる、誤読される、必要な情報が現場の手順に合わない等の可能性がある。

これを検証するには、別の事前計画による研究2が必要である。

## 24.6 研究1は情報の価値（VoI）を正式に計算していない

どの情報不足を解消する価値が高いかという順位は、目的・測定する結果・管理への応答のモデルが十分に閉じていない状態では正当化できない。

必須入力の欄の数を「優先度」へ変換してはならない。

---

# 25. 第三者資料・データの取扱い

この公開報告書は単体公開を想定し、第三者著作物や慎重な扱いを要する地域の資料の再配布を必要最小限にしている。

本レポートには、

- 原著論文PDFそのもの
- 原著論文の図表画像
- 大量な逐語引用
- 利用に制限のある地域の元データ
- 慎重な扱いを要する希少種の座標
- 個人・生産者識別情報
- 実際の現時点の運用・安全情報

を収録していない。

本文では、前身NAP-001が凍結した元の調査から得られた証拠の構造と、NAP-002が実装した意思決定支援への変換を要約している。

研究内部の再現性・監査資料はリポジトリに保存するが、それらを読まなくても本文の主要結論は理解できるようにした。

---

# 26. Study 2との境界

Study 1の完了後に最も自然な後続研究の一つは、

> **NAP-002 Study 2 — 実務者・行政担当者による意思決定支援の検証**

である。

Study 2が扱うべき問いは、Study 1とは異なる。

Study 1:

> 証拠制約を保持しながら、対象範囲・判断を妨げる要因・次に必要な情報へ変換できるか。

Study 2:

> その表現は、実際の行政担当者・草原管理者・意思決定者に理解可能で、実務手順に適合し、判断の透明性・一貫性・適切な情報取得に寄与するか。

Study 2が肯定的な結果でも否定的な結果でも、Study 1の正式結果は変更しない。

たとえばStudy 2で、

```text
情報量が多すぎる
matrixより別のUIが理解しやすい
required-input terminologyが現場用語と合わない
scope mapは有用だがblocker matrixは使いにくい
```

等が示された場合、それはStudy 1の失敗ではなく、**科学的な慎重さを守る仕組みと人が使う画面の間に、新たな設計上の問題がある**ことを示す独立結果になる。

---

# 27. その他の将来研究

Study 1を再解析して管理行為を直接推奨する地図を作るのではなく、必要に応じて結果を見る前に計画する独立研究として進める。

## 27.1 管理への応答を別の場所へ適用できるかの検証

G4を直接扱う研究である。

必要となり得るのは、

- 実際に行う管理方法の定義
- 元の調査地点と適用先の条件の比較可能性
- 保全対象に関係する測定結果
- 条件による効果の変化
- 繰り返しの観測
- 別の場所への適用に関する規則の事前定義
- 別の場所や別の時点での検証

等である。

## 27.2 将来のStage A — 利用に制限のある地域の実測データ

申請・許可が必要な資料や地域固有の運用情報を用いる可能性がある。

ただし資料の利用に制限があること自体は科学的妥当性を保証しない。新しい研究計画と資料の適格性の点検が必要である。

## 27.3 将来のStage B — 事前に計画した現地調査と継続観測

管理への応答、因果関係、継続観測に関する不足を新たに事前計画した研究設計で測定する。

Study 1の判断を妨げる要因の構造は、どの情報が判断に関係するかを整理する入力にはなり得るが、継続観測の設計自体の新規性は主張しない。

## 27.4 運用手順の試験

実際の判断時点における地域固有・現時点の入力規則を別途設計し、許可・安全・気象等の時点によって変わる情報を扱う可能性がある。

これはStudy 1の公開情報だけを用いた判断規則とは別の仕組みとして扱う必要がある。

---

# 28. 再現性識別子

研究1の主要な確定済み識別情報を以下にまとめる。

## 計画単位の形状

```text
count = 193
SHA-256 = 46ef4dd475ec7645d78130722e8ddfcae9f51c6244ce95dc22ea9f7dcaa6609d
```

## 植生構成

```text
rows = 1426
SHA-256 = ac01c133cf8d366dc02d0da2b8e1ff1334e5b997f31b74553cd60f0afc4b5413
```

## 開放草原の状態

```text
rows = 193
SHA-256 = c6aee6d304e223189289e8b2f8bcbf5f42042b037304741365091eea77a4a93c
```

## 判断規則の全体

```text
Tier E records = 22,113
Tier A records =  2,509
TOTAL          = 24,622
validation errors = 0
```

## 架空の検証例を含む最新のCI成果物

```text
artifact id = 9169736427
SHA-256 = 65b99e38df61fd5e00dfd8672dce7f39cfc349d5ec2931e1c437cabf403f9475
```

## 公開報告書の来歴

```text
repository = nkkmd/natural-area-planning
study-state snapshot commit = 93a6ab91c0dbcbac2dfa32c4ff11700f745770fc
study date = 2026-08-13 JST
```

---

# 29. リポジトリ内の主要な再現性資料

このレポート単体で主要結論を理解できるが、出典と処理の履歴、機械的な監査はリポジトリで追跡できる。

主要資料:

```text
doc/checkpoints/2026-08-13-nap002-study1-formal-closure.md
doc/nap002/NAP002_STUDY1_REPRODUCIBILITY_ADVERSARIAL_AUDIT.md
analysis/nap002/study1_reproducibility_audit.json

doc/nap002/NAP002_DECISION_GATE_SCHEMA_PROTOCOL.md
analysis/nap002/decision_record_schema.json
analysis/nap002/validate_decision_records.py

doc/nap002/NAP002_G1_MANAGEMENT_REVIEW_SCOPE_PROTOCOL.md
analysis/nap002/g1_management_review_scope_states.csv

doc/nap002/NAP002_G2_G5_ECOLOGICAL_GATE_PROTOCOL.md
analysis/nap002/decision_blocker_action_matrix.csv

doc/nap002/NAP002_G6_G8_ACTION_CONTEXT_PROTOCOL.md
analysis/nap002/required_input_action_checklist.csv

doc/nap002/NAP002_SYNTHETIC_CONDITIONAL_DECISION_PROTOCOL.md
analysis/nap002/synthetic/conditional_decision_results.csv
```

---

# 30. 結論

Natural Area Planning / NAP-002 Study 1は、NAP-001が到達した公開情報だけから得た証拠の限界を、根拠のない管理行為の推奨で覆い隠すのではなく、**実務で次に何を確認すべきかを示す意思決定支援の仕組みへ変換できること**を示した。

公開空間情報だけでも、

```text
188 / 193 planning units
```

について管理の検討対象範囲を定義できた。

しかし、24,622件からなる完全判断規則の全体では、

```text
G4 PASS_PUBLIC = 0
G6 PASS_PUBLIC = 0
G7 PASS_PUBLIC = 0
G8 PASS_PUBLIC = 0
public-only action-ready combinations = 0
```

であった。

この結果は、公開情報だけを用いた意思決定支援が無意味であることを示さない。

むしろ、

```text
どこをレビューするか
何が判断を止めているか
どの地域固有の事実が必要か
現時点のどの条件を確認すべきか
どこは新しい科学的検証が必要か
```

を分離して提示できる。

Study 1の最終到達点は、次の一文に要約できる。

> **証拠が候補行動の選択まで届かないとき、意思決定支援はその不足を隠して推奨を作るのではなく、どこまで分かっており、何が判断を止め、何を次に確認すべきかを明示できる。**

NAP-001が「証拠が止まるところで最適化計算を止める」研究だったとすれば、NAP-002 Study 1は、**その停止点を実務上の行き詰まりにせず、次の確認・研究・意思決定へ接続する方法を実装した研究**である。

---

# 用語

**計画単位（planning unit）**  
空間的な評価・計画の単位。本研究ではNAP-001から継承した193単位を固定した。

**候補行動・候補管理方法（candidate action / candidate management regime）**  
判断のために検討する管理行為。候補に含まれること自体は、推奨・安全・許可を意味しない。

**判定条件（decision gate）**  
候補行動を選ぶ前に個別に確認する条件と証拠。研究1ではG1–G8を使用した。

**判断を妨げる要因（decision blocker）**  
現在の情報では候補行動を選べない理由。研究1では `CONDITIONAL`、`UNRESOLVED`、`LOCAL_INPUT_REQUIRED`、`CURRENT_INPUT_REQUIRED`、`DO_NOT_INFER` を判断を止める状態とした。

**次に必要な情報（information need）**  
不足を解消するための追加情報。地域固有の事実、現時点の事実、新たな科学的検証を区別する。

**管理への応答を別の場所へ適用できるか**  
元の調査地点で観察された応答を、必要な精度で別の計画対象地にも適用できるかという問題。

**SUPPORTED_SOURCE_LOCAL**  
G3で元の調査地点における管理への応答の証拠がある状態。計画単位でも応答が成立することは意味しない。

**DO_NOT_INFER**  
現在の証拠から言える範囲を超える推論を禁止する状態。

**根拠のない見かけ上の精密さ（pseudo-precision）**  
証拠が支えない細かな数値・順位・空間差を、計算や図示によって精密に見せること。

---

# 参考文献・関連する先行研究

NAP-002 Study 1は、次に挙げる意思決定科学、不確実性、意思決定支援に関する先行研究を踏まえている。これら一般的な方法そのものを新たに発明したとは主張しない。

- Martin et al. (2009). Structured decision making / decision-threshold literature. DOI: `10.1890/08-0255.1`
- Robinson et al. (2016). Large-scale wildlife Structured Decision Making application. DOI: `10.1002/ecs2.1613`
- Schwartz et al. (2017). Conservation decision-support frameworks. DOI: `10.1111/conl.12385`
- Hemming et al. (2022). Decision science in conservation. DOI: `10.1111/cobi.13868`
- Lyons et al. (2008). Decision-driven monitoring / Structured Decision Making. Identifier: `USGS_5224905`
- Williams & Johnson (2015). Value of Information in natural-resource management. DOI: `10.1002/wsb.575`
- Runge, Converse & Lyons (2011). Value of Information / identifying decision-relevant uncertainty. DOI: `10.1016/j.biocon.2010.12.020`
- Lawson et al. (2022). Qualitative Value of Information. DOI: `10.1111/csp2.12732`
- Regan et al. (2005). Robust conservation decision making under severe uncertainty. DOI: `10.1890/03-5419`
- Sierra-Altamiranda et al. (2020). Spatial conservation planning under uncertainty. DOI: `10.1016/j.ecolmodel.2020.109016`
- Cattarino (2018). Multi-action spatial management prioritization under response uncertainty. DOI: `10.1111/1365-2664.13147`
- Moore et al. (2021). Conservation resource allocation among multiple threats/actions. DOI: `10.1111/cobi.13748`
- Aerts, Clarke & Keuper (2003). Spatial uncertainty visualization in decision support. DOI: `10.1559/152304003100011180`
- Gallo & Goodchild (2012). Mapping uncertainty in conservation assessment/planning. DOI: `10.1080/08941920.2011.578119`
- Korporaal, Ruginski & Fabrikant (2020). Effects of uncertainty visualization on map-based decisions. DOI: `10.3389/fcomp.2020.00032`
- Arciniegas, Janssen & Rietveld (2013). Collaborative map-based spatial decision support evaluation. DOI: `10.1016/j.envsoft.2012.02.021`

関連する先行報告書:

- Natural Area Planning / NAP-001 — 公開研究報告書 (2026), `doc/publication/NAP001_PUBLIC_RESEARCH_REPORT.md`

---

## 引用時の推奨表記

本レポートを引用する場合は、少なくとも次の情報を含めることを推奨する。

```text
Natural Area Planning / NAP-002 Study 1 (2026).
Public Research Report: 公開情報だけで阿蘇半自然草原の管理判断をどこまで支援できるか
— 「何をすべきか」を断定せず、「何が判断を止めているか」を明示する —.
Version 1.0.2, 日本語表現改訂 2026-09-28（科学的結果は2026-08-13確定）。
Study snapshot: nkkmd/natural-area-planning @ 93a6ab91c0dbcbac2dfa32c4ff11700f745770fc.
```

この `Study snapshot` はStudy 1の凍結された科学的状態を指し、その後のpublication packagingやeditorial-only commitを指すものではない。

著者名、所属、DOI、恒久公開URL等が後日正式に付与された場合は、それらを優先して引用情報へ追加する。

---

**研究1の正式な状態：完了・結果確定済み。v1.0.2では科学的結果を変更していない。**