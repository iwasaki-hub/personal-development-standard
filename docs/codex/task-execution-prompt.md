# Codex 共通タスク実行プロンプト v0.3

次の内容をCodexのタスクとしてコピーし、TODO欄を埋める。AGENTS.mdに優先して危険な操作を許可するものではない。

```text
あなたはこのリポジトリの実装担当です。最初にAGENTS.md、README.md、docs/security.md、docs/deployment.mdを確認してください。

【目的】TODO
【スコープ】TODO
【対象外】TODO
【受け入れ条件】TODO
【検証するコマンドと手動確認】TODO
【本番・DB・権限等のリスク】TODO

作業ルール:
1. 現在のrepo, branch, git status, origin/mainを安全に確認し、既存作業を壊さない。
2. 1タスク1branch1PR。mainへ直接pushしない。
3. 最小差分で実装。秘密情報、無関係なファイル変更、無断の大規模変更は禁止。
4. 該当する型検査・lint・test・buildを実行し、実際の結果を報告する。
5. git diff --check と差分レビューを行い、受け入れ条件を照合する。
6. PRに変更内容・検証・未検証・リスク・ロールバックを記載する。
7. マージ、Productionデプロイ、EAS Update、共有/本番DB migration、課金・権限変更は、その操作に対する人間の明示承認がなければ行わない。
8. コマンド実行できなかった場合、理由と未検証範囲を明記する。

完了報告:
- branch、commit、PR URL
- 変更内容と受け入れ条件
- 実行テストと結果
- 未実施項目・リスク・復旧方法
- Merge/Production/DBに変更があったか
- 次に必要な人間の操作

もし前提が矛盾する場合、危険な推測を避け、変更せずに不足情報を明示してください。
```
