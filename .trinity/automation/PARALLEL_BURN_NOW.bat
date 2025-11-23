@echo off
REM PARALLEL BURN - MAX OUT ALL THREE ACCOUNTS
REM Run this on each PC to start coordinated parallel work

echo.
echo  ========================================
echo   PARALLEL CREDIT BURN - TRIPLE TRINITY
echo  ========================================
echo.

REM Set this PC's identity
set /p COMPUTER_ID="Enter this computer's ID (PC1/PC2/PC3): "

cd %USERPROFILE%\100X_DEPLOYMENT

REM Pull latest
echo [1/3] Syncing git...
git pull

REM Start daemon in background
echo [2/3] Starting coordination daemon...
start "Trinity Daemon %COMPUTER_ID%" cmd /k "set COMPUTER_ID=%COMPUTER_ID% && python .trinity\automation\CROSS_COMPUTER_DAEMON.py"

REM Show pending tasks
echo [3/3] Checking task queue...
echo.

python -c "
from pathlib import Path
import json

spawn = Path.home() / '100X_DEPLOYMENT' / '.trinity' / 'spawn_queue'
tasks = Path.home() / '100X_DEPLOYMENT' / '.trinity' / 'tasks' / 'pending'

print('=== SPAWN QUEUE ===')
for f in spawn.glob('*.json'):
    t = json.loads(f.read_text())
    print(f'  [{t.get(\"priority\", \"normal\")}] {t[\"id\"]}')

print()
print('=== PENDING TASKS ===')
if tasks.exists():
    for f in tasks.glob('*.json'):
        t = json.loads(f.read_text())
        print(f'  {t[\"id\"]}: {t.get(\"name\", \"unnamed\")}')
else:
    print('  No pending tasks')
"

echo.
echo ========================================
echo  READY FOR PARALLEL BURN
echo ========================================
echo.
echo Daemon running. Open Claude Code and say:
echo   "Check spawn_queue and execute high priority tasks"
echo.
echo Or spawn work to other PCs:
echo   python -c "from CROSS_COMPUTER_DAEMON import CoordinationDaemon; d=CoordinationDaemon(); d.send_wake_signal('PC2', 'Need parallel help')"
echo.
pause
