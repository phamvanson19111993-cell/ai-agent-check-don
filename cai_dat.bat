@echo off
rem ============================================================
rem  CAI DAT TU DONG - Bot check trung don DiLi Supplement
rem  Chi can bam dup file nay. No se:
rem   1. Kiem tra Python (chua co thi mo trang tai ve)
rem   2. Cai thu vien can thiet
rem   3. Tao file .env va mo Notepad de ban dan BOT_TOKEN
rem ============================================================
cd /d %~dp0
title DiLi Bot - Cai dat

echo.
echo ===== BUOC 1/3: Kiem tra Python =====
python --version >nul 2>&1
if errorlevel 1 (
    echo.
    echo [!] May chua cai Python. Dang mo trang tai Python...
    echo     KHI CAI, NHO TICK O "Add Python to PATH" o man hinh dau tien!
    echo     Cai xong, dong cua so nay va bam dup lai file cai_dat.bat
    start https://www.python.org/downloads/
    pause
    exit /b 1
)
python --version
echo OK!

echo.
echo ===== BUOC 2/3: Cai thu vien (cho khoang 1 phut) =====
python -m pip install -r requirements.txt
if errorlevel 1 (
    echo.
    echo [!] Cai thu vien bi loi. Chup man hinh loi o tren gui cho Claude de duoc ho tro.
    pause
    exit /b 1
)
echo OK!

echo.
echo ===== BUOC 3/3: Cau hinh =====
if not exist .env copy .env.example .env >nul
echo Notepad sap mo file cau hinh. Ban chi can:
echo   1. Dan token vao sau dong  BOT_TOKEN=
echo      (Lay token: Telegram - chat @BotFather - /mybots - chon bot - API Token)
echo   2. Sua INTAKE_SECRET= thanh mot chuoi bi mat tuy y
echo   3. REPORT_CHAT_ID de trong, lat nua lay sau
echo   4. Bam Ctrl+S de luu roi dong Notepad
echo.
pause
notepad .env

echo.
echo ============================================================
echo  CAI DAT XONG!
echo  Tiep theo: bam dup file  run_bot.bat  de chay bot.
echo  Sau do vao nhom Telegram, them bot vao nhom, go /id
echo  de lay REPORT_CHAT_ID roi dien vao .env (mo lai Notepad),
echo  tat bot va bam dup run_bot.bat lan nua.
echo ============================================================
pause
