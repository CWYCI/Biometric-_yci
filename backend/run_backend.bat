@echo off
echo Starting Biometric Attendance System Backend...

:: Activate virtual environment
call ..\venv\Scripts\activate.bat

:: Run the Flask application
python app.py

pause