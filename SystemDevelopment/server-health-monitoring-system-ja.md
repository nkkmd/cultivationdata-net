# Google Apps Scriptによるサーバー監視システム

## 概要

このシステムはGoogle Apps Scriptを使用して、複数のサーバーの健全性を自動的に監視します。5分ごとにヘルスチェックを実行し、結果をスプレッドシートに記録し、問題が発生した場合はメール通知を送信します。

## システム要件

- Googleアカウント
- Google Apps Script
- Google スプレッドシート

## ソースコード

```javascript
// サーバーの状態を監視するスクリプト
function checkServerHealth() {
  // 監視対象のサーバーURLを設定
  const servers = [
    { name: 'サーバー1', url: 'https://example1.com/health' },
    { name: 'サーバー2', url: 'https://example2.com/health' }
  ];
  
  // 結果を記録するスプレッドシート
  const spreadsheetId = 'YOUR_SPREADSHEET_ID'; // スプレッドシートIDを設定
  const sheet = SpreadsheetApp.openById(spreadsheetId).getActiveSheet();
  
  // 現在の日時
  const timestamp = new Date();
  
  servers.forEach(server => {
    try {
      // HTTPリクエストを送信
      const startTime = new Date().getTime();
      const response = UrlFetchApp.fetch(server.url, {
        muteHttpExceptions: true,
        followRedirects: true,
        validateHttpsCertificates: true,
        timeout: 30 // タイムアウト30秒
      });
      const endTime = new Date().getTime();
      
      // レスポンスタイムを計算（ミリ秒）
      const responseTime = endTime - startTime;
      
      // ステータスコードを取得
      const statusCode = response.getResponseCode();
      
      // 結果を判定
      const status = (statusCode >= 200 && statusCode < 300) ? '正常' : '異常';
      
      // スプレッドシートに記録
      sheet.appendRow([
        timestamp,
        server.name,
        status,
        statusCode,
        responseTime + 'ms',
        response.getContentText().slice(0, 100) // レスポンスの最初の100文字
      ]);
      
      // エラーの場合はメール通知
      if (status === '異常') {
        sendAlertEmail(server.name, statusCode, responseTime);
      }
      
    } catch (error) {
      // エラー発生時の処理
      sheet.appendRow([
        timestamp,
        server.name,
        'エラー',
        'N/A',
        'N/A',
        error.toString()
      ]);
      
      sendAlertEmail(server.name, 'エラー', null, error.toString());
    }
  });
}

// アラートメールを送信する関数
function sendAlertEmail(serverName, statusCode, responseTime, errorMessage = '') {
  const recipient = 'your-email@example.com'; // 通知先メールアドレス
  const subject = `サーバーアラート: ${serverName}`;
  
  let body = `
サーバー名: ${serverName}
時刻: ${new Date().toLocaleString()}
ステータス: エラー
ステータスコード: ${statusCode}
`;

  if (responseTime) {
    body += `レスポンスタイム: ${responseTime}ms\n`;
  }
  
  if (errorMessage) {
    body += `エラー詳細: ${errorMessage}\n`;
  }
  
  MailApp.sendEmail(recipient, subject, body);
}

// トリガーを設定する関数
function setTrigger() {
  // 既存のトリガーをすべて削除
  const triggers = ScriptApp.getProjectTriggers();
  triggers.forEach(trigger => ScriptApp.deleteTrigger(trigger));
  
  // 5分おきに実行するトリガーを設定
  ScriptApp.newTrigger('checkServerHealth')
    .timeBased()
    .everyMinutes(5)
    .create();
}
```

## セットアップ手順

### 1. スプレッドシートの準備

1. 新規スプレッドシートを作成
2. 以下の列を追加：
   - タイムスタンプ
   - サーバー名
   - ステータス
   - ステータスコード
   - レスポンスタイム
   - レスポンス内容

### 2. スクリプトの設定

1. スプレッドシートでツール > スクリプトエディタを開く
2. 提供されたコードをコピー
3. 以下の値を環境に合わせて設定：
   ```javascript
   const spreadsheetId = 'YOUR_SPREADSHEET_ID'; // スプレッドシートID
   const servers = [
     { name: 'サーバー1', url: 'https://example1.com/health' },
     { name: 'サーバー2', url: 'https://example2.com/health' }
   ];
   const recipient = 'your-email@example.com'; // 通知先メール
   ```

### 3. トリガーの設定

1. `setTrigger()`関数を実行
2. 必要な権限を承認

## 主要機能

### ヘルスチェック機能
- HTTPリクエストによる死活監視
- レスポンスタイムの計測
- ステータスコードの確認
- タイムアウト設定（30秒）

### 監視結果の記録
- スプレッドシートへの自動記録
- 時系列データの保存
- エラー情報の詳細な記録

### アラート通知
- 異常検知時のメール通知
- エラー詳細の送信
- カスタマイズ可能な通知条件

## カスタマイズ方法

### 監視間隔の変更
```javascript
ScriptApp.newTrigger('checkServerHealth')
  .timeBased()
  .everyMinutes(10) // 10分間隔に変更する例
  .create();
```

### 監視サーバーの追加
```javascript
const servers = [
  { name: 'サーバー1', url: 'https://example1.com/health' },
  { name: 'サーバー2', url: 'https://example2.com/health' },
  { name: '新規サーバー', url: 'https://example3.com/health' } // 追加
];
```

### アラート条件のカスタマイズ
```javascript
// レスポンスタイムの閾値を設定する例
if (responseTime > 5000) { // 5秒以上の場合
  sendAlertEmail(server.name, statusCode, responseTime);
}
```

## トラブルシューティング

### よくある問題と解決方法

1. スクリプトが実行されない
   - トリガーの設定を確認
   - 権限の承認状態を確認

2. メール通知が届かない
   - メールアドレスの設定を確認
   - Gmailの送信制限を確認

3. エラーログの確認方法
   - Apps Scriptのログビューアーで確認
   - スプレッドシートのエラー列を確認

## セキュリティ考慮事項

- HTTPS証明書の検証を実施
- タイムアウト設定による無限ループ防止
- エラー情報の適切な処理

## メンテナンス

### 定期的な確認項目
- スプレッドシートの容量
- トリガーの動作状況
- エラー通知の適切性

### バックアップ
- スプレッドシートの定期的なバックアップを推奨
- スクリプトコードの保存

## サポートとフィードバック

問題や改善提案がある場合は、以下を確認してください：
- Google Apps Scriptのドキュメント
- スプレッドシートの共有設定
- スクリプトの実行ログ

---
- Created: 2024-12-01
- Updated: 2024-12-01