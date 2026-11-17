# CI選択方式 v0.3

## 適用
新規テンプレートリポジトリを作成したら、次のどれかを選択して初期化する。

```sh
python3 scripts/bootstrap.py --project MyNewApp --stacks web
python3 scripts/bootstrap.py --project MyNewApp --stacks mobile-expo,database-supabase --apply
```

既定は**dry-run**。--applyを渡して初めて`project.config.json`と`.github/workflows/stack-ci.yml`が生成される。
既存ファイルがあるときは失敗し、上書きしない。スクリプトは外部ネットワークやGitHub APIを呼ばない。

## スタック
| 入力 | CI | 明示的に除外するもの |
|---|---|---|
| web | Node 22 + npm ci + lint + typecheck + test + build | production deployment |
| mobile-expo | Node 22 + npm ci + lint + typecheck + test | EAS build/submit/update |
| api | Node 22 + npm ci + lint + typecheck + test | live API destructive tests |
| database-supabase | migration file changesを検出し、手動レビューを促す | remote db push, migration apply, reset |

web/mobile-expo/apiは`package.json`と`package-lock.json`、対象npm scriptsが必要。
追加したCIは**存在しないnpm scriptも失敗**するため、プロジェクトで整備する。
複数stack指定はコマンドの集合をとり、buildはwebを選択したときだけ必須。
database-supabaseの確認は静的な案内にとどまり、SQLの安全性やRLSを保証しない。
DB変更は隔離環境と実JWTで検証したうえで別途承認する。

## 共通CI
`standards.yml`はテンプレート構造・bootstrapの単体テストを実行し、デプロイしない。
追加CIは`pull_request`と`push main`で検査のみ実行。
PreviewやProductionへのデプロイは各プロジェクトで別途設計し、人間承認ゲートを設定してから導入。

## Branch protection
GitHub Actionsでworkflowを一度実行し、必要なチェックの名前が確認できた後にRulesetで必須化する。
初期化直後に存在しないチェックを必須にしてPRをブロックしないこと。
