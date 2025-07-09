import os
import json
import datetime
import pandas as pd
from flask import Flask, jsonify, request, Response, send_file
from flask_cors import CORS
from flask_socketio import SocketIO
from dotenv import load_dotenv
from models import db, Employee, Attendance, Device, Team, Shift
from sqlalchemy import func, and_, or_
from device_manager import DeviceManager
from utils import calculate_lateness, format_datetime

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

# Configure database
# Use direct connection parameters
db_params = {
    'dbname': os.getenv('DB_NAME'),
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD'),
    'host': os.getenv('DB_HOST', 'localhost'),
    'port': os.getenv('DB_PORT', '5432')
}

# Create SQLAlchemy engine with direct psycopg2 connection
from sqlalchemy.engine.url import URL
url = URL.create(
    drivername="postgresql+psycopg2",
    username=db_params['user'],
    password=db_params['password'],
    host=db_params['host'],
    port=db_params['port'],
    database=db_params['dbname']
)

# Configure SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = url
print(f"Connecting to database: {app.config['SQLALCHEMY_DATABASE_URI']}")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

# Initialize database
db.init_app(app)

# Initialize Socket.IO
socketio = SocketIO(app, cors_allowed_origins="*")

# Initialize device manager
device_manager = DeviceManager()

# Register devices
device_manager.register_device('192.168.1.201')
device_manager.register_device('192.168.1.202')

# Health check endpoint
@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'ok', 'timestamp': datetime.datetime.now().isoformat()})

# Get all employees
@app.route('/api/employees', methods=['GET'])
def get_employees():
    try:
        # Get current date
        today = datetime.datetime.now().date()
        
        # Create a fresh session for this request
        from sqlalchemy.orm import sessionmaker
        Session = sessionmaker(bind=db.engine)
        session = Session()
        
        # Format the response
        result = []
        
        # Get all employees first
        try:
            employees = session.query(Employee).all()
            session.commit()  # Commit after successful query
        except Exception as e:
            session.rollback()  # Rollback on error
            print(f"Error querying employees: {str(e)}")
            session.close()
            return jsonify({'error': f"Error querying employees: {str(e)}"}), 500
        
        # Process each employee individually with separate transactions
        for employee in employees:
            employee_obj = {
                'id': str(employee.id),
                'userId': employee.user_id if hasattr(employee, 'user_id') else 'Unknown',
                'name': employee.name if hasattr(employee, 'name') else 'Unknown'
            }
            
            # Get employee's shift in a separate transaction
            if employee.shift_id:
                try:
                    with Session() as shift_session:
                        shift = shift_session.query(Shift).get(employee.shift_id)
                        if shift:
                            employee_obj['shiftName'] = shift.name
                            employee_obj['shiftStartTime'] = shift.start_time.strftime('%H:%M')
                            employee_obj['shiftEndTime'] = shift.end_time.strftime('%H:%M')
                except Exception as shift_err:
                    print(f"Error getting shift for employee {employee.id}: {str(shift_err)}")
                    employee_obj['shiftName'] = ''
                    employee_obj['shiftStartTime'] = ''
                    employee_obj['shiftEndTime'] = ''
            else:
                employee_obj['shiftName'] = ''
                employee_obj['shiftStartTime'] = ''
                employee_obj['shiftEndTime'] = ''
            
            # Get employee's team in a separate transaction
            if employee.team_id:
                try:
                    with Session() as team_session:
                        team = team_session.query(Team).get(employee.team_id)
                        if team:
                            employee_obj['team'] = team.name
                            employee_obj['teamId'] = str(team.id)
                except Exception as team_err:
                    print(f"Error getting team for employee {employee.id}: {str(team_err)}")
                    employee_obj['team'] = ''
                    employee_obj['teamId'] = ''
            else:
                employee_obj['team'] = ''
                employee_obj['teamId'] = ''
            
            # Get employee's device in a separate transaction
            if employee.device_id:
                try:
                    with Session() as device_session:
                        device = device_session.query(Device).get(employee.device_id)
                        if device:
                            employee_obj['deviceIp'] = device.ip_address
                            employee_obj['isOnline'] = device_manager.is_device_online(device.ip_address)
                except Exception as device_err:
                    print(f"Error getting device for employee {employee.id}: {str(device_err)}")
                    employee_obj['deviceIp'] = ''
                    employee_obj['isOnline'] = False
            else:
                employee_obj['deviceIp'] = ''
                employee_obj['isOnline'] = False
            
            # Get employee's attendance in a separate transaction
            try:
                with Session() as attendance_session:
                    attendance_records = attendance_session.query(Attendance).filter(
                        Attendance.employee_id == employee.id
                    ).order_by(Attendance.timestamp.desc()).limit(10).all()
                    
                    # Find the first one from today
                    latest_attendance = None
                    for record in attendance_records:
                        if record.timestamp.date() == today:
                            latest_attendance = record
                            break
                    
                    # Set attendance-related fields
                    if latest_attendance:
                        employee_obj['status'] = latest_attendance.status
                        employee_obj['lastPunchDate'] = latest_attendance.timestamp.strftime('%Y-%m-%d')
                        employee_obj['lastPunchTime'] = latest_attendance.timestamp.strftime('%H:%M:%S')
                        
                        # Calculate lateness if punched in
                        if latest_attendance.status == 'Punched_In' and 'shiftStartTime' in employee_obj and employee_obj['shiftStartTime']:
                            try:
                                with Session() as shift_session:
                                    shift = shift_session.query(Shift).get(employee.shift_id) if employee.shift_id else None
                                    if shift:
                                        employee_obj['lateByMinutes'] = calculate_lateness(latest_attendance.timestamp, shift.start_time)
                                    else:
                                        employee_obj['lateByMinutes'] = 0
                            except Exception as late_err:
                                print(f"Error calculating lateness for employee {employee.id}: {str(late_err)}")
                                employee_obj['lateByMinutes'] = 0
                        else:
                            employee_obj['lateByMinutes'] = 0
                    else:
                        employee_obj['status'] = 'Punched_Out'
                        employee_obj['lastPunchDate'] = ''
                        employee_obj['lastPunchTime'] = ''
                        employee_obj['lateByMinutes'] = 0
            except Exception as att_err:
                print(f"Error getting attendance for employee {employee.id}: {str(att_err)}")
                employee_obj['status'] = 'Punched_Out'
                employee_obj['lastPunchDate'] = ''
                employee_obj['lastPunchTime'] = ''
                employee_obj['lateByMinutes'] = 0
            
            # Add the employee object to the result
            result.append(employee_obj)
        
        # Close the main session
        session.close()
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Get yesterday's late comers
@app.route('/api/yesterdays-late-comers', methods=['GET'])
def get_yesterdays_late_comers():
    try:
        # Get yesterday's date
        yesterday = (datetime.datetime.now() - datetime.timedelta(days=1)).date()
        
        # Query all attendance records for yesterday
        yesterday_start = datetime.datetime.combine(yesterday, datetime.time.min)
        yesterday_end = datetime.datetime.combine(yesterday, datetime.time.max)
        
        # Import text from sqlalchemy
        from sqlalchemy import text
        
        # Use raw SQL query with text() to match the actual database schema
        # The database schema uses user_id in attendance table, not employee_id
        query = text("""
        SELECT 
            e.id as employee_id,
            e.user_id,
            e.name,
            t.name as team_name,
            s.name as shift_name,
            s.start_time as shift_start_time,
            a.punch_time as timestamp,
            a.status
        FROM 
            employee e
        JOIN 
            attendance a ON e.user_id = a.user_id
        JOIN 
            shift s ON e.shift_id = s.id
        LEFT JOIN 
            team t ON e.team_id = t.id
        WHERE 
            a.punch_time >= :yesterday_start
            AND a.punch_time <= :yesterday_end
            AND a.status = 'check-in'
        ORDER BY 
            a.punch_time
        """)
        
        result = db.session.execute(query, {
            'yesterday_start': yesterday_start,
            'yesterday_end': yesterday_end
        })
        
        # Calculate lateness for each employee
        late_comers = []
        for row in result:
            # Convert shift_start_time to datetime for the same day as punch_time
            punch_time = row.timestamp
            shift_start_time = row.shift_start_time
            
            # Calculate lateness
            late_by_minutes = calculate_lateness(punch_time, shift_start_time)
            
            # Only include employees who were late
            if late_by_minutes > 0:
                # Create late employee object
                late_employee = {
                    'id': str(row.employee_id),
                    'userId': row.user_id,
                    'name': row.name,
                    'team': row.team_name if row.team_name else '',
                    'shiftName': row.shift_name,
                    'shiftStartTime': row.shift_start_time.strftime('%H:%M'),
                    'lateByMinutes': late_by_minutes
                }
                
                late_comers.append(late_employee)
        
        # Sort by lateness (descending)
        late_comers.sort(key=lambda x: x['lateByMinutes'], reverse=True)
        
        # Return top 10
        return jsonify(late_comers[:10])
    except Exception as e:
        print(f"Error in get_yesterdays_late_comers: {str(e)}")
        return jsonify({'error': str(e)}), 500

# Export daily report
@app.route('/api/export-daily', methods=['GET'])
def export_daily():
    try:
        # Get current date
        today = datetime.datetime.now().date()
        
        # Query all employees with their attendance records for today
        today_start = datetime.datetime.combine(today, datetime.time.min)
        today_end = datetime.datetime.combine(today, datetime.time.max)
        
        employees_data = db.session.query(
            Employee,
            Attendance
        ).outerjoin(
            Attendance,
            and_(
                Employee.id == Attendance.employee_id,
                # Use date range comparison
                Attendance.timestamp >= today_start,
                Attendance.timestamp <= today_end
            )
        ).all()
        
        # Prepare data for CSV
        data = []
        for employee, attendance in employees_data:
            # Get employee's shift
            shift = Shift.query.get(employee.shift_id)
            
            # Get employee's team
            team = Team.query.get(employee.team_id)
            
            # Determine employee status
            status = 'Punched_Out'
            if attendance:
                status = attendance.status
            
            # Format last punch date and time
            last_punch_date = ''
            last_punch_time = ''
            if attendance:
                last_punch_date = attendance.timestamp.strftime('%Y-%m-%d')
                last_punch_time = attendance.timestamp.strftime('%H:%M:%S')
            
            # Create row
            row = {
                'Employee ID': employee.user_id,
                'Name': employee.name,
                'Team': team.name if team else '',
                'Shift': shift.name if shift else '',
                'Shift Start': shift.start_time.strftime('%H:%M') if shift else '',
                'Shift End': shift.end_time.strftime('%H:%M') if shift else '',
                'Status': status,
                'Last Punch Date': last_punch_date,
                'Last Punch Time': last_punch_time
            }
            
            data.append(row)
        
        # Create DataFrame
        df = pd.DataFrame(data)
        
        # Create CSV
        csv_data = df.to_csv(index=False)
        
        # Return CSV file
        return Response(
            csv_data,
            mimetype='text/csv',
            headers={'Content-Disposition': f'attachment; filename=daily_report_{today}.csv'}
        )
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Export weekly report
@app.route('/api/export-weekly', methods=['GET'])
def export_weekly():
    try:
        # Get date range for the current week (Monday to Sunday)
        today = datetime.datetime.now().date()
        start_of_week = today - datetime.timedelta(days=today.weekday())
        end_of_week = start_of_week + datetime.timedelta(days=6)
        
        # Query all attendance records for the current week
        attendance_data = db.session.query(
            Employee,
            Attendance
        ).join(
            Attendance,
            Employee.id == Attendance.employee_id
        ).filter(
            # Use date comparison for better compatibility
            Attendance.timestamp >= datetime.datetime.combine(start_of_week, datetime.time.min),
            Attendance.timestamp <= datetime.datetime.combine(end_of_week, datetime.time.max)
        ).all()
        
        # Prepare data for CSV
        data = []
        for employee, attendance in attendance_data:
            # Get employee's team
            team = Team.query.get(employee.team_id)
            
            # Create row
            row = {
                'Employee ID': employee.user_id,
                'Name': employee.name,
                'Team': team.name if team else '',
                'Date': attendance.timestamp.strftime('%Y-%m-%d'),
                'Time': attendance.timestamp.strftime('%H:%M:%S'),
                'Status': attendance.status
            }
            
            data.append(row)
        
        # Create DataFrame
        df = pd.DataFrame(data)
        
        # Create CSV
        csv_data = df.to_csv(index=False)
        
        # Return CSV file
        return Response(
            csv_data,
            mimetype='text/csv',
            headers={'Content-Disposition': f'attachment; filename=weekly_report_{start_of_week}_to_{end_of_week}.csv'}
        )
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Export monthly report
@app.route('/api/export-monthly', methods=['GET'])
def export_monthly():
    try:
        # Get date range for the current month
        today = datetime.datetime.now().date()
        start_of_month = today.replace(day=1)
        # Calculate end of month
        if today.month == 12:
            end_of_month = today.replace(year=today.year + 1, month=1, day=1) - datetime.timedelta(days=1)
        else:
            end_of_month = today.replace(month=today.month + 1, day=1) - datetime.timedelta(days=1)
        
        # Query all attendance records for the current month
        attendance_data = db.session.query(
            Employee,
            Attendance
        ).join(
            Attendance,
            Employee.id == Attendance.employee_id
        ).filter(
            # Use date comparison for better compatibility
            Attendance.timestamp >= datetime.datetime.combine(start_of_month, datetime.time.min),
            Attendance.timestamp <= datetime.datetime.combine(end_of_month, datetime.time.max)
        ).all()
        
        # Prepare data for CSV
        data = []
        for employee, attendance in attendance_data:
            # Get employee's team
            team = Team.query.get(employee.team_id)
            
            # Create row
            row = {
                'Employee ID': employee.user_id,
                'Name': employee.name,
                'Team': team.name if team else '',
                'Date': attendance.timestamp.strftime('%Y-%m-%d'),
                'Time': attendance.timestamp.strftime('%H:%M:%S'),
                'Status': attendance.status
            }
            
            data.append(row)
        
        # Create DataFrame
        df = pd.DataFrame(data)
        
        # Create CSV
        csv_data = df.to_csv(index=False)
        
        # Return CSV file
        return Response(
            csv_data,
            mimetype='text/csv',
            headers={'Content-Disposition': f'attachment; filename=monthly_report_{today.strftime("%Y-%m")}.csv'}
        )
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Socket.IO event handlers
@socketio.on('connect')
def handle_connect():
    print('Client connected')

@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')

# Start the server
if __name__ == '__main__':
    with app.app_context():
        # Create tables if they don't exist
        db.create_all()
    
    # Start Socket.IO server directly on port 5001 since port 5000 is already in use
    port = 5001
    print(f"Starting server on port {port}...")
    socketio.run(app, host='0.0.0.0', port=port, debug=os.getenv('DEBUG', 'False').lower() == 'true')