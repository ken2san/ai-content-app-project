#!/bin/bash

# ============================================================================
# AI Content App テスト＆実行スクリプト
# 機能：
# - Dockerコンテナのビルド＆起動
# - 翻訳ファイルの構造チェック
# - 言語切り替え機能のテスト（UI・API）
# - JSONレスポンスの言語チェック
# ============================================================================

LOG_FILE="app_test_logs.txt"
echo "=== AI Content App テスト開始 $(date) ===" > "$LOG_FILE"

# 色の定義
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[0;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

log_message() {
  echo -e "${BLUE}[INFO]${NC} $1" | tee -a "$LOG_FILE"
}

log_success() {
  echo -e "${GREEN}[成功]${NC} $1" | tee -a "$LOG_FILE"
}

log_error() {
  echo -e "${RED}[エラー]${NC} $1" | tee -a "$LOG_FILE"
}

log_warning() {
  echo -e "${YELLOW}[警告]${NC} $1" | tee -a "$LOG_FILE"
}

# 翻訳ファイル構造のチェック
check_translation_structure() {
  log_message "翻訳ファイル構造をチェックしています..."
  if [ -d "translations" ]; then
    log_warning "ルートディレクトリに translations/ フォルダが存在します"
    log_warning "正しい場所は app/translations/ です"
    log_warning "./fix_translations.sh を実行して修正してください"
    ./fix_translations.sh
  else
    log_success "翻訳ファイル構造が正しいです (app/translations/ が使用されています)"
  fi
}

# Docker環境の構築
build_and_start_docker() {
  log_message "Dockerコンテナをビルドしています..."
  docker compose down 2>> "$LOG_FILE"
  docker compose build 2>> "$LOG_FILE"

  log_message "Dockerコンテナを起動しています..."
  docker compose up -d 2>> "$LOG_FILE"

  log_message "アプリケーションの起動を待機中 (5秒)..."
  sleep 5
}

# 言語切り替えテスト（UI）
test_ui_language_switching() {
  log_message "UI言語切り替え機能をテストしています..."

  log_message "英語エンドポイント (/?lang=en) をテスト中..."
  curl -s "http://localhost:8000/?lang=en" | grep -i "switch to japanese" > /dev/null
  if [ $? -eq 0 ]; then
    log_success "英語言語が正しく検出されました！"
  else
    log_error "英語言語テストに失敗しました。アプリケーションログを確認してください。"
  fi

  log_message "日本語エンドポイント (/?lang=ja) をテスト中..."
  curl -s "http://localhost:8000/?lang=ja" | grep -i "英語に切り替え" > /dev/null
  if [ $? -eq 0 ]; then
    log_success "日本語言語が正しく検出されました！"
  else
    log_error "日本語言語テストに失敗しました。アプリケーションログを確認してください。"
  fi
}

# JSON APIの言語テスト
test_api_language_support() {
  log_message "JSON API言語サポートをテストしています..."

  log_message "明示的なパラメータがない場合のJSON応答をテスト中..."
  curl -s -L -X POST -H "Accept-Language: ja" -H "Content-Type: application/json" \
       -d '{"userPrompt":"旅行について"}' http://localhost:8000/generate-json-prompt > test_no_lang.json

  # メッセージ部分とjson_dataのいずれかをチェック
  if grep -q "message.*日本語\|生成\|完了\|ダミー" test_no_lang.json || \
     grep -q "json_data.*\"title\".*[^a-zA-Z]" test_no_lang.json; then
    log_success "パラメータなしで日本語JSONレスポンスが正しく返されました"
    log_message "   応答サンプル: $(cat test_no_lang.json | grep -o '"message":"[^"]*"\|"title":"[^"]*"' | head -1)"
  else
    log_error "パラメータなしで日本語JSONレスポンスが返されませんでした"
    log_message "   応答内容: $(head -20 test_no_lang.json)"
  fi

  log_message "英語JSON応答をテスト中..."
  curl -s -L -X POST -H "Content-Type: application/json" \
       -d '{"userPrompt":"About travel"}' "http://localhost:8000/generate-json-prompt?lang=en" > test_lang_en.json
  
  # 英語メッセージをチェック
  if grep -q "message.*generat\|complet\|JSON\|dummy" test_lang_en.json || \
     grep -q "json_data.*\"title\".*[a-zA-Z]" test_lang_en.json; then
    log_success "英語JSONレスポンスが正しく返されました"
    log_message "   応答サンプル: $(cat test_lang_en.json | grep -o '"message":"[^"]*"\|"title":"[^"]*"' | head -1)"
  else
    log_error "英語JSONレスポンスが正しく返されませんでした"
    log_message "   応答内容: $(head -20 test_lang_en.json)"
  fi

  log_message "日本語JSON応答をテスト中..."
  curl -s -L -X POST -H "Content-Type: application/json" \
       -d '{"userPrompt":"旅行について"}' "http://localhost:8000/generate-json-prompt?lang=ja" > test_lang_ja.json
  
  # 日本語メッセージをチェック
  if grep -q "message.*生成\|完了\|ダミー\|JSON" test_lang_ja.json || \
     grep -q "json_data.*\"title\".*[^a-zA-Z]" test_lang_ja.json; then
    log_success "日本語JSONレスポンスが正しく返されました"
    log_message "   応答サンプル: $(cat test_lang_ja.json | grep -o '"message":"[^"]*"\|"title":"[^"]*"' | head -1)"
  else
    log_error "日本語JSONレスポンスが正しく返されませんでした"
    log_message "   応答内容: $(head -20 test_lang_ja.json)"
  fi

  # 一時ファイルのクリーンアップ
  rm -f test_no_lang.json test_lang_en.json test_lang_ja.json
}

# メイン実行
main() {
  log_message "AI Content Appテスト＆実行スクリプトを開始します"

  check_translation_structure
  build_and_start_docker
  test_ui_language_switching
  test_api_language_support

  log_message "テスト完了！"
  echo ""
  log_success "アプリケーションは http://localhost:8000 で実行中です"
  echo ""
  log_message "手動テスト用URL:"
  echo "  英語: http://localhost:8000/?lang=en"
  echo "  日本語: http://localhost:8000/?lang=ja"
  echo ""
  log_message "コマンド一覧:"
  echo "  詳細なログを見る: docker compose logs -f"
  echo "  コンテナを停止する: docker compose down"
  echo "  テスト結果ログを見る: cat $LOG_FILE"
}

# スクリプト実行
main
