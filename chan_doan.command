#!/bin/bash
# ============================================================
#  BAC SI TU DONG - DiLi Bot (macOS)
#  Tu tai code moi nhat -> chay bot -> bat benh -> mo ket qua
#  bang TextEdit de nguoi dung chup gui cho Claude.
# ============================================================
DIR="$HOME/Desktop/ai-agent-check-don-claude-telegram-duplicate-order-bot-ayyubm"
LOG="/tmp/dili-chandoan.txt"
ZIPURL="https://codeload.github.com/phamvanson19111993-cell/ai-agent-check-don/zip/refs/heads/claude/telegram-duplicate-order-bot-ayyubm"

{
  echo "=========== CHAN DOAN DiLi BOT ==========="
  date
  echo ""
  echo "--- 1. Cap nhat code moi nhat tu GitHub ---"
  curl -sL -o /tmp/dili.zip "$ZIPURL" && unzip -oq /tmp/dili.zip -d "$HOME/Desktop" \
    && echo "OK: da tai va giai nen ban moi nhat" \
    || echo "LOI: khong tai duoc code (kiem tra mang)"
  echo ""

  cd "$DIR" 2>/dev/null || { echo "LOI: khong thay thu muc $DIR"; exit 1; }

  echo "--- 2. Kiem tra moi truong ---"
  echo "Python: $(python3 --version 2>&1)"
  if grep -q '^BOT_TOKEN=..*' .env 2>/dev/null; then
    echo "Token trong .env: CO"
  else
    echo "Token trong .env: THIEU! (can dan BOT_TOKEN vao file .env)"
  fi
  python3 -c "import telegram, aiohttp, dotenv, requests" 2>&1 \
    && echo "Thu vien: DU" \
    || { echo "Thu vien: THIEU -> dang tu cai..."; python3 -m pip -q install -r requirements.txt && echo "Da cai xong thu vien"; }
  echo ""

  echo "--- 3. Khoi dong bot (cho 12 giay) ---"
} > "$LOG" 2>&1

cd "$DIR" 2>/dev/null
python3 bot.py >> "$LOG" 2>&1 &
BOTPID=$!
sleep 12

if kill -0 "$BOTPID" 2>/dev/null; then
  {
    echo ""
    echo "==========================================="
    echo "🎉 KET QUA: BOT DANG CHAY TOT!"
    echo "DUNG DONG cua so Terminal. Vao Telegram:"
    echo "  1) Them @dili_check_trung_bot vao nhom"
    echo "  2) Go /id trong nhom"
    echo "  3) Go /check 0976486366 -> phai ra TRUNG (Tran Loan)"
    echo "==========================================="
  } >> "$LOG" 2>&1
  open -e "$LOG"
  wait "$BOTPID"
else
  {
    echo ""
    echo "==========================================="
    echo "❌ KET QUA: BOT DA THOAT — loi nam o cac dong phia tren."
    echo "Hay CHUP MAN HINH cua so nay gui cho Claude de duoc sua."
    echo "==========================================="
  } >> "$LOG" 2>&1
  open -e "$LOG"
fi
