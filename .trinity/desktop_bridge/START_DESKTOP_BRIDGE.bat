@echo off
REM START DESKTOP BRIDGE
REM Launches the watcher and opens the UI

echo.
echo  ========================================
echo   DESKTOP CLAUDE BRIDGE
echo  ========================================
echo.

REM Check for watchdog
pip show watchdog >nul 2>&1
if %errorlevel% neq 0 (
    echo Installing watchdog...
    pip install watchdog
)

REM Start watcher in background
echo Starting bridge watcher...
start "Desktop Bridge" cmd /k "python %USERPROFILE%\.claude\trinity_messages\DESKTOP_BRIDGE_WATCHER.py"

REM Open UI
echo Opening bridge UI...
start "" "%USERPROFILE%\.claude\trinity_messages\DESKTOP_BRIDGE_UI.html"

echo.
echo Bridge is running!
echo - Watcher monitors outbox for messages
echo - UI open in browser for copy/paste
echo.
pause
