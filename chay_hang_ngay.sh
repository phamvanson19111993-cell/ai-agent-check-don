#!/usr/bin/env bash
# Chạy hằng ngày: lấy SĐT chưa chốt trên Pancake -> CSV + Google Sheet.
#
# Cài đặt 1 lần (macOS/Linux):
#   chmod +x chay_hang_ngay.sh
#   crontab -e
#   # dán dòng dưới -> chạy 8h sáng mỗi ngày:
#   0 8 * * * /duong/dan/toi/ai-agent-check-don/chay_hang_ngay.sh >> /tmp/pancake.log 2>&1

set -euo pipefail

cd "$(dirname "$0")"

# Quét 2 ngày gần nhất để không sót hội thoại cập nhật muộn.
# Trùng số sẽ tự bị loại, chạy lại nhiều lần không sao.
python3 -m pancake_export \
  --days 2 \
  --out "data/sdt_chua_chot.csv" \
  --drive

echo "[$(date '+%d/%m/%Y %H:%M')] xong"
