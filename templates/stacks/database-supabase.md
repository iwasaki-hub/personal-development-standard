# Stack Add-on: Supabase

- プロジェクトID、接続先、env、Data API公開範囲、Auth、RLSの前提を確認。
- migration SQLはPRレビュー対象。ローカル分離環境で適用/復元の検証を優先。
- owner-onlyなどのRLSは実際のA/BユーザーJWTでのアクセス確認が必要。
- `service_role` をアプリや公開環境変数へ入れない。
- Remote migration、schema reset、データ消去は事前承認なしに実行しない。
- ロールバック不能なDDLや既存データへの影響は別途手順を記録。
