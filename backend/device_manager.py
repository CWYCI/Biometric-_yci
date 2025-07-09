import time
import threading
import logging
from datetime import datetime

class DeviceManager:
    """
    Manages connections to ZKTeco biometric devices.
    
    This class handles device registration, connection status monitoring,
    and data retrieval from ZKTeco devices.
    """
    
    def __init__(self):
        self.devices = {}
        self.lock = threading.Lock()
        self.logger = logging.getLogger('device_manager')
        self.monitoring_thread = None
        self.should_stop = False
    
    def register_device(self, ip, port=4370, password=0):
        """
        Register a new ZKTeco device.
        
        Args:
            ip (str): IP address of the device
            port (int): Port number (default: 4370)
            password (int): Device password (default: 0)
            
        Returns:
            bool: True if registration successful, False otherwise
        """
        try:
            with self.lock:
                # In a real implementation, we would use the pyzk library to connect
                # For now, we'll simulate the connection
                self.logger.info(f"Registering device at {ip}:{port}")
                
                # Check if device already registered
                if ip in self.devices:
                    self.logger.info(f"Device at {ip} already registered")
                    return True
                
                # Add device to registry
                self.devices[ip] = {
                    'ip': ip,
                    'port': port,
                    'password': password,
                    'connected': True,
                    'last_connected': datetime.now(),
                    'attendance_data': []
                }
                
                # Start monitoring thread if not already running
                if self.monitoring_thread is None or not self.monitoring_thread.is_alive():
                    self.start_monitoring()
                
                return True
        except Exception as e:
            self.logger.error(f"Error registering device at {ip}: {e}")
            return False
    
    def is_device_online(self, ip):
        """
        Check if a device is online.
        
        Args:
            ip (str): IP address of the device
            
        Returns:
            bool: True if device is online, False otherwise
        """
        with self.lock:
            if ip not in self.devices:
                return False
            return self.devices[ip]['connected']
    
    def get_device_info(self, ip):
        """
        Get information about a device.
        
        Args:
            ip (str): IP address of the device
            
        Returns:
            dict: Device information or None if device not found
        """
        with self.lock:
            if ip not in self.devices:
                return None
            return self.devices[ip]
    
    def get_attendance_data(self, ip):
        """
        Get attendance data from a device.
        
        Args:
            ip (str): IP address of the device
            
        Returns:
            list: Attendance records or empty list if device not found
        """
        with self.lock:
            if ip not in self.devices or not self.devices[ip]['connected']:
                return []
            
            # In a real implementation, we would use the pyzk library to get attendance data
            # For now, we'll return an empty list
            return self.devices[ip]['attendance_data']
    
    def start_monitoring(self):
        """
        Start a background thread to monitor device connections.
        """
        self.should_stop = False
        self.monitoring_thread = threading.Thread(target=self._monitor_devices)
        self.monitoring_thread.daemon = True
        self.monitoring_thread.start()
    
    def stop_monitoring(self):
        """
        Stop the device monitoring thread.
        """
        self.should_stop = True
        if self.monitoring_thread and self.monitoring_thread.is_alive():
            self.monitoring_thread.join(timeout=5)
    
    def _monitor_devices(self):
        """
        Background thread function to monitor device connections.
        """
        while not self.should_stop:
            try:
                with self.lock:
                    for ip, device in self.devices.items():
                        # In a real implementation, we would ping the device
                        # For now, we'll simulate the connection status
                        device['connected'] = True
                        device['last_connected'] = datetime.now()
            except Exception as e:
                self.logger.error(f"Error monitoring devices: {e}")
            
            # Sleep for 30 seconds before checking again
            time.sleep(30)