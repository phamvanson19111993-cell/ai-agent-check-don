#!/bin/bash
# ============================================================
#  BAT LAI CHUC NANG NHAN SO TU MESSENGER
#
#  Bam dup file nay. No se tu:
#    1. Tao .env neu chua co
#    2. Dat INTAKE_SECRET (sinh chuoi ngau nhien neu chua dat)
#    3. Va chinh luon mat khau do vao file userscript cho khop
#    4. Kiem tra cong nhan so da mo chua
#
#  Sau khi chay xong, chi con 1 viec tay: dan userscript vao
#  Tampermonkey. Man hinh se chi ro tung buoc.
# ============================================================

cd "$(dirname "$0")" || exit 1

ENV_FILE=".env"
US_FILE="userscript/dili-trung-don.user.js"

echo ""
echo "==============================================="
echo "   BAT LAI NHAN SO TU MESSENGER — DiLi"
echo "==============================================="
echo ""

# ---------- 1. Bao dam co file .env ----------
if [ ! -f "$ENV_FILE" ]; then
  if [ -f ".env.example" ]; then
    cp .env.example "$ENV_FILE"
    echo "[1/4] Chua co .env — da tao moi tu .env.example"
    echo "      ⚠️  NHO dan BOT_TOKEN vao .env sau khi chay xong file nay!"
  else
    echo "[1/4] LOI: khong thay .env lan .env.example"
    echo "      Bam dup chan_doan.command truoc de tai lai code."
    echo ""
    read -r -p "Bam Enter de dong..."
    exit 1
  fi
else
  echo "[1/4] Da co file .env"
fi

# ---------- 2. Dat INTAKE_SECRET ----------
HIEN_TAI=$(grep -E '^INTAKE_SECRET=' "$ENV_FILE" | head -1 | cut -d= -f2-)

if [ -z "$HIEN_TAI" ] || [ "$HIEN_TAI" = "doi-mat-khau-nay-ngay" ]; then
  MOI="dili-$(LC_ALL=C tr -dc 'a-z0-9' </dev/urandom | head -c 24)"
  if grep -qE '^INTAKE_SECRET=' "$ENV_FILE"; then
    perl -pi -e "s|^INTAKE_SECRET=.*|INTAKE_SECRET=$MOI|" "$ENV_FILE"
  else
    printf '\nINTAKE_SECRET=%s\n' "$MOI" >> "$ENV_FILE"
  fi
  echo "[2/4] Da dat mat khau cong nhan so (sinh moi, ngau nhien)"
  SECRET="$MOI"
else
  echo "[2/4] Da co INTAKE_SECRET san — giu nguyen"
  SECRET="$HIEN_TAI"
fi

# ---------- 3. Chinh userscript cho khop ----------
if [ -f "$US_FILE" ]; then
  perl -pi -e "s|^(\s*const INTAKE_SECRET = ).*|\${1}\"$SECRET\";|" "$US_FILE"
  echo "[3/4] Da chinh mat khau trong userscript cho khop voi .env"
else
  echo "[3/4] Khong thay $US_FILE — bo qua buoc nay"
fi

# ---------- 4. Kiem tra cong ----------
echo "[4/4] Kiem tra cong nhan so..."
if curl -s --max-time 3 http://127.0.0.1:8787/health 2>/dev/null | grep -q '"ok"'; then
  CONG="DANG MO"
else
  CONG="DANG DONG"
fi

echo ""
echo "==============================================="
echo "  XONG PHAN TU DONG"
echo "==============================================="
echo ""
echo "Cong nhan so hien tai: $CONG"
echo ""

if [ "$CONG" = "DANG DONG" ]; then
  echo "  → Cong dang dong la BINH THUONG neu bot chua chay,"
  echo "    hoac vua doi mat khau xong."
  echo ""
  echo "  VIEC CAN LAM: TAT cua so Terminal cua bot (neu dang mo),"
  echo "  roi bam dup  chay_bot.command  de khoi dong lai."
  echo "  Doi mat khau ma khong khoi dong lai thi KHONG an."
  echo ""
fi

echo "-----------------------------------------------"
echo " CON 1 VIEC TAY DUY NHAT: dan script vao trinh duyet"
echo "-----------------------------------------------"
echo ""
echo " 1. Mo Tampermonkey → Bang dieu khien (Dashboard)"
echo " 2. Tim dong 'DiLi - Bat SDT nhom Xu ly trung don'"
echo "      - Co roi, dang mo  → chi can gat cong tac cho XANH"
echo "      - Khong thay       → bam dau + , xoa het mau,"
echo "                            roi dan noi dung file:"
echo "                            $(pwd)/$US_FILE"
echo " 3. Bam Cmd+S de luu"
echo " 4. Tampermonkey → Cai dat → Che do: Nang cao"
echo "    → muc Bao mat → cho phep ket noi toi  127.0.0.1"
echo " 5. Quay lai Facebook, bam Cmd+R"
echo "    Mo nhom 'Xu ly trung don DiLi Supplement'"
echo "    → Goc duoi phai phai hien nut  DiLi: DANG BAT SO"
echo "      Neu no mau do (TAM DUNG) thi bam mot cai cho xanh."
echo ""
echo " MAT KHAU da duoc dat GIONG NHAU o ca hai ben roi,"
echo " anh KHONG can tu go lai gi ca."
echo ""
echo "-----------------------------------------------"
echo " THU CHO CHAC"
echo "-----------------------------------------------"
echo " Nhan vao nhom Messenger so:  0976486366"
echo " Trong 3 giay bot phai bao len Telegram: TRUNG - Tran Loan"
echo ""
echo "==============================================="
echo ""
read -r -p "Bam Enter de dong cua so nay..."
