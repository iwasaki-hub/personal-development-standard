# Personal Development Standard v0.2

GitHub Template Repository として使える、技術スタック非依存の開発標準です。

## 最初にやること
1. GitHubでこのリポジトリを作成して Settings → General → **Template repository** にチェック。
2. 新規プロジェクトでは **Use this template** からリポジトリを作成（既存プロジェクトへは必要ファイルのみ段階的に導入）。
3. `docs/requirements.md`, `docs/architecture.md`, `docs/deployment.md`, `docs/security.md` を実態に合わせて更新。
4. `AGENTS.md` と `docs/development/roadmap.md` を確認し、作業を1タスク1PRに分割。
5. 必要なら `templates/stacks/` と `templates/workflows/` のサンプルを参照し、技術別CIを追加。
6. GitHubのBranch protection / RulesetsとEnvironment protectionを手動で有効化（ファイル配置だけでは保護は有効になりません）。

## 収録内容
- `AGENTS.md`: Codexを含む開発エージェント共通ルール
- `.github/workflows/standards.yml`: スタック非依存のドキュメント構造チェック
- `.github/pull_request_template.md`: 変更内容・テスト・リスク・承認チェック
- `.github/ISSUE_TEMPLATE/task.yml`: タスク定義フォーム
- `docs/`: 要件、設計、セキュリティ、デプロイ、開発記録
- `templates/stacks/`: Expo、Web、API、Supabaseの追加ガイド
- `templates/workflows/node-ci.example.yml`: Node系プロジェクト向け任意追加CI
- `scripts/validate-standards.sh`: ローカル検証

## 共通開発フロー
Issue/要件 → 専用branch → 最小実装 → ローカルテスト → PR → CI/Preview/実機 → 人間レビュー → Merge → 承認付き公開 → 記録。

## 重要な境界
- デフォルトでは**デプロイ、マージ、DB migration実行を自動化しない**。
- 既存repoへの導入では、現在のCIやAGENTS.mdを上書きしない。
- テストの実施は実際の実行結果でのみ「成功」と記載する。
- CIが通っただけで機能やセキュリティ全体の確認が済んだとはみなさない。

## 設計方針
『安全な反復は自動化、公開・権限・データ破壊は人間の判断』を基本とします。
詳細は `docs/development/working-agreement.md` と `docs/development/adoption-checklist.md` を参照。
