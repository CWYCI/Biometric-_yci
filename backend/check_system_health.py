import os
import sys
import time
import subprocess
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def print_header(title):
    """
    Print a formatted header for a section.
    """
    print("\n" + "=" * 60)
    print(f" {title} ".center(60, "="))
    print("=" * 60)

def print_result(component, status, message=None):
    """
    Print a formatted result for a component check.
    """
    status_str = "✅ PASS" if status else "❌ FAIL"
    print(f"{component.ljust(25)} {status_str.ljust(10)} {message if message else ''}")

def run_python_script(script_name, *args):
    """
    Run a Python script and return its exit code.
    """
    cmd = [sys.executable, script_name] + list(args)
    result = subprocess.run(cmd, capture_output=True, text=True)
    return result.returncode == 0, result.stdout, result.stderr

def check_database():
    """
    Check the database connection.
    """
    print_header("DATABASE CONNECTION CHECK")
    success, stdout, stderr = run_python_script("test_db_connection.py")
    print(stdout)
    if not success:
        print(stderr)
    return success

def check_devices():
    """
    Check the biometric device connections.
    """
    print_header("BIOMETRIC DEVICE CONNECTION CHECK")
    
    # Get device IPs from environment variables or use defaults
    device_ips = [
        "192.168.1.201",
        "192.168.1.202"
    ]
    
    all_success = True
    
    for ip in device_ips:
        print(f"\nChecking device at {ip}:")
        success, stdout, stderr = run_python_script("test_device_connection.py", ip)
        print(stdout)
        if not success:
            print(stderr)
            all_success = False
    
    return all_success

def check_backend():
    """
    Check the backend server health.
    """
    print_header("BACKEND SERVER HEALTH CHECK")
    success, stdout, stderr = run_python_script("test_backend_health.py")
    print(stdout)
    if not success:
        print(stderr)
    return success

def check_frontend():
    """
    Check if the frontend server is running.
    """
    print_header("FRONTEND SERVER CHECK")
    
    # Get frontend URL from environment variables or use default
    frontend_url = "http://localhost:3000"
    
    try:
        import requests
        print(f"Checking frontend at {frontend_url}...")
        response = requests.get(frontend_url, timeout=5)
        
        if response.status_code == 200:
            print("\nFrontend server is running!")
            return True
        else:
            print(f"\nFrontend server returned status code: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("\nConnection error: Frontend server is not running or not accessible.")
        return False
    except requests.exceptions.Timeout:
        print("\nTimeout error: Frontend server did not respond within 5 seconds.")
        return False
    except Exception as e:
        print(f"\nError checking frontend: {e}")
        return False

def main():
    """
    Run all health checks and display a summary.
    """
    print("\n" + "*" * 80)
    print(" BIOMETRIC ATTENDANCE SYSTEM - HEALTH CHECK ".center(80, "*"))
    print("*" * 80 + "\n")
    
    # Run all checks
    db_status = check_database()
    device_status = check_devices()
    backend_status = check_backend()
    frontend_status = check_frontend()
    
    # Print summary
    print_header("SYSTEM HEALTH SUMMARY")
    print_result("Database", db_status)
    print_result("Biometric Devices", device_status)
    print_result("Backend Server", backend_status)
    print_result("Frontend Server", frontend_status)
    
    # Overall status
    overall_status = all([db_status, device_status, backend_status, frontend_status])
    print("\n" + "-" * 60)
    if overall_status:
        print("✅ OVERALL SYSTEM STATUS: HEALTHY")
    else:
        print("❌ OVERALL SYSTEM STATUS: ISSUES DETECTED")
    print("-" * 60 + "\n")
    
    return overall_status

if __name__ == '__main__':
    # Run the health check
    success = main()
    
    # Exit with appropriate status code
    sys.exit(0 if success else 1)