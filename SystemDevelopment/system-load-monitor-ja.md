# システム負荷監視と自動サービス再起動システム

## 1. システム概要

このシステムは、サーバーのCPUとメモリの使用率を監視し、設定された閾値を超えた場合に自動的にサービスを再起動する機能を提供します。

## 2. 主要コンポーネント

### 2.1 監視スクリプト（load-monitor.sh）
システムリソースを監視し、必要に応じてサービスを再起動するメインスクリプト

```bash
#!/bin/bash

# 設定値
MAX_LOAD=80  # CPU負荷の閾値（%）
MAX_MEM=90   # メモリ使用率の閾値（%）
CHECK_INTERVAL=60  # チェック間隔（秒）

# ログ設定
log() {
    logger -t "service-monitor" "$1"
    echo "$(date '+%Y-%m-%d %H:%M:%S') $1"
}

# システム負荷チェック
check_load() {
    # CPU使用率を取得
    local cpu=$(top -bn1 | grep "Cpu(s)" | awk '{print $2 + $4}' | cut -d. -f1)
    # メモリ使用率を取得
    local mem=$(free | grep Mem | awk '{print ($3/$2) * 100}' | cut -d. -f1)
    
    log "現在の負荷状況 - CPU: ${cpu}%, メモリ: ${mem}%"
    
    # 閾値チェック
    if [ $cpu -gt $MAX_LOAD ] || [ $mem -gt $MAX_MEM ]; then
        return 0  # 負荷過剰
    fi
    return 1  # 正常
}

# サービス再起動
restart_services() {
    log "高負荷を検知しました。サービスの再起動を開始します。"
    
    # 再起動対象外のシステムサービス
    local exclude="systemd.service|systemd-journald.service|sshd.service|network.service"
    
    # 実行中のサービス一覧を取得し再起動
    systemctl list-units --type=service --state=running --no-legend | 
    grep -vE "$exclude" | 
    while read -r unit _; do
        log "再起動: $unit"
        systemctl restart "$unit"
        sleep 2
    done
    
    log "全サービスの再起動が完了しました。"
}

# メイン処理
log "負荷監視を開始します"
while true; do
    if check_load; then
        restart_services
        sleep 300  # 再起動後5分間待機
    fi
    sleep $CHECK_INTERVAL
done
```

### 2.2 systemdサービス設定（load-monitor.service）
監視スクリプトをデーモンとして実行するための設定ファイル

```ini
[Unit]
Description=System Load Monitor and Service Restarter
After=network.target

[Service]
Type=simple
ExecStart=/usr/local/bin/load-monitor.sh
Restart=always
RestartSec=60
User=root

[Install]
WantedBy=multi-user.target
```

## 3. 設定パラメータ

```bash
MAX_LOAD=80     # CPU負荷の閾値（%）
MAX_MEM=90      # メモリ使用率の閾値（%）
CHECK_INTERVAL=60  # チェック間隔（秒）
```

## 4. 主要機能

### 4.1 システム監視機能
- CPU使用率の監視
- メモリ使用率の監視
- 定期的な状態チェック（60秒間隔）

### 4.2 サービス再起動機能
- 全実行中サービスの検出
- 重要システムサービスの保護（再起動対象から除外）
- 順次再起動処理

### 4.3 ログ機能
- システムログへの記録
- 標準出力への表示
- タイムスタンプ付きログ

## 5. インストール手順

1. スクリプトファイルの作成
```bash
sudo nano /usr/local/bin/load-monitor.sh
sudo chmod +x /usr/local/bin/load-monitor.sh
```

2. サービス設定ファイルの作成
```bash
sudo nano /etc/systemd/system/load-monitor.service
```

3. サービスの有効化
```bash
sudo systemctl daemon-reload
sudo systemctl enable load-monitor
sudo systemctl start load-monitor
```

## 6. 運用方法

### 6.1 サービスの状態確認
```bash
sudo systemctl status load-monitor
```

### 6.2 ログの確認
```bash
sudo journalctl -u load-monitor -f
```

### 6.3 サービスの停止
```bash
sudo systemctl stop load-monitor
```

## 7. カスタマイズ

### 7.1 再起動対象外サービスの設定
以下の変数で定義されたサービスは再起動対象から除外されます：
```bash
exclude="systemd.service|systemd-journald.service|sshd.service|network.service"
```

### 7.2 監視閾値の調整
スクリプト冒頭の設定値を環境に応じて調整してください：
- MAX_LOAD：CPU負荷の閾値
- MAX_MEM：メモリ使用率の閾値
- CHECK_INTERVAL：チェック間隔

## 8. トラブルシューティング

### 8.1 サービスが起動しない場合
- スクリプトの実行権限を確認
- ログを確認して詳細なエラーを特定

### 8.2 監視が正常に動作しない場合
- システムログを確認
- CPU/メモリ使用率の取得コマンドが正常に動作するか確認

## 9. 注意事項

- 本番環境への導入前にテスト環境での十分な検証を推奨
- システムの負荷状況に応じて閾値を適切に設定
- 重要なサービスは必ず再起動対象から除外

## 10. 制限事項

- root権限が必要
- systemdを使用するシステムのみ対応
- 特定のLinuxコマンド（top, free）に依存

## 11. セキュリティ考慮事項

- root権限で実行されるため、スクリプトのアクセス権限を適切に設定
- ログファイルのアクセス権限を適切に設定
- セキュリティアップデートの定期的な適用を推奨

---
- Created: 2024-11-29
- Updated: 2024-11-29