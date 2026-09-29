# Natural Area Planning / NAP-002 Study 2A — 公開研究報告書

**人間参加者を用いずに意思決定支援表現をどこまで事前検証できるか**  
**― 追跡可能性・誤った推論への耐性・情報量の一致・公開行政文書との整合性を検証する ―**

- レポート版: **v1.0.1**
- 日本語表現の改訂: **2026-09-28（科学的結果・正式判定は変更なし）**
- 作成日: **2026-08-14 JST**
- 研究プロジェクト: **Natural Area Planning / NAP-002 Study 2A**
- 研究状態: **COMPLETE / FROZEN — 人間参加者を用いない意思決定支援の事前検証**
- 正式結果: **INDETERMINATE（判定不能）**
- 研究状態スナップショット: `nkkmd/natural-area-planning` / コミット `db83cae09e9b84a6b9deab46d87af6c36e9cfa49`
- 本文の性格: **単体公開用研究レポート**
- 編集整備: **2026-08-14：公開報告書の体裁を調整。科学的結果は変更なし**

> この文書は、元のGitHubリポジトリ、内部の研究計画、進捗記録、CSV、JSON、監査の成果物を参照しなくても、NAP-002 Study 2Aの背景、研究質問、設計、事前凍結、正式評価、主要結果、限界、再現性、Study 2Bとの境界、今後の研究課題を理解できるように構成している。GitHub外へこのファイル単体をコピーして公開しても、研究レポートとして成立することを意図している。

---

## 初めて読む方へ

この報告書は、研究02で作った意思決定支援の表現を、実在の人に試してもらう前に点検した研究です。追跡可能性などのA1–A4は `PASS` でしたが、公開文書を対象とするA5は予定した検索結果100件のうち98件しか得られず、正式判定は `INDETERMINATE`（判定不能）です。実務者が理解しやすいか、実務で使えるかはこの研究からは判断できません。

本文の研究ID、正式判定コード、数値、出典識別子は、研究結果と照合できるよう原表記を残しています。

# 要旨

先行するNAP-002 Study 1では、阿蘇半自然草原の193の計画単位について、公開証拠の限界を守りながら、管理の検討対象、判断を妨げる要因、次に必要な情報を示す意思決定支援の表現を構築した。管理の検討対象と判定された計画単位は188件だった。一方、元の調査地点で確認した応答を別の場所に適用できるか、地域で実行できるか、必要な資源があるか、現時点の条件を満たすかについては、公開情報だけで「条件を満たす」と判定できたものはなかった。管理行為の推奨や最適配置は示していない。

しかし、証拠の限界を正しく表現できることと、実務者がその表現を理解し、実務の手順で使えることは別の問いである。そこで研究2を、人間参加者を使わずに表現そのものを点検する研究2Aと、将来、実在の実務者によって検証する研究2Bに分けた。この区分は結果を見る前に決めており、研究2Aでは人間参加者を募集・調査していない。

正式評価の前に、16の個別の事実（うち重要な事実15）、誤った推論を防ぐべき12類型、誤読を想定した36事例、同じ情報を含む比較対象、公開文書の検索語10本、分析と再現性に関する規則を資料として確定した。評価は、他の条件の合格で不合格を相殺できない五つの判定条件A1–A5で行った。

```text
A1 traceability                    PASS
A2 evidence-boundary cues         PASS
A3 baseline equivalence           PASS
A4 adversarial consistency        PASS
A5 documentary compatibility      INDETERMINATE

OVERALL                            INDETERMINATE
```

A1では重要な事実15/15を研究1の確定済み資料と規則に追跡でき、根拠のない仮定は0件だった。A2では12/12類型について証拠が許さない解釈を明示的に退けた。A3では両方の提示方法が同じ16の事実を含み、重要な事実の欠落・追加・状態変更は0件だった。A4では36/36事例の想定した解釈が内部的に整合し、矛盾や架空の生態学的事実を必要とする事例はなかった。

A5では、阿蘇・熊本・環境省などの公開文書との用語と実務手順の整合性を調べた。事前に10件の検索語それぞれについて上位10件、計100順位を確認すると決めていたが、Q06とQ07は各9件しか返らず、確認できたのは98/100順位だった。取得した適格な文書では、管理や検討の計画、許可、安全と現時点の確認、資源、継続観測、出典管理に関する領域が確認され、研究1の証拠の限界を覆す重大な意味上の対立は見られなかった。それでも不足した2順位を結果に合わせて別の検索で補うことは、事前の停止条件を変えるため行わなかった。

このためA5と研究全体の正式判定はINDETERMINATE（判定不能）である。実務との不適合が確認されたという意味ではなく、事前に定めた検索を完全には実行できず、正式な適合判定を確定できなかったという結果である。

研究2Aは、人間参加者の理解度や使いやすさ、実際の判断の質、生態学的効果、管理効果を別の場所に適用できるか、管理の推奨、安全、許可、優先順位、最適性を実証していない。実在の人による検証は研究2Bとして未着手のままである。

本研究は、人間を対象とした検証の代わりを作ったものではない。**実在の人に試す前に、表現そのものについて確認できる条件と、人間参加者がいなければ判断できない条件を区別した**ことが成果である。

---

# 1. 研究の背景

## 1.1 NAP-001が示した公開証拠だけで到達できる限界

Natural Area Planning / NAP-001は、阿蘇半自然草原について、公開情報だけから管理方法を明示した体系的な保全計画をどこまで科学的に構築できるかを検討した。

NAP-001では、193の計画単位、13種類の候補となる管理方法、保全対象別の保全計画の枠組み、公開GIS・植生データから得た基礎的な状態、元の調査地点で得た管理への応答の証拠、計画ソフトへの構造上の対応付けまでを構築した。

しかし、正式な空間配置に必要な計画単位ごとの管理への応答を示す係数や応答を別の場所へ適用できるという検証結果は構築できなかった。

最終的な公開情報だけで到達できる範囲の限界は次である。

```text
Q3 planning-response features         = 0
Q4 local management × context models = 0
coefficient-ready regimes             = 0
zone contribution rows                = 0
formal optimizer authorized           = false
```

NAP-001の中心的判断は、最適化ソフトが数値を必要とすることを理由に、証拠が正当化しない係数を作らないことだった。

## 1.2 NAP-002 Study 1が作った意思決定支援の表現

NAP-002 Study 1は、この準備が整わなかったという結果を救済して計画用の係数を補う研究ではない。研究質問を一段上流へ移し、証拠限界そのものを意思決定支援へ変換した。

Study 1の正式な回答は `YES` であり、最終的な実務表現は次の三部構造となった。

```text
WHERE
  Management Review Scope Map

WHY
  Candidate Action × Decision-Gate Blocker Matrix

WHAT NEXT
  Candidate Action × Required-Input Checklist
```

Study 1は、管理の検討対象範囲、判断を妨げる要因、次に必要な情報を機械追跡可能に表現できることを示した。一方で、管理方法の推奨、管理行為の順位付け、管理行為の承認、計画単位ごとの生態学的応答、G4に関する検証、最適化計算は支持しなかった。

## 1.3 「科学的に正しい表現」と「人間に有用な表現」は同じではない

Study 1の表現が科学的境界を保持していることは、そのまま人にとっての使いやすさを意味しない。

たとえば、次の可能性はStudy 1だけでは評価できない。

```text
情報量が多すぎて理解しにくい
G1 PASSをaction approvalと誤読する
G5 NOT_APPLICABLEをsafeと誤読する
required-input数をpriorityと誤読する
WHERE / WHY / WHAT NEXTの分離がworkflowに合わない
terminologyが現場用語と一致しない
```

この問題を正式に評価するには、実在する実務者や行政担当者に参加してもらう研究が必要である。

しかし、人間参加者の確保が難しい状況で、それをLLMや架空の利用者で置き換えて「実在の人による検証済み」とすることは科学的に不適切である。

そこで、人間参加者から得た証拠を必要としない表現そのものの事前検証と、人間参加者から得た証拠を必要とする実務者による検証を別研究へ分離した。

---

# 2. Study 2A / 2Bの分離

2026-08-14、NAP-002 Study 2は次の2研究へ結果を見る前に分離された。

```text
NAP-002 Study 2A
  Non-Participant Decision-Support Pre-Validation
  人間参加者なしでrepresentation-level prerequisiteを評価

NAP-002 Study 2B
  Practitioner / Administrative Decision-Support Validation
  実在人物を対象にhuman comprehension / usability / workflow fitを評価
```

この分離は人間参加者から得たデータを見た後の結果に合わせた設計変更ではない。Study 2Bの人間参加者データは0であり、連絡、募集、同意取得、調査票、面接、参加者が行う作業、参加者単位の分析は開始していない。

既存の人間参加者による検証の研究計画はStudy 2Bとして将来へ保持し、Study 2Aは結果を見る前に計画した別の研究として開始した。

重要な関係は次である。

```text
Study 2A COMPLETE
!=
Study 2B COMPLETE

non-participant evidence
!=
human-participant evidence
```

---

# 3. 研究対象

Study 2Aの主たる研究対象は、阿蘇の土地そのものでも、実務者の集団でもない。

研究対象は、NAP-002 Study 1で凍結された**意思決定支援の表現**である。

対象となる表現は、少なくとも以下から構成される。

```text
G1 management-review scope
G2 target relevance
G3 management-response evidence
G4 response transferability
G5 ecological safeguard / conflict
G6 local operational feasibility
G7 resource / capacity
G8 current operational conditions

WHERE / WHY / WHAT NEXT presentation
required-input architecture
evidence-boundary interpretation rules
```

阿蘇・熊本の公開行政・運用文書はA5の公開文書との整合性を調べる監査に使用したが、それらの文書に記載された個人を研究参加者として扱っていない。

---

# 4. 研究目的と中心的研究質問

Study 2Aの中心的研究質問は次である。

> **NAP-002 Study 1で凍結された意思決定支援表現は、将来の実在の人による検証へ進む前に必要となる非参加者型の条件、すなわち追跡可能性、証拠が許す範囲の明示、比較対象との情報量の一致、誤読を想定した論理的一貫性、公開文書の用語・実務手順との整合性を満たすか。**

ここで重要なのは、これらの条件が実在の人による検証の**必要条件になり得るが十分条件ではない**ことである。

研究2Aの結果が肯定的でも、

```text
実務者が理解できる
実務者にとって使いやすい
実務手順に適合する
実際の判断の質が改善する
```

とは結論しない。

---

# 5. 先行研究との関係と新規性を主張できる範囲

## 5.1 意思決定支援の評価自体は新しくない

自然資源管理・保全では、Structured Decision Making、adaptive management、Value of Information、robust decision making、uncertainty visualization、map-based decision support、participatory spatial decision support等に広い先行研究がある。

Study 2Aは、次の一般概念を新規発明として主張しない。

```text
decision representationを評価すること
uncertainty / evidence boundaryを明示すること
baseline comparisonを設けること
adversarial caseで誤解釈可能性を点検すること
public workflow terminologyとの対応を見ること
human-facing interfaceを別途評価する必要性
```

## 5.2 Study 2Aが扱う固有の問題

Study 2Aの固有性は、一般的な使いやすさの評価手法の発明ではなく、**NAP-002 Study 1の凍結された証拠から言える範囲を明示した表現について、人間参加者を使わずに検証可能な範囲を結果を見る前に分離し、その結果を実在の人による検証結果に読み替えないための規則を実装したこと**にある。

## 5.3 LLMを人間の代役にしない

言語モデルは、架空の解釈者や誤読を試す道具として探索的に使用する余地を残したが、研究2Aの正式判定には使用しなかった。

```text
LLM behavior
!=
practitioner behavior

AI agreement
!=
human usability
```

この区別を変更しない条件として保持した。

---

# 6. 結果に応じて規則を変えない研究設計

Study 2Aの研究設計の記録は次の研究の識別情報で凍結した。

```text
studyId = NAP002-STUDY2A-NONPARTICIPANT-PREVALIDATION-2026-08-14-v1
humanParticipantStudy = false
study2BStatus = DEFERRED_NOT_STARTED
llmFormalInferenceAuthorized = false
```

正式判定の区分は次の4つに限定した。

```text
READY_FOR_HUMAN_VALIDATION
NOT_READY_FOR_HUMAN_VALIDATION
MIXED
INDETERMINATE
```

正式評価は、検証に使う資料、想定する解釈の正解、公開文書の検索方法と停止条件、分析の構造、再現性の確認資料を作成・確定するまで実施しなかった。

---

# 7. 正式評価前に確定したM1–M9の資料

Study 2Aでは、結果を見ながら検証用の事例を作ることを避けるため、正式評価前にM1–M9を資料として作成し確定した。

| 資料 | 内容 |
|---|---|
| M1 | 個別の事実の一覧 |
| M2 | 研究1の表現を使う検証条件 |
| M3 | 含む情報をそろえた従来型の比較対象 |
| M4 | 比較対象の情報量が一致するかを確かめる規則 |
| M5 | 証拠の適用範囲を伝える表示の一覧 |
| M6 | 誤読を想定した事例の一覧 |
| M7 | 想定される解釈の正解 |
| M8 | 公開文書の検索語の一覧 |
| M9 | 分析の構造と再現性の確認資料 |

評価前に資料が揃ったかを確認した監査の結果は次である。

```text
facts                              = 16
critical facts                     = 15
Study-1 / baseline fact sets equal = true
boundary families                  = 12
adversarial cases                  = 36
variants per boundary              = 3
public-document queries frozen     = 10
results to screen per query        = 10
maximum discovery frame            = 100
M1 through M9 materialized         = true
pre-evaluation audit               = PASS
```

この時点では正式な判定条件の採点も公開文書の検索も実行していなかった。

---

# 8. 正式な判定条件

Study 2Aは五つの相互に代替できない判定条件で構成した。

| 判定条件 | 評価対象 | 合格に必要なこと |
|---|---|---|
| A1 | 出典と規則を追跡できるか | 重要な事実のすべてが研究1にたどれる |
| A2 | 証拠の適用範囲が伝わるか | 根拠のない推論に関する重要な12類型を明示的に退けられる |
| A3 | 比較対象に含む情報が同じか | 重要な事実の欠落・追加・状態変更が0件 |
| A4 | 誤読を想定した解釈が論理的に整合するか | 重要な事例がすべて整合し、架空の生態学的事実を必要としない |
| A5 | 公開文書との整合性 | 事前に確定した文書の検索を実行し、重大な意味の対立を確認する |

研究全体の判定規則は次のとおりである。

```text
READY_FOR_HUMAN_VALIDATION
  A1-A4 PASS
  + A5にcritical conflictなし
  + 再現と事前資料の作成が確認された

NOT_READY_FOR_HUMAN_VALIDATION
  critical A1-A4 failure
  または A5 CRITICAL_CONFLICT

MIXED
  A1-A4 PASS後のnon-critical mismatch
  重大な不合格を相殺するためには使わない

INDETERMINATE
  frozen material不足/破損
  irreproducible analysis
  prospectively required documentary auditを実行不能
```

---

# 9. A1 — 出典と規則を追跡できるか

## 9.1 問い

Study 2Aで検証する重要な主張が、Study 1の確定済みの状態・規則・必要な入力の定義へ明示的に追跡できるか。

## 9.2 不合格となる条件

以下は不合格である。

```text
重要な事実が研究1の確定済み資料にない
新たな生態学的仮定を要する
法令や運用に関する仮定を追加する
優先順位について根拠のない仮定を追加する
```

## 9.3 結果

```text
critical facts                 = 15
critical facts traceable       = 15
untraceable critical facts     = 0
invented assumptions required  = 0
```

したがって、

```text
A1 = PASS
```

とした。

---

# 10. A2 — 証拠の適用範囲が伝わるか

## 10.1 問い

Study 1が禁止する根拠のない推論を、その表現から明示的に退けられるか。

事前に12の重要な禁止推論の類型を固定した。代表例は次である。

```text
candidate action != recommendation
G1 scope pass != action pass
source-supported != planning-unit supported
unresolved G4 cannot be assumed passed
G5 NOT_APPLICABLE != ecological safety
missing G6/G7 != feasible
missing/current G8 != permitted
missing information != approval
fewer blockers != higher priority
public no-record != ecological absence
unknown != zero / neutral / safe
representation success != ecological validation
```

## 10.2 結果

```text
critical boundary families          = 12
families with derivable rejection   = 12
missing critical boundary cues      = 0
```

したがって、

```text
A2 = PASS
```

とした。

---

# 11. A3 — 含む情報をそろえた比較対象

## 11.1 なぜ比較対象を情報等価にしたのか

Study 1の構造化した表現と従来型の比較対象を比較する際、構造化した表現を示す条件だけに有利な事実を追加すると、「構造の違い」ではなく「情報量の違い」を比較することになる。

そのため、両条件が保持する判断に関係する個別の事実を同一に固定した。

許可された差は、情報の整理と示し方のみである。

## 11.2 結果

```text
atomic facts                         = 16
Study-1 / baseline fact sets equal   = true
critical fact omissions              = 0
critical fact additions              = 0
critical state changes               = 0
Study-1 ranking signal               = false
baseline ranking signal              = false
Study-1 recommendation signal        = false
baseline recommendation signal       = false
```

したがって、

```text
A3 = PASS
```

とした。

重要なのは、Study 2Aでは人間参加者へこの比較条件を提示して成果を測定していないことである。A3は**比較条件に含む情報が同じことを確認した判定条件**であり、構造化した表現を示す条件が人間にとって優れていることを示す結果ではない。

---

# 12. A4 — 誤読を想定した論理的一貫性

## 12.1 設計

A2で定めた根拠のない推論の12類型について、示し方の異なる例をそれぞれ3種類作り、計36件の事例を確定した。

```text
12 boundary families
×
3 surface variants
=
36 adversarial cases
```

G1–G8の対象事例数は次である。

```text
G1 = 5 cases
G2 = 5 cases
G3 = 5 cases
G4 = 5 cases
G5 = 4 cases
G6 = 4 cases
G7 = 4 cases
G8 = 4 cases
```

## 12.2 採点前の訂正

正式評価前のQAで、最初に作成した資料には異なる例のIDが異なるにもかかわらず、一部の禁止推論の類型の中でで表現上の文言が実質同一という問題が見つかった。

この問題は、

```text
formal scoring前
public-document search前
formal outcome assignment前
```

に修正した。

変更したのは表現上の文言だけであり、事実、想定した解釈、重要性の区分、対象とする判定条件は変更していない。修正履歴は進捗記録に保存した。

## 12.3 結果

```text
adversarial cases                          = 36
critical expected interpretations          = 36
consistent critical interpretations        = 36
contradictory critical interpretations     = 0
cases requiring invented ecological truth  = 0
```

したがって、

```text
A4 = PASS
```

とした。

A4は架空の事例に対する内部論理の検証であり、人間が実際にどの程度誤読するかという誤読の割合を測定したものではない。

---

# 13. A5 — 公開文書の用語と実務手順との整合性

## 13.1 目的

A5では、Study 1が分離している概念や実務の手順が、阿蘇・熊本・国の公開行政・運用文書において重大に逆転していないかを検査した。

対象領域は次である。

```text
management / review planning
permission / authorization
safety / current-condition checks
resource / capacity constraints
monitoring / validation
data / source provenance
```

A5は、行政文書がStudy 1を「承認した」かを調べるものではない。

また、

```text
public-document compatibility
!=
practitioner acceptance
```

である。

## 13.2 結果を見る前に確定した検索語

正式な検索前に以下の検索語10本を凍結した。

| ID | 検索語 | 対象となる内容 |
|---|---|---|
| Q01 | 阿蘇 草原 野焼き 管理 許可 | 阿蘇の野焼きと許可 |
| Q02 | 阿蘇 草原 野焼き 安全 管理 | 阿蘇の野焼きと安全 |
| Q03 | 阿蘇 草原 放牧 管理 計画 | 阿蘇の放牧管理 |
| Q04 | 阿蘇 草原 刈取り 管理 計画 | 阿蘇の刈取り管理 |
| Q05 | 熊本県 野焼き 許可 草原 | 熊本県の野焼きと許可 |
| Q06 | 熊本県 草原 保全 管理 計画 | 熊本県の保全計画 |
| Q07 | 環境省 二次草原 管理 指針 | 国の草原管理指針 |
| Q08 | 阿蘇 草原 再生 モニタリング 管理 | 阿蘇での継続観測と管理 |
| Q09 | Aso grassland burning management official | 英語による候補資料の確認 |
| Q10 | Kumamoto grassland conservation management official | 英語による候補資料の確認 |

## 13.3 停止条件

停止規則は次のように固定した。

```text
各queryについて最初の10 unique retrievable resultsをscreenする
canonical document / URLでdeduplicateする
最初のquery/rank occurrenceを保持する
最大discovery frame = 100 query-result positions
eligible documentはすべて含める
favorable resultが見つかっても途中停止しない
```

この有限の検索範囲により、結果に都合のよい文書だけを追加検索し続けることを防いだ。

---

# 14. A5で確認した公開文書

正式な検索範囲内で適格と判断された文書の説明のための資料には、以下のような公式・運用資料が含まれた。

| ID | 発行主体 | 文書・ページ | 関連する実務領域 |
|---|---|---|---|
| D01 | 環境省 | 阿蘇くじゅう国立公園 風景地保護協定 | 管理の対象・許可・実施 |
| D02 | 農林水産省 | 世界農業遺産 熊本県阿蘇地域 | 管理計画・評価・継続観測・見直し |
| D03 | 阿蘇市 | 令和8年一斉野焼きのお知らせ | 現時点の気象・安全・実施時期 |
| D04 | 南阿蘇村 | 野外焼却・例外規定 | 法令上の例外・安全・火災の予防 |
| D05 | 熊本県 | 県立自然公園の許可・届出 | 許可・届出・権限 |
| D06 | 環境省 | 阿蘇草原保全計画関連業務 | 現況・過去の管理・生態学的調査・計画策定 |
| D07 | 環境省 | 阿蘇管理道路調査・設計関連業務 | 作業資源・実施・安全・計画 |
| D08 | 熊本県 | 阿蘇草原維持再生基礎調査 | 地域の管理状況・担い手の対応能力・課題の把握 |
| D09 | 阿蘇グリーンストック | 草原保全ボランティア活動 | 研修・労働力・安全 |
| D10 | 阿蘇草原再生協議会 | 情報プラットフォーム | 出典情報・利用条件・出典表示 |
| D11 | 環境省 | 阿蘇くじゅう国立公園の取組 | 管理上の困難・担い手・協働 |
| D12 | 環境省 | 自然再生基本方針 | 地域の条件・継続観測・関係者・順応的管理 |
| D13 | 環境省 | 阿蘇草原再生全体構想 | 再生計画・関係者間の調整・継続観測 |
| D14 | 環境省 | 阿蘇地域管理運営計画関連資料 | 地域計画・審議・意見募集 |
| D15 | 農研機構 | 阿蘇草原植生に対する刈取り時期の影響 | 管理への応答の背景・刈取り時期・注意点 |
| D16 | 熊本県 | 阿蘇草原再生全体構想 第3期 | 再生計画・地域の調整・管理 |
| D17 | 環境省 | 阿蘇くじゅう国立公園 保護・規制計画改定関連資料 | 保護の規則・土地利用の条件 |
| D18 | 熊本県 | 自然環境保全基本方針 | 規則・評価・継続観測・保全計画 |

これらはA5で取得できた資料を記述するためのものであり、18文書だけを都合よく選んで正式な調査対象と定義したものではない。正式な規則はあくまで結果を見る前に確定した10検索語の検索範囲である。

---

# 15. A5の正式な実施と結果

正式な検索で得られた検索結果の順位枠は次であった。

```text
Q01 = 10
Q02 = 10
Q03 = 10
Q04 = 10
Q05 = 10
Q06 =  9
Q07 =  9
Q08 = 10
Q09 = 10
Q10 = 10

TOTAL = 98 / intended 100
```

Q06とQ07はそれぞれ9件しか返却されなかった。

利用可能な適格文書の内容の確認では、次がすべて確認された。

```text
reviewScopePlanningRepresented       = true
permissionAuthorizationRepresented  = true
safetyCurrentConditionRepresented   = true
resourceCapacityRepresented         = true
monitoringValidationRepresented     = true
sourceLocalProvenanceRepresented    = true
criticalSemanticConflictsObserved   = 0
```

しかし、正式な規則は「資料の不足を整合の証拠へ変換しない」と事前に規定していた。

検索挙動を見た後で、

```text
別の検索語を追加する
不足した順位枠だけを再検索する
検索条件を緩める
手作業の代用で10件へ埋める
```

ことは、結果を見る前に確定した検索対象と順位の枠組みの変更になる。

そのため不足した2順位は補完しなかった。

```text
A5 = INDETERMINATE
```

とした。

これは、

```text
critical conflictが見つかった
```

という結果ではない。

正確には、

> **利用可能な適格文書では重大な意味上の対立を観察しなかったが、凍結済み正式な検索範囲を完全に実行できなかったため、整合性の正式な判定を確定しなかった。**

という結果である。

---

# 16. Study 2Aの正式判定

正式結果は次のとおりである。

```text
A1 traceability                    PASS
A2 evidence-boundary cues         PASS
A3 baseline equivalence           PASS
A4 adversarial consistency        PASS
A5 documentary compatibility      INDETERMINATE

OVERALL                            INDETERMINATE
```

研究全体の判定規則では、A5を正式に評価できない状態で `READY_FOR_HUMAN_VALIDATION` を付与しない。

同時に、A1–A4に重大な不合格はなく、A5で `CRITICAL_CONFLICT` を観察したわけでもないため、`NOT_READY_FOR_HUMAN_VALIDATION`にも分類しない。

したがって正式判定は、

> **INDETERMINATE（判定不能）**

である。

`INDETERMINATE`はStudy 2Aが未完了という意味ではない。事前に定めた判定規則を適用した結果、「READY / NOT_READY / MIXEDの正式な判定を正当化できない」と判定し、その状態で研究を完了・凍結したという意味である。

---

# 17. 本研究が支持すること

Study 2Aは、少なくとも以下を支持する。

1. Study 1の重要な事実を、15/15について確定済みの出典の状態・規則・必要な入力の定義へ追跡できる。
2. 根拠のない推論に関する12の重要な類型すべてについて、禁止する解釈を表現から明示的に棄却できる。
3. 研究1の表現と従来型の比較対象に、同じ16の事実を含められる。
4. 重要な事実の欠落・追加・状態変更を0のまま比較できる形を作れる。
5. 根拠のない推論の12類型について示し方の異なる例を各3種類用意し、計36件の事例を結果を見る前に確定できる。
6. 36/36の重要な事例に対して想定した解釈が内部整合し、架空の生態学的な事実を必要としない。
7. 公開文書の用語と実務手順に関する監査を有限の検索範囲として結果を見る前に規定できる。
8. 検索結果の不足が生じても、それを結果を見た後に行う追加検索で都合よく修復しない判定規則を実行できる。
9. 取得できた公式・実務文書において、研究1で定めた証拠の限界を覆す重大な意味の逆転は観察されなかった。
10. 人間参加者を使わずに得た証拠と人間参加者から得た証拠を正式な研究運用規則上分離できる。
11. `INDETERMINATE`を都合よく肯定・否定の判定に変更せず、妥当な最終結果として凍結できる。

---

# 18. 本研究が支持しないこと

Study 2Aは以下を主張しない。

- 実務者が研究1の表現を正しく理解できる
- 実務者による根拠のない推論が減る
- 実務者がこの表現を好む
- 実際の判断の質が改善する
- 判断にかかる時間が短くなる
- 行政の実務手順へ実際に適合する
- 組織への導入が進む
- 認知的な負担が小さい
- 人の判断に対する確信度が適切になる
- 管理行為が生態学的に有効である
- 元の調査地点で得た応答を計画単位へ適用できる
- G4で応答の転用を検証済みである
- 候補行動が推奨される
- 候補行動が安全である
- 必要な許可や承認を得ている
- 必要な入力の数が管理行為の優先順位を示す
- 最適な管理配置が得られた
- 言語モデルの応答が実務者の判断の代わりになる

特に、

```text
human participant evidence = 0
```

である。

---

# 19. 実務的含意

Study 2Aの実務的含意は、「人間に使わせる前に機械的・構造的に確認できること」と「人間に使わせなければ分からないこと」を分離した点にある。

人が使う意思決定支援を評価する場合、いきなり人間参加者を対象とした研究へ進む前に、少なくとも次を確認できる。

```text
根拠をたどれるか
禁止した推論を表現自体が退けるか
比較条件の情報量が等しいか
誤読を想定した事例で矛盾しないか
公開文書の実務用語と重大に食い違わないか
```

しかし、これらを通過しても、

```text
実際に分かりやすいか
誤読率が低いか
現場で使いやすいか
```

は残る。

Study 2Aは、この残差を「AIなら分かる」「文書上は似ている」といった代替物で結論づけなかった。

---

# 20. NAP-002 Study 2Bとの境界

Study 2Bは、実在する実務者や行政の担当者を対象とする実在の人による検証である。

現在の状態は、

```text
NAP-002 Study 2B
DEFERRED / NOT STARTED
```

である。

研究2Bが扱う予定の主な観点は次である。

```text
comprehension
evidence-boundary interpretation
critical unsupported-inference error
required-input identification
rationale traceability
usability
cognitive burden
workflow fit
confidence calibration
```

Study 2Aの結果を用いて、これらの人を対象に測る結果を「実質的に検証済み」と扱ってはならない。

また、Study 2Aが `INDETERMINATE` であるため、`READY_FOR_HUMAN_VALIDATION`も`NOT_READY_FOR_HUMAN_VALIDATION`も正式には付与されていない。

将来Study 2Bを実施する場合は、参加者の募集経路、倫理と個人情報の扱い、参加条件、調査手段、割付け、標本と統計解析の計画等を別の研究計画として結果を見る前に管理する必要がある。

---

# 21. G4 Response-Transfer 検証との関係

Study 2A / 2Bは人が使う意思決定支援の検証系列である。

一方、Study 1で最も重要な科学的な障壁の一つは、

```text
source-local response
!=
planning-unit response
```

というG4での別の場所への適用可能性である。

G4は人にとっての使いやすさとは別の科学的問題であるため、Study 2Bを延期したまま残し、結果を見る前に計画する独立したG4の応答転用検証研究へ進むことは可能である。

ただし、G4の研究はStudy 2Bの実在の人による検証が完了したと仮定してはならない。

逆に、将来研究2Bの結果が肯定的であっても、それによってG4が検証済みになるわけではない。

```text
human usability
!=
ecological response transferability
```

である。

---

# 22. 研究上の限界

## 22.1 人間参加者を使用していない

Study 2Aの最大の限界であり、同時に研究の識別情報そのものである。

理解度、選好、使いやすさ、実務手順への適合、認知的な負担等の人を対象に測る結果は測定していない。

## 22.2 A4は架空の誤読事例を用いた整合性確認

36事例は表現の論理的一貫性を検証するための架空の検証であり、実在の実務者が誤読する割合の分布を推定するものではない。

## 22.3 A3は比較対象より優れていることを示さない

A3は両条件に含まれる事実の一致を確認しただけであり、構造化した表現が情報を平面的に示した比較対象より人間にとって優れていることを示さない。

人にとっての優劣を検証するには実際の参加者の課題成績が必要である。

## 22.4 A5は公開文書との整合性を扱い、人間による受容性を示さない

行政・運用文書で用語や実務上の概念が共存していても、実際の担当者が研究1の表現を自然に理解できるとは限らない。

## 22.5 A5 検索対象と順位の枠組みが完全実行できなかった

事前に定めた100順位のうち98順位しか取得できなかったため、A5は正式には判定不能となった。

この限界を後から検索条件変更で消していない。

## 22.6 検索結果の返り方は研究対象そのものではない

A5の `INDETERMINATE` は、行政文書が2件不足しているという意味ではない。事前に決めた10件の検索結果が得られなかった検索語が2本あり、予定どおりの検索を実行できなかったことを示す。

## 22.7 研究1の科学的結果は再検証していない

Study 2AはG1–G8の生態学的・運用上の事実を新規に測定した研究ではない。Study 1の確定済みの表現を結果を変更しない先行研究の入力として扱った。

---

# 23. 第三者資料・データの取扱い

本公開報告書は単体公開を想定し、第三者著作物や個人情報の再配布を必要最小限にしている。

本レポートには、

- 原著論文PDFそのもの
- 行政文書PDFそのもの
- 行政文書の図表画像
- 大量の逐語引用
- 利用に制限のある非公開の元データ
- 慎重な扱いを要する希少種の座標
- 実務者の個人情報
- 参加者のデータ
- 組織を特定できる機密データ

を収録していない。

A5で用いた公開文書については、発行主体・表題・URL・関連する実務領域などの出典情報をリポジトリ内の機械で読み取れる記録へ保持している。

Study 2Aでは公開された公的機関の文書を主対象とし、個人が公開した意見や個人SNS投稿を人間の行動を示す証拠として扱っていない。

---

# 24. 再現性と終了時の監査

## 24.1 正式結果の再構成

確定済みの成果物から再計算した判定条件ごとの状態は次である。

```text
A1 = PASS
A2 = PASS
A3 = PASS
A4 = PASS
A5 = INDETERMINATE

recomputed formal outcome = INDETERMINATE
stored formal outcome     = INDETERMINATE
```

再現性の監査では、

```text
passed                          = true
formalResultReproducible        = true
inputsFrozenBeforeRelevantScoring = true
decisionRuleConsistent          = true
postHocA5GapFill                = false
llmFormalInferenceUsed          = false
humanParticipantDataUsed        = false
study1EndpointsModified         = false
study2BStarted                  = false
interpretationCeilingPreserved  = true
```

を確認した。

## 24.2 誤読を想定した終了時の監査

結果を確定したときには、結果の解釈が都合よく拡張されていないかを別途監査した。

以下はすべて `false` である。

```text
A5 missing ranksをcompatibilityへ変換
no-conflict observationをREADYへ昇格
INDETERMINATEをsecondary evidenceでsoften
Study 1 formal endpointsを書換え
Study 2Aをhuman validationとして報告
practitioner usability claim
G4/ecological validation claim
management recommendation / authorization
LLMをhuman surrogateとしてformal利用
Study 2Bを暗黙に完了扱い
unknownをzero/safeへ変換
public no-recordをecological absenceへ変換
```

誤読を想定した終了時の監査は `PASS` であり、結果を確定できる状態になったとなった。

---

# 25. 再現性識別子

Study 2Aの主な確定済み識別情報を以下にまとめる。

## 研究の識別情報

```text
NAP002-STUDY2A-NONPARTICIPANT-PREVALIDATION-2026-08-14-v1
```

## 科学的結果を確定した時点

```text
repository = nkkmd/natural-area-planning
study-state snapshot commit = db83cae09e9b84a6b9deab46d87af6c36e9cfa49
study date = 2026-08-14 JST
```

## 評価前に確定した資料

```text
facts = 16
critical facts = 15
boundary families = 12
adversarial cases = 36
variants per boundary = 3
public-document queries = 10
maximum discovery frame = 100
pre-evaluation audit = PASS
```

## A1–A4の正式な成果物識別情報

```text
2445d07d93f47a7f9fba817df1e6eb74b17579f3
```

## A5の正式な成果物識別情報

```text
95289455433ff3f0fa0cf1bb9fe00558b1b6c56e
```

## 正式結果の成果物識別情報

```text
18bf2e864c1fad7c4dfbeb46aacdf2c025e0ac5d
```

## 最終判定

```text
A1 PASS
A2 PASS
A3 PASS
A4 PASS
A5 INDETERMINATE
OVERALL INDETERMINATE
```

---

# 26. リポジトリ内の主要な再現性資料

このレポート単体で主要結論を理解できるが、出典・処理の履歴と機械的な監査はリポジトリで追跡できる。

## 結果を見る前に定めた研究計画

```text
doc/nap002/study2/study2a/NAP002_STUDY2A_PROSPECTIVE_RESEARCH_PROTOCOL.md
doc/nap002/study2/study2a/FORMAL_DECISION_GATES.md
doc/nap002/study2/study2a/PUBLIC_DOCUMENT_AUDIT_PROTOCOL.md
doc/nap002/study2/study2a/MATERIALIZATION_AND_REPRODUCIBILITY_PLAN.md
doc/nap002/study2/study2a/DECISION_REGISTER.md
```

## 評価前に確定した資料

```text
analysis/nap002/study2a/study2a_design_registry.json
analysis/nap002/study2a/materialization/atomic_fact_registry.csv
analysis/nap002/study2a/materialization/study1_test_condition.json
analysis/nap002/study2a/materialization/baseline_condition.json
analysis/nap002/study2a/materialization/boundary_cue_registry.csv
analysis/nap002/study2a/materialization/adversarial_case_registry.csv
analysis/nap002/study2a/materialization/adversarial_expected_key.csv
analysis/nap002/study2a/materialization/public_document_search_register.csv
analysis/nap002/study2a/materialization/pre_evaluation_materialization_audit.json
```

## 正式結果

```text
analysis/nap002/study2a/results/a1_a4_formal_audit.json
analysis/nap002/study2a/results/a5_retrieval_execution_audit.json
analysis/nap002/study2a/results/a5_observed_documentary_context.csv
analysis/nap002/study2a/results/a5_public_document_compatibility_audit.json
analysis/nap002/study2a/results/study2a_formal_result.json
analysis/nap002/study2a/results/study2a_reproducibility_audit.json
analysis/nap002/study2a/results/study2a_adversarial_closure_audit.json
```

## 進捗記録

```text
doc/nap002/study2/checkpoints/2026-08-14-study2-split-into-2a-2b.md
doc/nap002/study2/checkpoints/2026-08-14-study2a-prospective-design-freeze.md
doc/nap002/study2/checkpoints/2026-08-14-study2a-pre-evaluation-materialization-freeze.md
doc/nap002/study2/checkpoints/2026-08-14-study2a-pre-scoring-materialization-correction.md
doc/nap002/study2/checkpoints/2026-08-14-study2a-a1-a4-formal-audit.md
doc/nap002/study2/checkpoints/2026-08-14-study2a-a5-formal-audit.md
doc/nap002/study2/checkpoints/2026-08-14-study2a-formal-closure.md
```

---

# 27. 今後の研究

## 27.1 Study 2B — 実在する人による検証

実在の実務者や行政の担当者を対象に、理解度、重大な根拠のない推論による誤り、必要な入力の特定、判断理由の追跡可能性、使いやすさ、実務手順への適合等を検証する。

現在は `DEFERRED / NOT STARTED` である。

## 27.2 G4 Response-Transfer 検証

Study 1の主要科学的な障壁である別の場所への応答の適用可能性を扱う、結果を見る前に計画した独立研究である。

少なくとも、

```text
source / target comparability domain
management-definition compatibility
target / outcome definition
context modifiers
transfer criteria
explicit non-transfer state
analysis plan
external / temporal validation
```

等を結果を見る前に固定する必要がある。

## 27.3 運用手順の試験

将来、実際の判断時点の地域固有・現時点の入力を扱う場合は、Study 1/2Aとは別の結果を見る前に定める運用上の研究手順が必要になる。

許可、安全、天候、現地の状態等の現時点の事実を過去の公開資料で代替してはならない。

## 27.4 Future Stage A / B

利用に制限のある地域の実測データや新たに事前計画した現地調査・継続観測を使う研究は、NAP-001の公開情報のみを用いたStage Cで確定した結果を変更せず、別の研究として管理する。

---

# 28. 結論

本研究は、研究1で作った「どこを確認するか・何が判断を止めるか・次に何を調べるか」という意思決定支援の表現を、人間参加者を使わずに事前検証した。採点前に16の事実（うち重要な事実15）、禁止すべき推論の12類型、誤読を想定した36事例、公開文書の検索語10本と判定規則を確定した。

追跡可能性などのA1–A4は合格し、取得できた公開文書にも重大な意味上の対立は見られなかった。しかし、事前に定めた検索結果100順位のうち確認できたのは98順位だった。検索方法を後から変えず、A5と研究全体をINDETERMINATE（判定不能）とした。

この結果は人間を対象とした検証に代わるものではない。**資料と規則の追跡、誤った解釈の排除、比較条件に含む情報の一致は人間参加者なしでも点検できる。一方、実務者が実際に理解し、誤読せず使えるかは、人間参加者による検証が必要である。**

```text
16 atomic facts
15 critical facts
12 critical boundary families
36 adversarial cases
10 frozen documentary queries
```

```text
A1 traceability                    PASS
A2 evidence-boundary cues         PASS
A3 baseline equivalence           PASS
A4 adversarial consistency        PASS
A5 documentary compatibility      INDETERMINATE
OVERALL                            INDETERMINATE
```

---

# 用語

**人間参加者を用いない事前検証（non-participant pre-validation）**  
実在の参加者から理解度や使いやすさに関するデータを得ず、表現や研究手順に必要な条件を事前に点検すること。人間を対象とした検証の代わりにはならない。

**追跡可能性（traceability）**  
評価する主張や状態が、研究1で確定した規則・状態・必要な入力の定義にたどれること。

**個別の事実**  
二つの提示方法に同じ情報が含まれるかを調べるため、情報を最小単位に分けたもの。

**証拠の限界を伝える表示（boundary cue）**  
「候補行動に含まれることは推奨ではない」など、証拠が許さない推論を退けるための表示。

**誤読を想定した事例**  
誤った推論や論理的な矛盾が起きないか確認するために作った架空の事例。

**情報量をそろえた比較対象（information-equated baseline）**  
研究1の表現と同じ事実を含め、情報の整理と示し方だけを変えた比較条件。

**公開文書との整合性**  
公開された行政・運用文書の用語や手順と、研究1で分けた概念が重大に食い違わないかという文書上の性質。実務者による受容を意味しない。

**INDETERMINATE**  
事前に定めた条件で正式判定を確定するための資料や実施結果が不足している状態。本研究ではA5の検索を予定どおり完了できなかったことによる。研究そのものは完了している。

**Study 2B**  
実在する実務者や行政担当者を対象に、将来行う人間参加者による検証。研究2Aとは独立している。

---

# 参考文献・関連する先行研究

研究2Aは、意思決定支援や不確実性の示し方に関する広い先行研究を踏まえている。これらの一般的な方法そのものを新たに発明したとは主張しない。

- Martin et al. (2009). Structured decision making / decision-threshold literature. DOI: `10.1890/08-0255.1`
- Hemming et al. (2022). Decision science in conservation. DOI: `10.1111/cobi.13868`
- Regan et al. (2005). Robust conservation decision making under severe uncertainty. DOI: `10.1890/03-5419`
- Korporaal, Ruginski & Fabrikant (2020). Effects of uncertainty visualization on map-based decisions. DOI: `10.3389/fcomp.2020.00032`
- Arciniegas, Janssen & Rietveld (2013). Collaborative map-based spatial decision support evaluation. DOI: `10.1016/j.envsoft.2012.02.021`

関連する先行報告書:

- Natural Area Planning / NAP-001 — 公開研究報告書, `doc/publication/NAP001_PUBLIC_RESEARCH_REPORT.md`
- Natural Area Planning / NAP-002 Study 1 — 公開研究報告書, `doc/publication/NAP002_STUDY1_PUBLIC_RESEARCH_REPORT.md`

A5で確認した文書について、出典を機械で読み取れる形で記録した資料:

- `analysis/nap002/study2a/results/a5_observed_documentary_context.csv`
- `analysis/nap002/study2a/materialization/public_document_search_register.csv`

---

## 引用時の推奨表記

本レポートを引用する場合は、少なくとも次の情報を含めることを推奨する。

```text
Natural Area Planning / NAP-002 Study 2A (2026).
Public Research Report:
人間参加者を用いずに意思決定支援表現をどこまで事前検証できるか
— 追跡可能性・誤った推論への耐性・情報量の一致・公開行政文書との整合性を検証する —.
Version 1.0.1, 日本語表現改訂 2026-09-28（科学的結果は2026-08-14確定）。
Formal outcome: INDETERMINATE.
Study snapshot: nkkmd/natural-area-planning @ db83cae09e9b84a6b9deab46d87af6c36e9cfa49.
```

ここに示した研究状態のスナップショット（`Study snapshot`）は、Study 2Aの確定済みの科学的結果を指す。その後に行った案内の更新、日本語表現の修正、公開報告書の体裁の整備は編集上の変更であり、正式な研究結果を変更していない。

著者名、所属、DOI、恒久公開URL等が後日正式に付与された場合は、それらを優先して引用情報へ追加する。