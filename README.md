# Personal Development Standard v0.3

技術スタック共通の開発規約と、新規GitHubリポジトリ向けの安全なbootstrapを提供します。

## クイックスタート
1. GitHub Settings → General → Template repository を有効化。
2. **Use this template** で新しいリポジトリを作る。
3. clone後、次を実行（既定はdry-run）：

```sh
python3 scripts/bootstrap.py --project NewApp --stacks web
python3 scripts/bootstrap.py --project NewApp --stacks web --apply
python3 -m unittest discover -s tests -v
bash scripts/validate-standards.sh
```

4. 生成された`project.config.json`と`.github/workflows/stack-ci.yml`を確認し、プロジェクトのnpm scriptsや各種設定を整える。
5. docsのTODOを埋め、専用branchでPRを作る。CIを確認して、人間がマージを決定。
6. GitHub Rulesets/Branch protection、Environment保護を各リポジトリで設定（ファイルのコピーでは自動適用されない）。

## v0.3 の4本柱
- **GitHub保護**: `docs/github-protection.md`, `config/github/main-ruleset.example.json`
- **CI選択**: `docs/ci-selection.md`, `scripts/bootstrap.py` （Web/Expo/API/Supabase）
- **Codex共通プロンプト**: `docs/codex/task-execution-prompt.md`
- **初期化**: `docs/bootstrap.md`, `tests/test_bootstrap.py`

## 既存の共通ルール
- `AGENTS.md`: 1タスク1PR、main直push禁止、危険操作の事前承認
- `.github/workflows/standards.yml`: 共通ファイル構造 + bootstrap tests
- `.github/ISSUE_TEMPLATE/task.yml`, `.github/pull_request_template.md`
- `docs/requirements.md`, `docs/architecture.md`, `docs/security.md`, `docs/deployment.md`
- `docs/development/`: ロードマップ、ADR、タスク、運用、導入チェックリスト
- `templates/stacks/`, `templates/workflows/`: 技術別ガイドとサンプル

## 制約と重要事項
- `--apply`は**新規の設定ファイルをローカル生成するだけ**。push、merge、Production、DB更新、EAS Updateは行わない。
- 既存`project.config.json`、`stack-ci.yml`があるときは上書きを拒否。
- stack CIは対象のnpm scriptsを要求し、未実装ならCI失敗になる。Supabaseは静的レビュー案内のみで、RLS/SQLの安全性を保証しない。
- 既存プロジェクトにはそのまま一括適用しない。専用PRで差分を段階的に移す。
- GitHub Rulesets/Branch protectionの**実際の強制力**はアカウントプラン・権限と各リポジトリの設定に依存し、設定ファイルの追加だけでは有効にならない。
- 自動デプロイは組み込まない。人間の承認を必須にする。

詳細: `docs/bootstrap.md`, `docs/ci-selection.md`, `docs/github-protection.md`, `docs/codex/task-execution-prompt.md`。
