# Biometric Attendance System Backend

This is the backend server for the Biometric Attendance System. It provides API endpoints for the frontend to fetch employee data, attendance records, and real-time updates via Socket.IO.

## Features

- RESTful API endpoints for employee data
- Real-time updates via Socket.IO
- PostgreSQL database integration
- Biometric device integration (ZKTeco)
- Authentication and authorization
- Report generation

## Setup

1. Create a virtual environment: `python -m venv venv`
2. Activate the virtual environment: 
   - Windows: `venv\Scripts\activate`
   - Linux/Mac: `source venv/bin/activate`
3. Install dependencies: `pip install -r requirements.txt`
4. Set up environment variables in `.env` file
5. Initialize the database: `python init_db.py`
6. Run the server: `python app.py`

## Environment Variables

Create a `.env` file in the backend directory with the following variables:

```
DB_HOST=localhost
DB_PORT=5432
DB_NAME=Attendance_YCI
DB_USER=postgres
DB_PASSWORD=Admin123@
SECRET_KEY=your_secret_key
DEBUG=True
```

## API Endpoints

- `GET /api/employees` - Get all employees
- `GET /api/yesterdays-late-comers` - Get yesterday's late comers
- `GET /api/export-daily` - Export daily report
- `GET /api/export-weekly` - Export weekly report
- `GET /api/export-monthly` - Export monthly report
- `GET /health` - Health check endpoint

## Socket.IO Events

- `connect` - Client connected
- `disconnect` - Client disconnected
- `employee_update` - Employee status update

## Biometric Devices

The system is configured to connect to the following biometric devices:

- Device 1: 192.168.1.201
- Device 2: 192.168.1.202
