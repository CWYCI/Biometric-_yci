from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean, Time, Text, Enum
from sqlalchemy.orm import relationship
import enum
import uuid
from datetime import datetime, time

# Initialize SQLAlchemy
db = SQLAlchemy()

# Define status enum
class StatusEnum(enum.Enum):
    PUNCHED_IN = 'Punched_In'
    PUNCHED_OUT = 'Punched_Out'
    BREAK_IN = 'Break_In'
    BREAK_OUT = 'Break_Out'

# Employee model
class Employee(db.Model):
    __tablename__ = 'employees'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(String(50), unique=True, nullable=False)
    name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=True)
    phone = Column(String(20), nullable=True)
    shift_id = Column(Integer, ForeignKey('shifts.id'), nullable=False)
    team_id = Column(Integer, ForeignKey('teams.id'), nullable=False)
    device_id = Column(Integer, ForeignKey('devices.id'), nullable=False)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    
    # Relationships
    shift = relationship('Shift', back_populates='employees')
    team = relationship('Team', back_populates='employees')
    device = relationship('Device', back_populates='employees')
    attendance_records = relationship('Attendance', back_populates='employee')
    
    def __repr__(self):
        return f'<Employee {self.name}>'

# Attendance model
class Attendance(db.Model):
    __tablename__ = 'attendance'
    
    id = Column(Integer, primary_key=True)
    employee_id = Column(Integer, ForeignKey('employees.id'), nullable=False)
    timestamp = Column(DateTime, default=datetime.now, nullable=False)
    status = Column(String(20), nullable=False)
    device_id = Column(Integer, ForeignKey('devices.id'), nullable=False)
    
    # Relationships
    employee = relationship('Employee', back_populates='attendance_records')
    device = relationship('Device', back_populates='attendance_records')
    
    def __repr__(self):
        return f'<Attendance {self.employee.name} {self.status} at {self.timestamp}>'

# Device model
class Device(db.Model):
    __tablename__ = 'devices'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    ip_address = Column(String(15), unique=True, nullable=False)
    port = Column(Integer, default=4370, nullable=False)
    is_active = Column(Boolean, default=True)
    last_connected = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    
    # Relationships
    employees = relationship('Employee', back_populates='device')
    attendance_records = relationship('Attendance', back_populates='device')
    
    def __repr__(self):
        return f'<Device {self.name} ({self.ip_address})>'

# Team model
class Team(db.Model):
    __tablename__ = 'teams'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100), unique=True, nullable=False)
    description = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    
    # Relationships
    employees = relationship('Employee', back_populates='team')
    
    def __repr__(self):
        return f'<Team {self.name}>'

# Shift model
class Shift(db.Model):
    __tablename__ = 'shifts'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100), unique=True, nullable=False)
    start_time = Column(Time, nullable=False)
    end_time = Column(Time, nullable=False)
    break_start = Column(Time, nullable=True)
    break_end = Column(Time, nullable=True)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    
    # Relationships
    employees = relationship('Employee', back_populates='shift')
    
    def __repr__(self):
        return f'<Shift {self.name} ({self.start_time}-{self.end_time})>'