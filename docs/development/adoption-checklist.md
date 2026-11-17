# Adoption Checklist

## 新規リポジトリ
- [ ] GitHubの「Template repository」を有効化
- [ ] 新repoを「Use this template」で作成
- [ ] READMEのテンプレ説明をプロジェクト説明に変更
- [ ] docsのTODOを埋める
- [ ] `.env.example` をプロジェクトに合わせる（秘密情報なし）
- [ ] Rulesetでmain保護、PRレビュー、必要なCIを必須にする
- [ ] Actionsの権限を最小限にする
- [ ] 必要な技術別CIを追加して動作確認
- [ ] Production環境で承認者と保護ルールを設定

## 既存リポジトリ
- [ ] 現状のAGENTS/CI/deployment運用を棚卸し
- [ ] 差分を先に確認し、既存ファイルを上書きしない
- [ ] 小さなPRに分けて段階導入
- [ ] CIと権限の変更が既存デプロイを壊さないことを確認

## 注意
- GitHub設定はテンプレファイルのコピーでは引き継がれないものがある。
- Branch protection/Rulesets、Secrets、Environments、外部サービス設定は新repoで個別に確認する。
