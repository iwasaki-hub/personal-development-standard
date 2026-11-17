# Personal Development Standard v0.4

新規GitHubプロジェクトを安全にセットアップするためのテンプレートです。

## 初期化の流れ
1. GitHubの **Use this template** で新規repoを作成。
2. ローカルで技術スタックを選択（dry-run後に明示的にapply）。
3. テストとCIを整備したうえでPRから確認。
4. Rulesetのdry-runと明示承認を行い、GitHub CLIを使って新規repoのmain保護を適用。
5. Actionsのチェック名が実際に作られた後、GitHub UIで必須チェックを追加。

```sh
python3 scripts/bootstrap.py --project NewApp --stacks web
python3 scripts/bootstrap.py --project NewApp --stacks web --apply
python3 scripts/protect_github.py --repo OWNER/NewApp
python3 scripts/protect_github.py --repo OWNER/NewApp --apply --approve OWNER/NewApp
python3 -m unittest discover -s tests -v
```

## ガイド
- **Ruleset適用**: `docs/github-ruleset-bootstrap.md`
- **Ruleset仕様**: `docs/github-protection.md`
- **スタック別CI**: `docs/ci-selection.md`
- **Codexプロンプト**: `docs/codex/task-execution-prompt.md`
- **新規repoの初期化**: `docs/bootstrap.md`
- **開発規約**: `AGENTS.md`

## 安全性
- GitHub設定はテンプレート複製で自動継承されません。
- ルールは明示承認がない限り適用されません。
- 既存Rulesetを上書きせず、競合時は停止。
- 初回から未確認のCIチェックを必須化しません。
- デプロイ、DB更新、Secret変更、リポジトリの公開状態変更は実行しません。
