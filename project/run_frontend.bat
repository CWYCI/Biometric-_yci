@echo off
echo ====================================
echo Starting Attendance System Frontend
echo ====================================

cd /d "%~dp0"

:: Check if node_modules exists, if not install dependencies
if not exist node_modules (
    echo Installing dependencies...
    call npm install
)

:: Start the development server
echo Starting Next.js development server on http://localhost:3000
call npm run dev

pause