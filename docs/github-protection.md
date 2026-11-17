# GitHub 保護ルール標準 v0.3

## 推奨する運用
1. **mainへの直接pushを避け、PR経由でのみ変更**する。
2. Force pushとbranch deleteを禁止する。
3. CIが存在して正常に実行されたことを確認してから、必須チェックに設定する。
4. Production用GitHub Environmentには承認者、branch制限を設定し、必要に応じてデプロイ先サービス側でもゲートを設定する。
5. PRでリスク、テスト、ロールバックを記録する。

## 初期設定（最低限）
GitHub → Settings → Rules → Rulesets または Branches → Branch protection rule。
- Target: main のみ
- Require a pull request before merging
- Block force pushes; block deletions
- Do not enable bypass for automation bots
- 初回は必須チェックを指定しない。CIのjob名/チェック名が安定したら登録する
- 1人開発では「自分のPRに1承認必須」はマージ不能になり得るため、0 required approvals + 明示的な人間のマージ操作を推奨。別レビュアーが確保できる場合は1承認以上へ

## Rulesetサンプル
`config/github/main-ruleset.example.json` はAPIの参考設定。**自動適用しない**。
そのまま流用せず、repoと現在のGitHubプランに合わせてUIでプレビューし、適用時には別途明示承認を得る。
`required_status_checks` は事前にCIのチェック名と実行を確認して追加する。

## 権限とGitHubプラン
Private repositoryでRulesets等が使えるかはプランと権限に依存する。
403の場合、リポジトリを勝手にPublicへ変更したり、課金設定を変更したりしない。
プラン上適用不能な場合でも、AGENTS.mdとPR運用は継続できるが、**技術的な強制保護は未設定**と記録する。

## 検証
- mainへ直接pushできないことをGitHub UIの設定/Rulesets statusで確認
- PRなしでmainを変更できないことを設定で確認
- CIを必須化した場合、失敗中のマージが拒否されることを確認
- [ ] このリポジトリで保護が有効であることを確認した（未確認なら未チェック）

## 適用対象
Template repositoryから作った新規repoにはRulesets、Secrets、Environment保護が自動継承されないことがある。
毎回個別に確認する。
