@echo off
rem =====================================================
rem  DiLi Supplement - Bot check trung don (chay 24/7)
rem  Bo file nay (hoac shortcut cua no) vao thu muc Startup:
rem  Nhan Win+R, go: shell:startup , roi keo shortcut vao.
rem =====================================================
cd /d %~dp0
title DiLi Bot - Check trung don

:loop
echo [%date% %time%] Dang khoi dong bot...
python bot.py
echo [%date% %time%] Bot da dung/loi. Tu khoi dong lai sau 5 giay... (Ctrl+C de thoat han)
timeout /t 5 /nobreak >nul
goto loop
