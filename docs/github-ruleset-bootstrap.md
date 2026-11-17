# GitHub Ruleset bootstrap v0.4

GitHub Template Repositoryの複製ではRulesetsは引き継がれません。
このスクリプトは新しいPublicリポジトリのmainに、基本的なブランチ保護を適用するためのものです。

## 必要条件
- Python 3、GitHub CLI `gh`、GitHubの管理権限を持つ認証
- `gh auth status`で接続先と権限を確認
- 新規repoのdefault branchが`main`
- GitHubプラン/権限がrepository rulesets APIに対応すること

## 手順
1. `python3 scripts/protect_github.py --repo OWNER/NEW_REPO` でdry-run（APIアクセスなし）。
2. ローカルで内容を確認し、人間が承認。
3. `python3 scripts/protect_github.py --repo OWNER/NEW_REPO --apply --approve OWNER/NEW_REPO`。
4. Settings → Rules → RulesetsでActive/main/PR/force push/delete禁止を確認。
5. 初回CIをPRで成功させ、ジョブ名とGitHub Actions提供元を確認してから、GitHub UIでそのstatus checkを必須にする。
6. 必須チェックが実際にマージをブロックすることを確認する。

## 安全策
- --applyかつ--approveが一致した場合にだけGitHubへ書き込み。
- 同名または他のbranch rulesetsが存在する場合は停止。**既存rulesetを編集・削除しません**。
- default branchがmainでない場合は停止。
- --checkはdry-run時の参考表示のみ。誤ったチェック必須化によるデッドロックを避けるため、applyでは拒否。
- ルール作成後GETで再確認。途中で失敗した場合、自動リトライせずGitHub画面で状態を確認する。
- 本番環境、DB、GitHub Secrets、リポジトリ公開状態は変更しない。
- GitHub CLIでのAPI呼び出しを安全に分離し、テストではmockのみ使用する。

## 補足
Required approvals=0は個人開発用の設定です。管理体制に合わせてレビュー人数を検討してください。
`config/github/main-ruleset.example.json`はAPIの参考用であり、実際の作成には`scripts/protect_github.py`を使います。
