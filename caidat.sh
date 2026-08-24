#!/usr/bin/env bash
# Cài 1 lần -> máy tự lấy SĐT chưa chốt mỗi ngày.
#
#   ./caidat.sh          -> chạy 8h sáng hằng ngày
#   ./caidat.sh 7        -> chạy 7h sáng
#   ./caidat.sh 7 --go   -> cài xong chạy thử luôn

set -euo pipefail

cd "$(dirname "$0")"
THU_MUC="$(pwd)"
GIO="${1:-8}"

if [ ! -f .env ]; then
  cp .env.example .env
  echo "→ Đã tạo file .env. Mở file này, dán API key Pancake vào rồi chạy lại."
  echo "  (Pancake -> Cấu hình -> Cấu hình ứng dụng -> Webhook & API Key)"
  exit 1
fi

if grep -q "dan_api_key_cua_ban_vao_day" .env; then
  echo "! File .env chưa có API key thật. Mở .env dán key vào rồi chạy lại."
  exit 1
fi

chmod +x chay_hang_ngay.sh

DONG_CRON="0 $GIO * * * $THU_MUC/chay_hang_ngay.sh >> $THU_MUC/data/nhat_ky.log 2>&1"

# Gỡ lịch cũ của chính tool này (nếu có) rồi cài lại -> chạy nhiều lần không bị trùng lịch.
( crontab -l 2>/dev/null | grep -v "$THU_MUC/chay_hang_ngay.sh" || true; echo "$DONG_CRON" ) | crontab -

echo "→ Đã cài: mỗi ngày ${GIO}h sáng tự lấy số chưa chốt và ghi lên Google Sheet."
echo "→ Xem lịch đang chạy : crontab -l"
echo "→ Xem nhật ký        : tail -f $THU_MUC/data/nhat_ky.log"
echo "→ Gỡ lịch            : crontab -e  (xoá dòng có chay_hang_ngay.sh)"

if [ "${2:-}" = "--go" ]; then
  echo
  echo "→ Chạy thử ngay:"
  ./chay_hang_ngay.sh
fi
