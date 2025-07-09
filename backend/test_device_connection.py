import sys
import time
import logging
from zk import ZK, const
from zk.exception import ZKError, ZKNetworkError, ZKErrorConnection

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

def test_device_connection(ip_address, port=4370, timeout=5):
    """Test the connection to a ZKTeco biometric device."""
    logging.info(f"Testing connection to biometric device at {ip_address}:{port}...")
    
    # Create a ZK instance
    zk = ZK(ip_address, port=port, timeout=timeout)
    
    try:
        # Connect to the device
        conn = zk.connect()
        
        # Get device information
        info = conn.get_device_info()
        
        # Print device information
        logging.info("\nConnection successful!")
        logging.info("Device Information:")
        logging.info(f"  Serial Number: {info.serial_number}")
        logging.info(f"  Device Name: {info.device_name}")
        logging.info(f"  Firmware Version: {info.firmware_version}")
        logging.info(f"  Platform: {info.platform}")
        logging.info(f"  Work Code: {info.work_code}")
        logging.info(f"  User Capacity: {info.user_capacity}")
        logging.info(f"  Fingerprint Capacity: {info.finger_capacity}")
        logging.info(f"  Face Capacity: {info.face_capacity}")
        
        # Get attendance records count
        attendance_count = len(conn.get_attendance())
        logging.info(f"  Attendance Records: {attendance_count}")
        
        # Disconnect from the device
        conn.disconnect()
        
        return True
    
    except ZKNetworkError as e:
        logging.error(f"\nNetwork error: {e}")
        return False
    except ZKErrorConnection as e:
        logging.error(f"\nConnection error: {e}")
        return False
    except ZKError as e:
        logging.error(f"\nDevice error: {e}")
        return False
    except Exception as e:
        logging.error(f"\nUnexpected error: {e}")
        return False

if __name__ == '__main__':
    # Check if IP address is provided as command line argument
    if len(sys.argv) < 2:
        print("Usage: python test_device_connection.py <ip_address> [port]")
        sys.exit(1)
    
    # Get IP address from command line argument
    ip_address = sys.argv[1]
    
    # Get port from command line argument if provided
    port = int(sys.argv[2]) if len(sys.argv) > 2 else 4370
    
    # Test the connection
    success = test_device_connection(ip_address, port)
    
    # Exit with appropriate status code
    sys.exit(0 if success else 1)