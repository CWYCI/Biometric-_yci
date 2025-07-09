# Biometric Attendance System

A comprehensive real-time attendance tracking system that integrates with ZKTeco biometric devices to monitor employee attendance, generate reports, and provide real-time dashboard updates. This project consists of a frontend built with Next.js and a backend built with Flask and PostgreSQL.

## Project Structure

- `/backend` - Flask backend with API endpoints and database interactions
- `/project` - Next.js frontend application

## Prerequisites

- PostgreSQL (installed and running)
- Node.js and npm (for frontend)
- Python 3.8+ (for backend)
- Git (optional, for version control)

## Setup Instructions

### 1. Database Setup

1. Make sure PostgreSQL is installed and running
2. Navigate to the backend directory
3. Run the database setup script:

```bash
cd backend
psql -U postgres -f setup_database.sql
```

This will:
- Create the database if it doesn't exist
- Create all required tables (employees and attendance_logs)
- Set up the necessary schema

### 2. Backend Setup

1. Navigate to the backend directory
2. Create and activate a virtual environment (optional but recommended):

```bash
python -m venv venv
venv\Scripts\activate
```

3. Install the required packages:

```bash
pip install -r requirements.txt
```

4. Configure the `.env` file with your database credentials and other settings

5. Start the backend server:

```bash
run_backend.bat
```

The backend will be available at http://localhost:5000

### 3. Frontend Setup

1. Navigate to the frontend directory
2. Install the required packages:

```bash
cd project
npm install
```

3. Start the development server:

```bash
npm run dev
```

The frontend will be available at http://localhost:3000

### 4. Biometric Device Setup

1. Ensure your ZKTeco biometric devices are connected to the network
2. Configure them with the correct IP addresses (default: 192.168.1.201 and 192.168.1.202)
3. Test the connection to the devices:

```bash
python test_device_connection.py 192.168.1.201
python test_device_connection.py 192.168.1.202
```

4. Register employees to the biometric devices:

```bash
python register_employees.py
```

### 5. Running the Complete System

1. Start the backend server:

```bash
run_backend.bat
```

2. Start the frontend (in a new terminal):

```bash
cd ../project
npm run dev
```

3. Open your browser and navigate to http://localhost:3000

## Monitoring and Maintenance

### Real-time Attendance Monitoring

You can monitor attendance logs in real-time using the monitoring script:

```bash
python monitor_attendance.py
```

This will display a live view of today's attendance records and statistics, refreshing every 5 seconds.

### System Health Check

To verify that all components of the system are working correctly, run the health check script:

```bash
python check_system_health.py
```

This script will check:
- Database connection and tables
- Backend server status
- Biometric device connectivity
- Frontend server status

## Database Schema

The database consists of the following tables:

### employees
- Stores basic employee information
- Fields: id, user_id, name, shift_name, shift_start_time, shift_end_time, team, team_id, device_ip, created_at

### attendance_logs
- Stores all attendance events
- Fields: id, user_id, punch_time, status, device_ip, created_at

## API Endpoints

- `/api/employees` - Get all employees with their current status
- `/api/export-daily` - Generate a daily attendance report (CSV)
- `/api/export-weekly` - Generate a weekly attendance report (CSV)
- `/api/export-monthly` - Generate a monthly attendance report (CSV)
- `/health` - Check the health status of the system

## Real-time Updates

The system uses Socket.IO for real-time updates:

- `employee_update` - Sent when an employee's status changes
- `status_change` - Sent when a status change event occurs
- `attendance_update` - Sent when new attendance logs are added

## Troubleshooting

### Database Connection Issues

1. Verify that PostgreSQL is running
2. Check the database credentials in the `.env` file
3. Run the system health check to verify the connection:

```bash
python check_system_health.py
```

### Biometric Device Issues

1. Ensure the devices are powered on and connected to the network
2. Verify the IP addresses are correct (default: 192.168.1.201 and 192.168.1.202)
3. Check that port 4370 is accessible on the devices
4. Test the connection using the test script:

```bash
python test_device_connection.py 192.168.1.201
```

### Backend Issues

1. Check if the backend is running by visiting http://localhost:5000/health
2. Check the backend logs for errors
3. Verify that all required packages are installed

### Frontend Issues

1. Check if the frontend is running by visiting http://localhost:3000
2. Check the browser console for errors
3. Verify that the frontend is configured to connect to the correct backend URL

For more detailed setup and troubleshooting information, refer to the [Backend Setup Guide](backend/SETUP_GUIDE.md).

## License

This project is proprietary and confidential.