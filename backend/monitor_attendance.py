import os
import sys
import time
import datetime
import psycopg2
import psycopg2.extras
from dotenv import load_dotenv
from tabulate import tabulate
from colorama import init, Fore, Style

# Initialize colorama for colored terminal output
init()

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

def get_today_attendance():
    """
    Get today's attendance records from the database.
    """
    # Get today's date
    today = datetime.date.today()
    
    try:
        # Connect to the database
        conn = get_db_connection()
        
        # Create a cursor with dictionary-like results
        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        
        # Query to get today's attendance with employee information
        query = """
        SELECT 
            a.id, 
            e.name, 
            e.user_id, 
            a.punch_time, 
            a.status, 
            a.device_ip,
            e.team,
            e.shift_name
        FROM 
            attendance a
        JOIN 
            employee e ON a.user_id = e.user_id
        WHERE 
            DATE(a.punch_time) = %s
        ORDER BY 
            a.punch_time DESC
        """
        
        # Execute the query
        cursor.execute(query, (today,))
        
        # Fetch all records
        records = cursor.fetchall()
        
        # Close the cursor and connection
        cursor.close()
        conn.close()
        
        return records
    
    except Exception as e:
        print(f"Error getting attendance records: {e}")
        return []

def get_attendance_statistics():
    """
    Get attendance statistics for today.
    """
    # Get today's date
    today = datetime.date.today()
    
    try:
        # Connect to the database
        conn = get_db_connection()
        
        # Create a cursor
        cursor = conn.cursor()
        
        # Query to get total employees
        cursor.execute("SELECT COUNT(*) FROM employee")
        total_employees = cursor.fetchone()[0]
        
        # Query to get employees who have punched in today
        cursor.execute("""
        SELECT COUNT(DISTINCT user_id) 
        FROM attendance 
        WHERE DATE(punch_time) = %s
        """, (today,))
        present_employees = cursor.fetchone()[0]
        
        # Calculate absent employees
        absent_employees = total_employees - present_employees
        
        # Query to get employees who are currently working
        cursor.execute("""
        SELECT COUNT(DISTINCT user_id) 
        FROM attendance 
        WHERE DATE(punch_time) = %s 
        AND status = 'check-in'
        """, (today,))
        working_employees = cursor.fetchone()[0]
        
        # Query to get employees who are on break
        cursor.execute("""
        SELECT COUNT(DISTINCT user_id) 
        FROM attendance 
        WHERE DATE(punch_time) = %s 
        AND status = 'break'
        """, (today,))
        break_employees = cursor.fetchone()[0]
        
        # Query to get employees who have checked out
        cursor.execute("""
        SELECT COUNT(DISTINCT user_id) 
        FROM attendance 
        WHERE DATE(punch_time) = %s 
        AND status = 'check-out'
        """, (today,))
        checked_out_employees = cursor.fetchone()[0]
        
        # Close the cursor and connection
        cursor.close()
        conn.close()
        
        return {
            'total': total_employees,
            'present': present_employees,
            'absent': absent_employees,
            'working': working_employees,
            'on_break': break_employees,
            'checked_out': checked_out_employees
        }
    
    except Exception as e:
        print(f"Error getting attendance statistics: {e}")
        return {
            'total': 0,
            'present': 0,
            'absent': 0,
            'working': 0,
            'on_break': 0,
            'checked_out': 0
        }

def display_attendance_monitor(refresh_interval=5):
    """
    Display a real-time attendance monitor that refreshes at the specified interval.
    
    Args:
        refresh_interval (int): Refresh interval in seconds (default: 5)
    """
    try:
        while True:
            # Clear the screen
            os.system('cls' if os.name == 'nt' else 'clear')
            
            # Get current time
            now = datetime.datetime.now()
            
            # Print header
            print("\n" + "=" * 80)
            print(f" BIOMETRIC ATTENDANCE SYSTEM - REAL-TIME MONITOR ".center(80, "="))
            print("=" * 80)
            print(f"\n{Fore.YELLOW}Date: {now.strftime('%Y-%m-%d')}  Time: {now.strftime('%H:%M:%S')}{Style.RESET_ALL}")
            print(f"Refreshing every {refresh_interval} seconds. Press Ctrl+C to exit.\n")
            
            # Get attendance statistics
            stats = get_attendance_statistics()
            
            # Display statistics
            print("\n" + "-" * 80)
            print(" ATTENDANCE STATISTICS ".center(80, "-"))
            print("-" * 80)
            print(f"\n{Fore.CYAN}Total Employees:{Style.RESET_ALL} {stats['total']}")
            print(f"{Fore.GREEN}Present:{Style.RESET_ALL} {stats['present']} ({stats['present']/stats['total']*100:.1f}%% if stats['total'] > 0 else 0%%)")
            print(f"{Fore.RED}Absent:{Style.RESET_ALL} {stats['absent']} ({stats['absent']/stats['total']*100:.1f}%% if stats['total'] > 0 else 0%%)")
            print(f"{Fore.BLUE}Currently Working:{Style.RESET_ALL} {stats['working']}")
            print(f"{Fore.YELLOW}On Break:{Style.RESET_ALL} {stats['on_break']}")
            print(f"{Fore.MAGENTA}Checked Out:{Style.RESET_ALL} {stats['checked_out']}")
            
            # Get today's attendance records
            records = get_today_attendance()
            
            # Display attendance records
            print("\n" + "-" * 80)
            print(f" TODAY'S ATTENDANCE RECORDS ({len(records)}) ".center(80, "-"))
            print("-" * 80 + "\n")
            
            if records:
                # Prepare data for tabulate
                table_data = []
                for record in records:
                    # Format the status with color
                    if record['status'] == 'check-in':
                        status = f"{Fore.GREEN}Check In{Style.RESET_ALL}"
                    elif record['status'] == 'check-out':
                        status = f"{Fore.RED}Check Out{Style.RESET_ALL}"
                    elif record['status'] == 'break':
                        status = f"{Fore.YELLOW}Break{Style.RESET_ALL}"
                    else:
                        status = record['status']
                    
                    # Add the record to the table data
                    table_data.append([
                        record['id'],
                        record['name'],
                        record['user_id'],
                        record['punch_time'].strftime('%H:%M:%S'),
                        status,
                        record['device_ip'],
                        record['team'],
                        record['shift_name']
                    ])
                
                # Display the table
                headers = ["ID", "Name", "User ID", "Time", "Status", "Device IP", "Team", "Shift"]
                print(tabulate(table_data, headers=headers, tablefmt="grid"))
            else:
                print("No attendance records found for today.")
            
            # Wait for the specified interval
            time.sleep(refresh_interval)
    
    except KeyboardInterrupt:
        print("\n\nMonitoring stopped. Goodbye!")
    except Exception as e:
        print(f"\n\nError: {e}")

if __name__ == '__main__':
    # Get refresh interval from command line argument if provided
    refresh_interval = int(sys.argv[1]) if len(sys.argv) > 1 else 5
    
    # Display the attendance monitor
    display_attendance_monitor(refresh_interval)