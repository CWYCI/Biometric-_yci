import datetime

def calculate_lateness(punch_time, shift_start_time):
    """
    Calculate lateness in minutes between punch time and shift start time.
    
    Args:
        punch_time (datetime): The time employee punched in
        shift_start_time (time): The scheduled shift start time
    
    Returns:
        int: Number of minutes late (0 if on time or early)
    """
    # Convert shift_start_time to datetime for the same day as punch_time
    shift_start_datetime = datetime.datetime.combine(
        punch_time.date(),
        shift_start_time
    )
    
    # Calculate difference in minutes
    if punch_time <= shift_start_datetime:
        return 0
    
    time_diff = punch_time - shift_start_datetime
    return int(time_diff.total_seconds() / 60)

def format_datetime(dt):
    """
    Format datetime object to string.
    
    Args:
        dt (datetime): Datetime object
    
    Returns:
        tuple: (date_str, time_str)
    """
    if not dt:
        return '', ''
    
    date_str = dt.strftime('%Y-%m-%d')
    time_str = dt.strftime('%H:%M:%S')
    
    return date_str, time_str

def is_weekend(date):
    """
    Check if the given date is a weekend (Saturday or Sunday).
    
    Args:
        date (datetime.date): The date to check
    
    Returns:
        bool: True if weekend, False otherwise
    """
    return date.weekday() >= 5  # 5 = Saturday, 6 = Sunday

def get_date_range(start_date, end_date):
    """
    Generate a list of dates between start_date and end_date (inclusive).
    
    Args:
        start_date (datetime.date): Start date
        end_date (datetime.date): End date
    
    Returns:
        list: List of datetime.date objects
    """
    delta = end_date - start_date
    return [start_date + datetime.timedelta(days=i) for i in range(delta.days + 1)]