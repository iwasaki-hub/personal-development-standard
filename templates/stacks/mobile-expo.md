# Stack Add-on: Expo / EAS

- 開始時にExpo SDK、Node、package manager、EAS project ID、ownerを確認。
- Expo Goで確認できる機能とdevelopment buildが必要な機能を区別。
- `npx expo-doctor`, TypeScript, lint, web export / native build等を実装段階に合わせて検証。
- EAS Build / Submit / Update のProduction実行は明示承認を要求。
- ExpoのPreview、iPhone実機確認、ビルド証跡をPRへ記録。
- Apple Developer Program未加入でも可能な範囲と必要な署名/配布要件を区別。
- 実際のプロジェクト設定に合わせてCI、EAS profileとSecretsを別途追加。
