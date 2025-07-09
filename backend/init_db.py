import os
import datetime
from dotenv import load_dotenv
from flask import Flask
from models import db, Employee, Attendance, Device, Team, Shift
from sqlalchemy.exc import IntegrityError

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)

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

# Initialize database
db.init_app(app)

def create_sample_data():
    """
    Create sample data for the database.
    """
    try:
        # Create devices
        device1 = Device(
            name="Main Entrance",
            ip_address="192.168.1.201",
            port=4370,
            is_active=True,
            last_connected=datetime.datetime.now()
        )
        
        device2 = Device(
            name="Side Entrance",
            ip_address="192.168.1.202",
            port=4370,
            is_active=True,
            last_connected=datetime.datetime.now()
        )
        
        db.session.add(device1)
        db.session.add(device2)
        db.session.commit()
        
        # Create teams
        engineering = Team(
            name="Engineering",
            description="Software and hardware engineering team"
        )
        
        marketing = Team(
            name="Marketing",
            description="Marketing and sales team"
        )
        
        hr = Team(
            name="HR",
            description="Human resources team"
        )
        
        db.session.add(engineering)
        db.session.add(marketing)
        db.session.add(hr)
        db.session.commit()
        
        # Create shifts
        morning_shift = Shift(
            name="Morning Shift",
            start_time=datetime.time(8, 0),  # 8:00 AM
            end_time=datetime.time(16, 0),   # 4:00 PM
            break_start=datetime.time(12, 0), # 12:00 PM
            break_end=datetime.time(13, 0)    # 1:00 PM
        )
        
        afternoon_shift = Shift(
            name="Afternoon Shift",
            start_time=datetime.time(12, 0),  # 12:00 PM
            end_time=datetime.time(20, 0),    # 8:00 PM
            break_start=datetime.time(16, 0),  # 4:00 PM
            break_end=datetime.time(17, 0)     # 5:00 PM
        )
        
        night_shift = Shift(
            name="Night Shift",
            start_time=datetime.time(20, 0),  # 8:00 PM
            end_time=datetime.time(4, 0),     # 4:00 AM
            break_start=datetime.time(0, 0),   # 12:00 AM
            break_end=datetime.time(1, 0)      # 1:00 AM
        )
        
        db.session.add(morning_shift)
        db.session.add(afternoon_shift)
        db.session.add(night_shift)
        db.session.commit()
        
        # Create employees
        employees = [
            Employee(
                user_id="EMP001",
                name="John Doe",
                email="john.doe@example.com",
                phone="+1234567890",
                shift_id=morning_shift.id,
                team_id=engineering.id,
                device_id=device1.id
            ),
            Employee(
                user_id="EMP002",
                name="Jane Smith",
                email="jane.smith@example.com",
                phone="+1234567891",
                shift_id=morning_shift.id,
                team_id=marketing.id,
                device_id=device1.id
            ),
            Employee(
                user_id="EMP003",
                name="Bob Johnson",
                email="bob.johnson@example.com",
                phone="+1234567892",
                shift_id=afternoon_shift.id,
                team_id=engineering.id,
                device_id=device2.id
            ),
            Employee(
                user_id="EMP004",
                name="Alice Brown",
                email="alice.brown@example.com",
                phone="+1234567893",
                shift_id=afternoon_shift.id,
                team_id=hr.id,
                device_id=device2.id
            ),
            Employee(
                user_id="EMP005",
                name="Charlie Wilson",
                email="charlie.wilson@example.com",
                phone="+1234567894",
                shift_id=night_shift.id,
                team_id=engineering.id,
                device_id=device1.id
            )
        ]
        
        for employee in employees:
            db.session.add(employee)
        
        db.session.commit()
        
        # Create attendance records
        today = datetime.datetime.now().date()
        yesterday = today - datetime.timedelta(days=1)
        
        # Today's attendance
        attendance_records = [
            # John Doe - on time
            Attendance(
                employee_id=1,
                timestamp=datetime.datetime.combine(today, datetime.time(7, 55)),
                status="Punched_In",
                device_id=device1.id
            ),
            # Jane Smith - late
            Attendance(
                employee_id=2,
                timestamp=datetime.datetime.combine(today, datetime.time(8, 15)),
                status="Punched_In",
                device_id=device1.id
            ),
            # Bob Johnson - on time
            Attendance(
                employee_id=3,
                timestamp=datetime.datetime.combine(today, datetime.time(11, 55)),
                status="Punched_In",
                device_id=device2.id
            ),
            # Alice Brown - late
            Attendance(
                employee_id=4,
                timestamp=datetime.datetime.combine(today, datetime.time(12, 10)),
                status="Punched_In",
                device_id=device2.id
            ),
            # John Doe - break in
            Attendance(
                employee_id=1,
                timestamp=datetime.datetime.combine(today, datetime.time(12, 0)),
                status="Break_In",
                device_id=device1.id
            )
        ]
        
        # Yesterday's attendance
        yesterday_records = [
            # John Doe - late
            Attendance(
                employee_id=1,
                timestamp=datetime.datetime.combine(yesterday, datetime.time(8, 10)),
                status="Punched_In",
                device_id=device1.id
            ),
            # Jane Smith - on time
            Attendance(
                employee_id=2,
                timestamp=datetime.datetime.combine(yesterday, datetime.time(7, 55)),
                status="Punched_In",
                device_id=device1.id
            ),
            # Bob Johnson - late
            Attendance(
                employee_id=3,
                timestamp=datetime.datetime.combine(yesterday, datetime.time(12, 20)),
                status="Punched_In",
                device_id=device2.id
            ),
            # Alice Brown - on time
            Attendance(
                employee_id=4,
                timestamp=datetime.datetime.combine(yesterday, datetime.time(11, 55)),
                status="Punched_In",
                device_id=device2.id
            ),
            # Charlie Wilson - late
            Attendance(
                employee_id=5,
                timestamp=datetime.datetime.combine(yesterday, datetime.time(20, 15)),
                status="Punched_In",
                device_id=device1.id
            )
        ]
        
        for record in attendance_records + yesterday_records:
            db.session.add(record)
        
        db.session.commit()
        
        print("Sample data created successfully!")
        
    except IntegrityError as e:
        db.session.rollback()
        print(f"Error creating sample data: {e}")
        print("Sample data may already exist.")
    except Exception as e:
        db.session.rollback()
        print(f"Error creating sample data: {e}")

if __name__ == '__main__':
    with app.app_context():
        # Create tables
        db.create_all()
        
        # Create sample data
        create_sample_data()