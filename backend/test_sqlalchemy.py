import os
import psycopg2
from sqlalchemy import create_engine
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Try direct psycopg2 connection
print("Testing direct psycopg2 connection...")
try:
    conn = psycopg2.connect(
        dbname='Attendance_YCI',
        user='postgres',
        password='Admin123@',
        host='localhost',
        port='5432'
    )
    print("Direct psycopg2 connection successful!")
    conn.close()
except Exception as e:
    print(f"Direct psycopg2 connection failed: {e}")

# Try SQLAlchemy connection with direct psycopg2 parameters
print("\nTesting SQLAlchemy connection with direct parameters...")
try:
    # Create connection parameters
    conn_params = {
        'dbname': 'Attendance_YCI',
        'user': 'postgres',
        'password': 'Admin123@',
        'host': 'localhost',
        'port': '5432'
    }
    
    # Create SQLAlchemy engine with direct psycopg2 connection
    from sqlalchemy.engine.url import URL
    url = URL.create(
        drivername="postgresql+psycopg2",
        username=conn_params['user'],
        password=conn_params['password'],
        host=conn_params['host'],
        port=conn_params['port'],
        database=conn_params['dbname']
    )
    
    engine = create_engine(url)
    
    # Test connection
    connection = engine.connect()
    print("SQLAlchemy connection successful!")
    connection.close()
except Exception as e:
    print(f"SQLAlchemy connection failed: {e}")