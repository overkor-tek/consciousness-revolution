@echo off
echo.
echo ===================================
echo   YOUR PERSONAL BRAIN
echo   Consciousness Revolution
echo ===================================
echo.
echo Commands:
echo   brain learn "what you learned"
echo   brain search "topic"
echo   brain patterns
echo   brain stats
echo   brain insight "your insight"
echo   brain export
echo.
echo Type 'brain' followed by a command, or 'exit' to quit.
echo.

cd /d "%~dp0"

:loop
set /p cmd="brain> "
if /i "%cmd%"=="exit" goto end
if /i "%cmd%"=="quit" goto end
python brain.py %cmd%
echo.
goto loop

:end
echo.
echo Brain saved. Goodbye!
pause
