-- Setup script for Biometric Attendance System Database

-- Create the database if it doesn't exist
-- We need to do this outside of a function
DROP DATABASE IF EXISTS "Attendance_YCI";
CREATE DATABASE "Attendance_YCI";


-- Connect to the database
\c Attendance_YCI;

-- Create enum type for attendance status
DO $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'status_enum') THEN
        CREATE TYPE status_enum AS ENUM ('check-in', 'check-out', 'break');
    END IF;
END
$$;

-- Create teams table
CREATE TABLE IF NOT EXISTS team (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create shifts table
CREATE TABLE IF NOT EXISTS shift (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE,
    start_time TIME NOT NULL,
    end_time TIME NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create devices table
CREATE TABLE IF NOT EXISTS device (
    id SERIAL PRIMARY KEY,
    ip_address VARCHAR(15) NOT NULL UNIQUE,
    name VARCHAR(100),
    location VARCHAR(100),
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create employees table
CREATE TABLE IF NOT EXISTS employee (
    id SERIAL PRIMARY KEY,
    user_id VARCHAR(20) NOT NULL UNIQUE,
    name VARCHAR(100) NOT NULL,
    shift_id INTEGER REFERENCES shift(id),
    shift_name VARCHAR(100),
    shift_start_time TIME,
    shift_end_time TIME,
    team_id INTEGER REFERENCES team(id),
    team VARCHAR(100),
    device_ip VARCHAR(15) REFERENCES device(ip_address),
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create attendance table
CREATE TABLE IF NOT EXISTS attendance (
    id SERIAL PRIMARY KEY,
    user_id VARCHAR(20) NOT NULL,
    punch_time TIMESTAMP NOT NULL,
    status status_enum NOT NULL,
    device_ip VARCHAR(15) REFERENCES device(ip_address),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES employee(user_id)
);

-- Create indexes for better performance
CREATE INDEX IF NOT EXISTS idx_attendance_user_id ON attendance(user_id);
CREATE INDEX IF NOT EXISTS idx_attendance_punch_time ON attendance(punch_time);
CREATE INDEX IF NOT EXISTS idx_attendance_status ON attendance(status);
CREATE INDEX IF NOT EXISTS idx_employee_team_id ON employee(team_id);
CREATE INDEX IF NOT EXISTS idx_employee_shift_id ON employee(shift_id);

-- Create view for employee status
CREATE OR REPLACE VIEW employee_status AS
SELECT 
    e.id,
    e.user_id,
    e.name,
    e.shift_name,
    e.shift_start_time,
    e.shift_end_time,
    e.team,
    COALESCE(
        (SELECT a.punch_time 
         FROM attendance a 
         WHERE a.user_id = e.user_id 
         ORDER BY a.punch_time DESC 
         LIMIT 1),
        NULL
    ) AS last_punch_time,
    COALESCE(
        (SELECT a.status 
         FROM attendance a 
         WHERE a.user_id = e.user_id 
         ORDER BY a.punch_time DESC 
         LIMIT 1),
        NULL
    ) AS last_status,
    e.device_ip,
    e.is_active
FROM 
    employee e;

-- Create function to calculate lateness
CREATE OR REPLACE FUNCTION calculate_lateness(shift_start TIME, punch_time TIMESTAMP)
RETURNS INTEGER AS $$
DECLARE
    punch_time_only TIME;
    minutes_late INTEGER;
BEGIN
    -- Extract time from timestamp
    punch_time_only := punch_time::TIME;
    
    -- Calculate minutes late
    IF punch_time_only > shift_start THEN
        minutes_late := EXTRACT(EPOCH FROM (punch_time_only - shift_start))/60;
    ELSE
        minutes_late := 0;
    END IF;
    
    RETURN minutes_late;
END;
$$ LANGUAGE plpgsql;

-- Create view for late employees
CREATE OR REPLACE VIEW late_employees AS
SELECT 
    e.id,
    e.user_id,
    e.name,
    e.shift_name,
    e.shift_start_time,
    e.shift_end_time,
    e.team,
    a.punch_time AS last_punch_time,
    a.status AS last_status,
    e.device_ip,
    e.is_active,
    calculate_lateness(e.shift_start_time, a.punch_time) AS late_by_minutes
FROM 
    employee e
JOIN 
    attendance a ON e.user_id = a.user_id
WHERE 
    DATE(a.punch_time) = CURRENT_DATE
    AND a.status = 'check-in'
    AND calculate_lateness(e.shift_start_time, a.punch_time) > 0
ORDER BY 
    late_by_minutes DESC;

-- Create view for yesterday's late employees
CREATE OR REPLACE VIEW yesterday_late_employees AS
SELECT 
    e.id,
    e.user_id,
    e.name,
    e.shift_name,
    e.shift_start_time,
    e.shift_end_time,
    e.team,
    a.punch_time AS last_punch_time,
    a.status AS last_status,
    e.device_ip,
    e.is_active,
    calculate_lateness(e.shift_start_time, a.punch_time) AS late_by_minutes
FROM 
    employee e
JOIN 
    attendance a ON e.user_id = a.user_id
WHERE 
    DATE(a.punch_time) = CURRENT_DATE - INTERVAL '1 day'
    AND a.status = 'check-in'
    AND calculate_lateness(e.shift_start_time, a.punch_time) > 0
ORDER BY 
    late_by_minutes DESC;

PRINT 'Database setup completed successfully!';