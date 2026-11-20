@echo off
setlocal enabledelayedexpansion

echo ========================================================
echo        RideBook AI - Django Server Launcher
echo ========================================================
echo.
echo Starting RideBook AI Server on port 5000...
echo.

:: Automatically open browser after 2 seconds in the background
start "" /b cmd /c "timeout /t 2 /nobreak >nul && start http://127.0.0.1:5000"

:: Start Django Server
python manage.py runserver 0.0.0.0:5000

pause
