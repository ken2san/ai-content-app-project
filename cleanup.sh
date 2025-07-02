#!/bin/bash

# ============================================================================
# AI Content App クリーンアップスクリプト
# 機能：
# - 重複したテストスクリプトの削除
# - 一時ファイル・ログの削除
# ============================================================================

# 色の定義
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[0;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

log_message() {
  echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
  echo -e "${GREEN}[成功]${NC} $1"
}

log_warning() {
  echo -e "${YELLOW}[警告]${NC} $1"
}

# 削除する重複テストスクリプト
DUPLICATE_TEST_SCRIPTS=(
  "test_language_fix.sh"
  "test_language_switching.sh"
  "run_and_cleanup.sh"
)

# 削除する一時ファイル
TEMP_FILES=(
  "cookie.txt"
  "docker_test_logs.txt"
  "en_response.json"
  "ja_response.json"
)

# 確認メッセージを表示
echo "以下のファイルを削除しようとしています："
echo ""
echo "重複テストスクリプト:"
for file in "${DUPLICATE_TEST_SCRIPTS[@]}"; do
  if [ -f "$file" ]; then
    echo "  - $file"
  fi
done

echo ""
echo "一時ファイル:"
for file in "${TEMP_FILES[@]}"; do
  if [ -f "$file" ]; then
    echo "  - $file"
  fi
done

echo ""
read -p "これらのファイルを削除してもよろしいですか？ (y/N): " confirm

if [[ "$confirm" != "y" && "$confirm" != "Y" ]]; then
  log_warning "クリーンアップをキャンセルしました"
  exit 0
fi

# ファイル削除
for file in "${DUPLICATE_TEST_SCRIPTS[@]}"; do
  if [ -f "$file" ]; then
    rm "$file"
    log_success "$file を削除しました"
  fi
done

for file in "${TEMP_FILES[@]}"; do
  if [ -f "$file" ]; then
    rm "$file"
    log_success "$file を削除しました"
  fi
done

log_message "クリーンアップが完了しました"
log_message "今後は test_app.sh を使用してアプリケーションのテストと実行を行ってください"
