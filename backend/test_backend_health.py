import os
import sys
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_backend_health(host=None, port=None, timeout=5):
    """
    Test the health of the backend server by making a request to the health endpoint.
    
    Args:
        host (str): The host address (default: from .env or 0.0.0.0)
        port (int): The port number (default: from .env or 5000)
        timeout (int): Request timeout in seconds (default: 5)
        
    Returns:
        bool: True if health check successful, False otherwise
    """
    # Get host and port from arguments, environment variables, or defaults
    if host is None:
        host = os.getenv('HOST', '0.0.0.0')
    if port is None:
        port = os.getenv('PORT', '5000')
    
    # Construct the health check URL
    url = f"http://{host}:{port}/health"
    
    print(f"Testing backend health at {url}...")
    
    try:
        # Make a GET request to the health endpoint
        response = requests.get(url, timeout=timeout)
        
        # Check if the response status code is 200 (OK)
        if response.status_code == 200:
            # Parse the response JSON
            data = response.json()
            
            # Print the response data
            print("\nHealth check successful!")
            print("Response:")
            print(f"  Status: {data.get('status', 'Unknown')}")
            print(f"  Database: {data.get('database', 'Unknown')}")
            print(f"  Devices: {data.get('devices', 'Unknown')}")
            print(f"  Message: {data.get('message', 'No message')}")
            
            return True
        else:
            # Print error message
            print(f"\nHealth check failed with status code: {response.status_code}")
            print(f"Response: {response.text}")
            return False
    
    except requests.exceptions.ConnectionError:
        print("\nConnection error: Backend server is not running or not accessible.")
        return False
    except requests.exceptions.Timeout:
        print(f"\nTimeout error: Backend server did not respond within {timeout} seconds.")
        return False
    except Exception as e:
        print(f"\nError: {e}")
        return False

if __name__ == '__main__':
    # Get host and port from command line arguments if provided
    host = sys.argv[1] if len(sys.argv) > 1 else None
    port = sys.argv[2] if len(sys.argv) > 2 else None
    
    # Test the backend health
    success = test_backend_health(host, port)
    
    # Exit with appropriate status code
    sys.exit(0 if success else 1)