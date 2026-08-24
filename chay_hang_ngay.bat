@echo off
REM Chay hang ngay tren Windows: lay SDT chua chot Pancake -> CSV + Google Sheet.
REM
REM Cai dat 1 lan:
REM   1. Mo "Task Scheduler" (Bo lap lich tac vu)
REM   2. Create Basic Task -> Daily -> chon gio (vd 8:00)
REM   3. Action: Start a program -> tro toi file chay_hang_ngay.bat nay
REM
REM Quet 2 ngay gan nhat de khong sot hoi thoai cap nhat muon.
REM Trung so se tu bi loai, chay lai nhieu lan khong sao.

cd /d "%~dp0"

python -m pancake_export --days 2 --out "data\sdt_chua_chot.csv" --drive

echo Xong luc %date% %time%
