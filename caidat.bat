@echo off
REM Cai 1 lan -> may tu lay SDT chua chot moi ngay (Windows).
REM
REM   caidat.bat        -> chay 8h sang hang ngay
REM   caidat.bat 07:00  -> chay 7h sang

setlocal
cd /d "%~dp0"

set "GIO=%~1"
if "%GIO%"=="" set "GIO=08:00"

if not exist ".env" (
  copy ".env.example" ".env" >nul
  echo Da tao file .env. Mo file nay, dan API key Pancake vao roi chay lai.
  echo (Pancake -^> Cau hinh -^> Cau hinh ung dung -^> Webhook ^& API Key^)
  exit /b 1
)

findstr /c:"dan_api_key_cua_ban_vao_day" ".env" >nul
if %errorlevel%==0 (
  echo File .env chua co API key that. Mo .env dan key vao roi chay lai.
  exit /b 1
)

REM Xoa lich cu cua chinh tool nay (neu co) roi cai lai.
schtasks /delete /tn "PancakeChuaChot" /f >nul 2>&1

schtasks /create /tn "PancakeChuaChot" /tr "\"%~dp0chay_hang_ngay.bat\"" /sc daily /st %GIO% /f

echo.
echo Da cai: moi ngay luc %GIO% tu lay so chua chot va ghi len Google Sheet.
echo Xem lich   : schtasks /query /tn "PancakeChuaChot"
echo Chay thu   : schtasks /run /tn "PancakeChuaChot"
echo Go lich    : schtasks /delete /tn "PancakeChuaChot" /f

endlocal
