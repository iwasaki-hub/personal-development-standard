# Deployment & Rollback

## 環境
| 環境 | URL/プロジェクト | 自動公開 | 管理者 |
|---|---|---|---|
| Local | TODO | いいえ | TODO |
| Preview | TODO | TODO | TODO |
| Production | TODO | **承認制** | TODO |

## デプロイ前チェック
- [ ] 対象commitとPRを確認
- [ ] CI、必要な手動テストを確認
- [ ] 環境変数とアクセス権限を確認
- [ ] DB migrationの有無・順序・復旧手順を確認
- [ ] 影響とロールバック方法を明確化
- [ ] Production公開の明示承認を得た

## デプロイ手順
TODO: 手動/自動の区別、コマンド、承認者、ログの見方

## ロールバック
TODO: 以前のリリースへの復旧手順。DB変更はコードのロールバックと別途設計。

## 確認
TODO: 公開後のヘルスチェック、実機確認、監視
