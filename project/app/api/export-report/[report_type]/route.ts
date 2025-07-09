import { NextRequest, NextResponse } from 'next/server';
interface Employee {
  userId: string;
  name: string;
  team: string;
  teamId: string;
  shiftName: string;
  shiftStartTime: string;
  shiftEndTime: string;
  status: string;
  isOnline: boolean;
  lastPunchDate: string;
  lastPunchTime: string;
  lateByMinutes?: number;
  deviceIp: string;
}

async function fetchEmployeeData(): Promise<Employee[]> {
  try {
    const response = await fetch(`${process.env.NEXT_PUBLIC_BACKEND_URL}/api/employees`);
    if (!response.ok) {
      throw new Error('Failed to fetch employee data');
    }
    return await response.json();
  } catch (error) {
    console.error('Error fetching employee data:', error);
    return [];
  }
}

function generateCSV(employees: Employee[], reportType: string): string {
  const headers = [
    'Employee ID',
    'Name',
    'Team',
    'Team ID',
    'Shift',
    'Shift Start',
    'Shift End',
    'Status',
    'Online',
    'Last Punch Date',
    'Last Punch Time',
    'Late By (minutes)',
    'Device IP'
  ];

  const rows = employees.map(emp => [
    emp.userId,
    emp.name,
    emp.team,
    emp.teamId,
    emp.shiftName,
    emp.shiftStartTime,
    emp.shiftEndTime,
    emp.status,
    emp.isOnline ? 'Yes' : 'No',
    emp.lastPunchDate,
    emp.lastPunchTime,
    emp.lateByMinutes || 0,
    emp.deviceIp
  ]);

  const csvContent = [headers, ...rows]
    .map(row => row.map(field => `"${field}"`).join(','))
    .join('\n');

  return csvContent;
}

export async function GET(request: NextRequest) {
  const url = new URL(request.url);
  const pathParts = url.pathname.split('/');
  const reportType = pathParts[pathParts.length - 1];

  if (!['daily', 'weekly', 'monthly'].includes(reportType)) {
    return NextResponse.json(
      { error: 'Invalid report type. Must be daily, weekly, or monthly.' },
      { status: 400 }
    );
  }

  const employees = await fetchEmployeeData();
  
  if (employees.length === 0) {
    return NextResponse.json(
      { error: 'No employee data available' },
      { status: 404 }
    );
  }

  // Filter employees based on report type (simplified for demo)
  let filteredEmployees = employees;
  const currentDate = new Date();
  
  // For this demo, we'll just use all employees
  // In a real implementation, you'd filter by date ranges
  
  const csvContent = generateCSV(filteredEmployees, reportType);
  const filename = `attendance_${reportType}_${currentDate.toISOString().split('T')[0]}.csv`;

  return new NextResponse(csvContent, {
    status: 200,
    headers: {
      'Content-Type': 'text/csv',
      'Content-Disposition': `attachment; filename="${filename}"`,
    },
  });
}