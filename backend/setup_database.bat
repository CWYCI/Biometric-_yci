@echo off
echo Setting up Biometric Attendance System Database...

:: Set PostgreSQL credentials
set PGUSER=postgres
set PGPASSWORD=Admin123@

:: Run the SQL script
echo Running SQL setup script...
psql -f setup_database.sql

IF %ERRORLEVEL% NEQ 0 (
    echo Error: Database setup failed!
    pause
    exit /b %ERRORLEVEL%
)

echo.
echo Database schema created successfully!
echo.

:: Activate virtual environment
call ..\venv\Scripts\activate.bat

:: Run the database initialization script
echo Initializing database with sample data...
python init_db.py

IF %ERRORLEVEL% NEQ 0 (
    echo Error: Database initialization failed!
    pause
    exit /b %ERRORLEVEL%
)

echo.
echo Database setup complete!
echo.

pause