#!/bin/bash
# =====================================================
#  CAI DAT TU DONG cho macOS - Bot check trung don DiLi
#  Bam dup file nay trong Finder. No se:
#   1. Cai thu vien Python can thiet
#   2. Tao file .env va mo TextEdit de ban dan BOT_TOKEN
#  (Lan dau macOS co the chan: chuot phai -> Open -> Open)
# =====================================================
cd "$(dirname "$0")"

echo "===== BUOC 1/2: Cai thu vien (cho ~1 phut) ====="
python3 -m pip install -r requirements.txt || {
  echo "[!] Cai thu vien loi. Neu macOS hoi cai 'Command Line Developer Tools' thi bam Install roi chay lai file nay."
  read -p "Nhan Enter de thoat..."
  exit 1
}

echo ""
echo "===== BUOC 2/2: Cau hinh ====="
[ -f .env ] || cp .env.example .env
echo "TextEdit sap mo file cau hinh:"
echo "  1. Dan token vao sau dong  BOT_TOKEN=   (lay tu @BotFather)"
echo "  2. Sua INTAKE_SECRET= thanh chuoi bi mat tuy y"
echo "  3. Nhan Cmd+S de luu roi dong lai"
open -e .env

echo ""
echo "===== XONG! Tiep theo: bam dup file chay_bot.command de chay bot ====="
echo "Roi vao nhom Telegram: them bot vao nhom, go /id (bot tu nhan nhom)."
read -p "Nhan Enter de dong cua so nay..."
