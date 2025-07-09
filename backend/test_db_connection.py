import os
import sys
from dotenv import load_dotenv
import psycopg2

# Load environment variables
load_dotenv()

def test_connection():
    """
    Test the connection to the PostgreSQL database.
    """
    # Get database connection parameters from environment variables
    db_host = os.getenv('DB_HOST', 'localhost')
    db_port = os.getenv('DB_PORT', '5432')
    db_name = os.getenv('DB_NAME', 'Attendance_YCI')
    db_user = os.getenv('DB_USER', 'postgres')
    db_password = os.getenv('DB_PASSWORD', 'Admin123@')
    
    # Display connection information
    print(f"Testing connection to PostgreSQL database:")
    print(f"  Host: {db_host}")
    print(f"  Port: {db_port}")
    print(f"  Database: {db_name}")
    print(f"  User: {db_user}")
    print()
    
    try:
        # Attempt to connect to the database
        conn = psycopg2.connect(
            host=db_host,
            port=db_port,
            dbname=db_name,
            user=db_user,
            password=db_password
        )
        
        # Create a cursor
        cursor = conn.cursor()
        
        # Execute a simple query
        cursor.execute('SELECT version();')
        
        # Fetch the result
        db_version = cursor.fetchone()
        
        # Close the cursor and connection
        cursor.close()
        conn.close()
        
        # Display success message
        print("Connection successful!")
        print(f"PostgreSQL version: {db_version[0]}")
        return True
    
    except Exception as e:
        # Display error message
        print(f"Connection failed: {e}")
        return False

if __name__ == '__main__':
    # Run the test
    success = test_connection()
    
    # Exit with appropriate status code
    sys.exit(0 if success else 1)