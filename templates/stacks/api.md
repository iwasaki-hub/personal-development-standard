# Stack Add-on: API

- OpenAPI等で契約（schema、認証、エラー、バージョン）を明示。
- Validation、認証、レート制限、リトライ/タイムアウト、エラーハンドリングを検証。
- PRごとにunit / integration / contract testsを設計。
- Secretsとサービス間権限は最小権限。実サービスへの破壊的テストを避ける。
- ログにtoken、個人情報、request bodyをむやみに記録しない。
