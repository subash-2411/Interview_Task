@echo off
echo Stopping RideBook AI Django Server...
for /f "tokens=5" %%a in ('netstat -aon ^| find ":5000" ^| find "LISTENING"') do (
    taskkill /F /PID %%a
)
echo Server stopped successfully.
pause
