#!/bin/bash
# =====================================================
#  DiLi Supplement - Bot check trung don (macOS)
#  Bam dup file nay trong Finder de chay bot 24/7.
#  (Lan dau macOS co the chan: chuot phai -> Open -> Open)
# =====================================================
cd "$(dirname "$0")"

if [ ! -f .env ]; then
  echo "[!] Chua co file .env — bam dup file cai_dat_mac.command truoc!"
  read -p "Nhan Enter de thoat..."
  exit 1
fi

while true; do
  echo "[$(date '+%H:%M:%S %d/%m/%Y')] Dang khoi dong bot..."
  python3 bot.py
  echo "[$(date '+%H:%M:%S %d/%m/%Y')] Bot dung/loi — tu chay lai sau 5 giay (Ctrl+C de thoat han)"
  sleep 5
done
