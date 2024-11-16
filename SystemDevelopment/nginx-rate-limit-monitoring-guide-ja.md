# Nginxレート制限モニタリング

## はじめに
Webサーバー「Nginx」のレート制限（アクセス制限）機能を監視するための基本的な方法を説明します。

### 重要な用語解説
- **Nginx**: 高性能なWebサーバーソフトウェア
- **レート制限**: サーバーへのアクセス回数を制限する機能
- **429エラー**: アクセス制限に引っかかった際に返されるエラー
- **ログ**: サーバーの動作記録

## 1. 基本設定

Nginxの設定は主に以下のファイルで管理されています：
- メイン設定ファイル: `/etc/nginx/nginx.conf`
- サイト個別の設定: `/etc/nginx/conf.d/*.conf` または `/etc/nginx/sites-available/*`

### 1.1 レート制限の設定

**設定ファイルの場所と編集方法：**
```bash
# 設定ファイルのバックアップを作成（重要）
sudo cp /etc/nginx/nginx.conf /etc/nginx/nginx.conf.backup

# 設定ファイルを編集
sudo nano /etc/nginx/nginx.conf
```

**追加する設定内容：**
```nginx
# /etc/nginx/nginx.conf のhttp{}ブロック内に以下を追加

# レートリミットゾーンの定義
# ここでは全体的なアクセス制限（global）とAPI用の制限（api）を設定
limit_req_zone $binary_remote_addr zone=global:5m rate=3r/s;
limit_req_zone $binary_remote_addr zone=api:5m rate=3r/s;

# レート制限のログレベル設定
limit_req_log_level notice;
```

**設定の詳細説明：**
- `limit_req_zone`: レート制限のルールを定義するディレクティブ
- `$binary_remote_addr`: クライアントのIPアドレスをキーとして使用
- `zone=global:5m`: 
  - `global`という名前のゾーンを作成
  - `5m`は5MBのメモリを割り当て（約32,000のIPアドレスを記録可能）
- `rate=3r/s`: 1秒あたり3リクエストまで許可

### 1.2 ログ設定

**基本的なログ設定：**
```nginx
# /etc/nginx/nginx.conf のhttp{}ブロック内に以下を追加

# アクセスログのフォーマットを定義
log_format monitoring '$remote_addr - $remote_user [$time_local] '
                    '"$request" $status $body_bytes_sent '
                    '"$http_referer" "$http_user_agent" '
                    '$request_time '                    # リクエスト処理時間
                    '$limit_req_status '               # レート制限状態
                    '$connection '                     # コネクション番号
                    '$connection_requests '            # 現在のコネクションでのリクエスト数
                    'upstream_response_time $upstream_response_time ' # upstream（バックエンド）の応答時間
                    'upstream_addr $upstream_addr';    # upstream（バックエンド）のアドレス

# ログファイルの出力設定
access_log /var/log/nginx/access.log monitoring buffer=32k flush=5s;
error_log /var/log/nginx/error.log notice;

# レート制限に特化したログを別ファイルに出力（オプション）
map $status $loggable {
    429     1;
    default 0;
}

access_log /var/log/nginx/ratelimit.log monitoring if=$loggable buffer=16k flush=5s;
```

### 1.2.1 ログローテーションの設定

```plaintext
# /etc/logrotate.d/nginx に以下の設定を作成
/var/log/nginx/*.log {
    daily                   # 毎日ローテーション
    missingok              # ログファイルが存在しなくてもエラーを出さない
    rotate 14              # 14世代分保持
    compress               # 古いログを圧縮
    delaycompress          # 最新の古いログは圧縮しない
    notifempty            # 空のログファイルはローテーションしない
    create 0640 nginx adm  # 新しいログファイルのパーミッションとオーナー設定
    sharedscripts         # 全てのログのローテーション後に1回だけスクリプトを実行
    postrotate            # ローテーション後のスクリプト
        if [ -f /var/run/nginx.pid ]; then
            kill -USR1 `cat /var/run/nginx.pid`
        fi
    endscript
    
    # 容量ベースのローテーション（オプション）
    size 100M             # 100MBを超えたらローテーション
}
```

### 1.2.2 ログ出力例と変数の説明

```plaintext
# 通常のアクセスログの出力例
192.168.1.100 - user123 [15/Mar/2024:10:15:30 +0900] "GET /api/users HTTP/1.1" 200 1534 "https://example.com" "Mozilla/5.0 (Windows NT 10.0; Win64; x64)" 0.002 - 1 3 upstream_response_time 0.001 upstream_addr 10.0.0.10:8080

# レート制限エラーログの出力例
192.168.1.101 - - [15/Mar/2024:10:15:31 +0900] "GET /api/users HTTP/1.1" 429 198 "-" "curl/7.68.0" 0.000 limiting 2 8 upstream_response_time - upstream_addr -

# 各変数の説明
- $remote_addr: "192.168.1.100" - クライアントのIPアドレス
- $remote_user: "user123" - 認証されたユーザー名（認証がない場合は "-"）
- $time_local: "[15/Mar/2024:10:15:30 +0900]" - リクエスト時刻
- $request: "GET /api/users HTTP/1.1" - リクエストライン
- $status: "200" or "429" - HTTPステータスコード
- $body_bytes_sent: "1534" - 送信されたボディのバイト数
- $http_referer: "https://example.com" - リファラー
- $http_user_agent: "Mozilla/5.0..." - ユーザーエージェント
- $request_time: "0.002" - リクエスト処理時間（秒）
- $limit_req_status: "limiting" - レート制限状態（制限時のみ値が設定される）
- $connection: "1" - コネクション番号
- $connection_requests: "3" - 現在のコネクションでのリクエスト数
- $upstream_response_time: "0.001" - バックエンドの応答時間
- $upstream_addr: "10.0.0.10:8080" - バックエンドのアドレス
```

### 1.2.3 ログ分析のためのコマンド例

```bash
# レート制限エラーの時間帯別集計
awk '$9 == "429" {print $4}' /var/log/nginx/access.log | cut -d: -f2 | sort | uniq -c

# 特定IPからのアクセス頻度確認
awk '{print $1}' /var/log/nginx/access.log | sort | uniq -c | sort -nr | head -n 10

# レスポンスタイムの統計
awk '{print $11}' /var/log/nginx/access.log | sort -n | awk '{count[NR] = $1; sum += $1} END {print "Min:", count[1], "\nMax:", count[NR], "\nAvg:", sum/NR}'
```

### 1.3 サイト個別の設定例

**特定のサイトやAPIにレート制限を適用する場合：**
```nginx
# /etc/nginx/conf.d/example.conf または
# /etc/nginx/sites-available/example の server{}ブロック内に追加

server {
    listen 80;
    server_name example.com;

    # 全体的なレート制限
    location / {
        limit_req zone=global burst=5 nodelay;
        
        # その他の設定...
    }

    # API専用のレート制限
    location /api/ {
        limit_req zone=api burst=3 nodelay;
        
        # その他のAPI設定...
    }
}
```

**設定の説明：**
- `burst=5`: 一時的なリクエストの突発を5つまで許可
- `nodelay`: バーストリクエストを遅延なく処理
- `location /`: すべてのURLに適用
- `location /api/`: /api/で始まるURLにのみ適用

### 1.4 設定の適用手順

1. **設定ファイルの構文チェック**
```bash
# 設定ファイルの構文エラーをチェック
sudo nginx -t
```

2. **Nginxの再読み込み**
```bash
# エラーがなければ設定を再読み込み
sudo nginx -s reload
```

### 1.5 設定の確認方法

1. **レート制限の動作確認**
```bash
# 短時間に複数のリクエストを送信してテスト
for i in {1..5}; do curl -I http://your-domain.com; done
```

2. **ログの確認**
```bash
# アクセスログの確認
sudo tail -f /var/log/nginx/access.log

# エラーログの確認
sudo tail -f /var/log/nginx/error.log
```

### 1.6 トラブルシューティング

**よくある問題と解決方法：**

1. **設定ファイルが見つからない場合**
```bash
# Nginxの設定ファイルの場所を確認
nginx -t
```

2. **パーミッションエラーの場合**
```bash
# ログディレクトリのパーミッションを修正
sudo chmod 755 /var/log/nginx
sudo chown -R nginx:nginx /var/log/nginx
```

3. **設定が反映されない場合**
```bash
# Nginxを完全に再起動
sudo systemctl restart nginx
```

### 1.7 セキュリティのベストプラクティス

1. **バックアップの作成**
- 設定変更前に必ずバックアップを作成
- 定期的なバックアップの自動化を検討

2. **適切な制限値の設定**
- サービスの性質に応じた適切なレート制限を設定
- 段階的に制限を調整

3. **監視の設定**
- ログローテーションの設定
- アラートの設定

### 1.8 注意事項

- 本番環境での変更は慎重に行う
- まずはテスト環境で設定をテスト
- 変更後は必ずログを確認
- 急激な設定変更は避け、段階的に調整

これらの設定により、基本的なレート制限とログ監視の環境が整います。実際の運用では、サービスの特性に応じて適切な値に調整することが重要です。

## 2. 基本的な監視コマンド

### 2.1 リアルタイムログ監視
```bash
# アクセスログのリアルタイム監視
tail -f /var/log/nginx/access.log
```
**使い方のポイント:**
- `-f`オプションで最新のログをリアルタイムに表示
- 画面に新しいログが随時追加表示される
- Ctrl+Cで監視を終了

### 2.2 統計情報の収集
```bash
# 429エラーの数を確認
grep " 429 " /var/log/nginx/access.log | wc -l
```
**コマンドの解説:**
- `grep`: 特定のパターンを検索
- `wc -l`: 行数をカウント
- `|`: 左のコマンドの出力を右のコマンドに渡す

## 3. シンプルな監視スクリプト

### 3.1 基本的な監視スクリプト
```bash
#!/bin/bash

# 設定
ACCESS_LOG="/var/log/nginx/access.log"
ERROR_LOG="/var/log/nginx/error.log"
INTERVAL=5  # 監視間隔（秒）

# 関数：タイムスタンプの取得
get_timestamp() {
    date "+%Y-%m-%d %H:%M:%S"
}

# 関数：レート制限エラー（429）の数を取得
get_rate_limit_errors() {
    grep " 429 " "$ACCESS_LOG" | wc -l
}

# 関数：Nginxプロセス数の取得
get_nginx_processes() {
    pgrep nginx | wc -l
}

# 関数：メモリ使用量の取得（MB単位）
get_memory_usage() {
    free -m | awk 'NR==2{printf "%.1f%%", $3*100/$2}'
}

# メイン処理
while true; do
    clear
    echo "=== Nginx監視レポート ===="
    echo "時刻: $(get_timestamp)"
    echo "------------------------"
    echo "レート制限エラー数: $(get_rate_limit_errors)"
    echo "Nginxプロセス数: $(get_nginx_processes)"
    echo "メモリ使用率: $(get_memory_usage)"
    echo "------------------------"
    sleep $INTERVAL
done
```

### 3.2 使用方法

1. **スクリプトの作成と保存**
```bash
# スクリプトを作成
sudo nano /usr/local/bin/nginx_monitor.sh

# 実行権限を付与
sudo chmod 744 /usr/local/bin/nginx_monitor.sh
```

2. **スクリプトの実行**
```bash
sudo /usr/local/bin/nginx_monitor.sh
```

### 3.3 スクリプトの機能
- 5秒ごとに画面をクリアして最新の情報を表示
- レート制限エラー（429）の発生回数を監視
- 実行中のNginxプロセス数を表示
- システムのメモリ使用率を表示
- タイムスタンプ付きで情報を表示

### 3.4 監視の終了方法
- `Ctrl+C` で監視を終了

### 3.5 カスタマイズ例
- 監視間隔の調整（`INTERVAL`の値を変更）
- 表示項目の追加（CPU使用率など）
- アラート機能の追加（特定の閾値を超えた場合にメール通知など）
- ログファイルへの出力機能の追加

**権限について:**
- `744`: 所有者は実行可能、他のユーザーは読み取りのみ
- 必ずroot権限で実行する必要がある操作には`sudo`を使用

## 4. トラブルシューティング

### 4.1 よくある問題と対処法

**429エラーが多発する場合の確認手順:**
1. エラーの発生頻度を確認
2. 問題のあるIPアドレスを特定
3. アクセスパターンを分析
4. 必要に応じてレート制限を調整

### 4.2 監視のポイント

**重要な監視項目:**
- 429エラーの急激な増加
- 特定IPからの集中アクセス
- システムリソースの使用状況

## 5. 運用のベストプラクティス

### 日常的な監視のコツ
1. 定期的なチェック
   - 朝一番でログを確認
   - 異常値の早期発見が重要
   
2. アラートの設定
   - 重要なエラーは通知を設定
   - しきい値を適切に設定

3. ドキュメント化
   - 発生した問題と対処法を記録
   - チーム内で情報を共有

### 注意事項:
- 重要なコマンドは必ずroot権限（sudo）で実行
- ログファイルのパスは環境により異なる
- 本番環境での変更は必ずバックアップを取ってから
- セキュリティ設定は慎重に行う

---
- Created: 2024-11-17
- Updated: 2024-11-17