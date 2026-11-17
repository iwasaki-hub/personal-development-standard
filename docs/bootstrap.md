# 新規プロジェクト初期化 v0.3

## 推奨ステップ
1. このリポジトリをTemplate repositoryとして設定する。
2. Use this template → Create new repository で新しいプロジェクトを作る。
3. ローカルにcloneし、`python3 scripts/bootstrap.py --project <name> --stacks web` で生成プランを確認。
4. 問題なければ同じコマンドに`--apply`を付ける。
5. 出力された`project.config.json`と`.github/workflows/stack-ci.yml`を確認。
6. docsのTODOを埋め、package scriptsやtest環境を設定。CIをローカルで確認してから1PRを作る。
7. main保護とEnvironmentの承認設定はGitHub上で個別に適用する。

## 具体例
```sh
python3 scripts/bootstrap.py --project RecipeApp --stacks mobile-expo,database-supabase
python3 scripts/bootstrap.py --project RecipeApp --stacks mobile-expo,database-supabase --apply
python3 -m unittest discover -s tests -v
```

`--apply`はローカルに2ファイルを生成するだけで、commit、push、デプロイ、DB操作、Secrets登録をしない。
未対応のstack、重複stack、不正なproject名、既存ファイルを検知して停止する。
既存リポジトリへの導入では新規生成ではなく現状差分を評価し、専用PRで段階導入する。
