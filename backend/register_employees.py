import os
import sys
import time
import psycopg2
import psycopg2.extras
from dotenv import load_dotenv
from zk import ZK, const

# Load environment variables
load_dotenv()

def get_db_connection():
    """
    Create a connection to the PostgreSQL database.
    """
    # Get database connection parameters from environment variables
    db_host = os.getenv('DB_HOST', 'localhost')
    db_port = os.getenv('DB_PORT', '5432')
    db_name = os.getenv('DB_NAME', 'Attendance_YCI')
    db_user = os.getenv('DB_USER', 'postgres')
    db_password = os.getenv('DB_PASSWORD', 'Admin123@')
    
    # Connect to the database
    conn = psycopg2.connect(
        host=db_host,
        port=db_port,
        dbname=db_name,
        user=db_user,
        password=db_password
    )
    
    return conn

def get_employees():
    """
    Get all employees from the database.
    """
    try:
        # Connect to the database
        conn = get_db_connection()
        
        # Create a cursor with dictionary-like results
        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        
        # Query to get all employees
        query = """
        SELECT 
            id, 
            user_id, 
            name, 
            device_ip
        FROM 
            employee
        ORDER BY 
            id
        """
        
        # Execute the query
        cursor.execute(query)
        
        # Fetch all records
        employees = cursor.fetchall()
        
        # Close the cursor and connection
        cursor.close()
        conn.close()
        
        return employees
    
    except Exception as e:
        print(f"Error getting employees: {e}")
        return []

def connect_to_device(ip_address, port=4370, timeout=5):
    """
    Connect to a ZKTeco biometric device.
    
    Args:
        ip_address (str): The IP address of the device
        port (int): The port number (default: 4370)
        timeout (int): Connection timeout in seconds (default: 5)
        
    Returns:
        tuple: (ZK instance, connection object) if successful, (None, None) otherwise
    """
    # Create a ZK instance
    zk = ZK(ip_address, port=port, timeout=timeout)
    
    try:
        # Connect to the device
        conn = zk.connect()
        return zk, conn
    
    except Exception as e:
        print(f"Error connecting to device at {ip_address}: {e}")
        return None, None

def register_employee(conn, user_id, name):
    """
    Register an employee to a biometric device.
    
    Args:
        conn: The device connection object
        user_id (str): The employee's user ID
        name (str): The employee's name
        
    Returns:
        bool: True if registration successful, False otherwise
    """
    try:
        # Convert user_id to integer
        uid = int(user_id)
        
        # Check if user already exists
        users = conn.get_users()
        for user in users:
            if user.user_id == uid:
                print(f"User {uid} ({name}) already exists on the device.")
                return True
        
        # Create the user
        conn.set_user(uid=uid, name=name, privilege=const.USER_DEFAULT, password='', group_id='', user_id=str(uid))
        print(f"Successfully registered user {uid} ({name}) to the device.")
        return True
    
    except Exception as e:
        print(f"Error registering user {user_id} ({name}): {e}")
        return False

def register_employees_to_devices():
    """
    Register all employees to their assigned biometric devices.
    """
    # Get all employees
    employees = get_employees()
    
    if not employees:
        print("No employees found in the database.")
        return False
    
    print(f"Found {len(employees)} employees in the database.")
    
    # Group employees by device IP
    employees_by_device = {}
    for employee in employees:
        device_ip = employee['device_ip']
        if device_ip not in employees_by_device:
            employees_by_device[device_ip] = []
        employees_by_device[device_ip].append(employee)
    
    # Process each device
    success = True
    for device_ip, device_employees in employees_by_device.items():
        print(f"\nProcessing device at {device_ip} with {len(device_employees)} employees...")
        
        # Connect to the device
        zk, conn = connect_to_device(device_ip)
        
        if conn:
            try:
                # Get device information
                info = conn.get_device_info()
                print(f"Connected to device: {info.device_name} (SN: {info.serial_number})")
                
                # Register each employee
                for employee in device_employees:
                    register_employee(conn, employee['user_id'], employee['name'])
                
                # Disconnect from the device
                conn.disconnect()
            
            except Exception as e:
                print(f"Error processing device at {device_ip}: {e}")
                success = False
        else:
            print(f"Failed to connect to device at {device_ip}.")
            success = False
    
    return success

def main():
    """
    Main function to register employees to biometric devices.
    """
    print("\n" + "=" * 80)
    print(" BIOMETRIC ATTENDANCE SYSTEM - EMPLOYEE REGISTRATION ".center(80, "="))
    print("=" * 80 + "\n")
    
    # Register employees to devices
    success = register_employees_to_devices()
    
    # Print summary
    print("\n" + "-" * 80)
    if success:
        print("✅ EMPLOYEE REGISTRATION COMPLETED SUCCESSFULLY")
    else:
        print("❌ EMPLOYEE REGISTRATION COMPLETED WITH ERRORS")
    print("-" * 80 + "\n")
    
    return success

if __name__ == '__main__':
    # Run the registration process
    success = main()
    
    # Exit with appropriate status code
    sys.exit(0 if success else 1)