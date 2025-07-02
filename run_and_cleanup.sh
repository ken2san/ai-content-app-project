#!/bin/bash

LOG_FILE="docker_test_logs.txt"
TEST_SCRIPT="test_script.sh"

# ログ保存用の関数
echo_log() {
  echo "$1" | tee -a "$LOG_FILE"
}

# ログファイルの初期化
echo "--- ログファイルを初期化します ---" > "$LOG_FILE"
echo_log "--- Docker Compose を起動します (コンテナは自動削除) ---"

# Docker Compose を起動し、ログを保存
docker compose up --build | tee -a "$LOG_FILE"

echo_log "--- アプリケーションが停止しました ---"

# 自動テストスクリプトの実行
echo_log "--- 自動テストスクリプトを実行します ---"
if [ -f "$TEST_SCRIPT" ]; then
  bash "$TEST_SCRIPT" | tee -a "$LOG_FILE"
  echo_log "--- テストスクリプトの実行が完了しました ---"
else
  echo_log "--- テストスクリプトが見つかりませんでした ---"
fi

# Dockerイメージ削除の確認
read -p "関連するDockerイメージも全て削除しますか？ (y/N): " choice

if [[ "$choice" == "y" || "$choice" == "Y" ]]; then
  echo_log "--- Dockerイメージを削除中 ---"
  docker compose down --rmi all | tee -a "$LOG_FILE"
  echo_log "--- イメージの削除が完了しました ---"
else
  echo_log "--- イメージは削除されませんでした ---"
fi

echo_log "--- 処理終了 ---"
