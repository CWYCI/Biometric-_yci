import { Employee, Statistics, PieChartSegment, LateEmployee, LastEvent } from '@/types/employee';

export function calculateLateness(employee: Employee): number {
  if (employee.status !== 'Punched_In' || !employee.lastPunchTime || !employee.shiftStartTime) {
    return 0;
  }

  const [shiftHour, shiftMinute] = employee.shiftStartTime.split(':').map(Number);
  const shiftStart = new Date();
  shiftStart.setHours(shiftHour, shiftMinute, 0, 0);

  const lastPunch = new Date(`${employee.lastPunchDate} ${employee.lastPunchTime}`);
  
  if (lastPunch <= shiftStart) {
    return 0;
  }

  return Math.floor((lastPunch.getTime() - shiftStart.getTime()) / (1000 * 60));
}

export function calculateStatistics(employees: Employee[]): Statistics {
  const today = new Date().toDateString();
  
  const presentToday = employees.filter(emp => 
    emp.isOnline && emp.lastPunchDate === today
  ).length;
  
  const workingNow = employees.filter(emp => 
    emp.isOnline && emp.status === 'Punched_In'
  ).length;
  
  const onBreak = employees.filter(emp => 
    emp.isOnline && emp.status === 'Break_In'
  ).length;

  // Calculate employees who should be working but haven't punched in
  const currentTime = new Date();
  const currentHour = currentTime.getHours();
  const currentMinute = currentTime.getMinutes();
  const currentTimeInMinutes = currentHour * 60 + currentMinute;

  const notPunchedIn = employees.filter(emp => {
    if (emp.status === 'Punched_In') return false;
    
    const [shiftHour, shiftMinute] = emp.shiftStartTime.split(':').map(Number);
    const shiftStartInMinutes = shiftHour * 60 + shiftMinute;
    
    return currentTimeInMinutes >= shiftStartInMinutes;
  }).length;

  // Calculate absent today (employees who are offline or punched out)
  const absentToday = employees.filter(emp => 
    !emp.isOnline || emp.status === 'Punched_Out'
  ).length;

  // Find last events
  const todaysEvents = employees.filter(emp => emp.lastPunchDate === today);
  
  const findLastEvent = (status: string): LastEvent | undefined => {
    const matchingEmployees = todaysEvents.filter(emp => emp.status === status);
    if (matchingEmployees.length === 0) return undefined;
    
    const latest = matchingEmployees.reduce((latest, current) => {
      const latestTime = new Date(`${latest.lastPunchDate} ${latest.lastPunchTime}`);
      const currentTime = new Date(`${current.lastPunchDate} ${current.lastPunchTime}`);
      return currentTime > latestTime ? current : latest;
    });
    
    return {
      timestamp: `${latest.lastPunchDate} ${latest.lastPunchTime}`,
      userId: latest.userId,
      name: latest.name,
    };
  };

  return {
    totalEmployees: employees.length,
    presentToday,
    workingNow,
    onBreak,
    notPunchedIn,
    absentToday,
    lastPunchIn: findLastEvent('Punched_In'),
    lastPunchOut: findLastEvent('Punched_Out'),
    lastBreakIn: findLastEvent('Break_In'),
    lastBreakOut: findLastEvent('Break_Out'),
    lastEarlyLogOut: findLastEvent('Punched_Out'), // Assuming early logout is just punch out
  };
}

export function generatePieChartData(employees: Employee[]): PieChartSegment[] {
  const statusCounts = employees.reduce((acc, emp) => {
    let status: string;
    
    if (!emp.isOnline) {
      status = 'Offline';
    } else if (emp.status === 'Punched_In') {
      status = 'Working';
    } else if (emp.status === 'Break_In') {
      status = 'On Break';
    } else if (emp.status === 'Break_Out') {
      status = 'Available';
    } else {
      status = 'Punched Out';
    }
    
    acc[status] = (acc[status] || 0) + 1;
    return acc;
  }, {} as Record<string, number>);

  // Vibrant RGB color mix for better visual appeal
  const colorMap: Record<string, string> = {
    'Working': 'rgb(34, 197, 94)',      // Vibrant Green
    'On Break': 'rgb(251, 146, 60)',    // Vibrant Orange
    'Available': 'rgb(59, 130, 246)',   // Vibrant Blue
    'Punched Out': 'rgb(239, 68, 68)',  // Vibrant Red
    'Offline': 'rgb(156, 163, 175)',    // Cool Gray
  };

  return Object.entries(statusCounts).map(([status, count]) => ({
    name: status,
    value: count,
    color: colorMap[status] || 'rgb(107, 114, 128)',
  }));
}

export function getTopLateComers(employees: Employee[], count: number = 10): LateEmployee[] {
  return employees
    .filter(emp => emp.lateByMinutes && emp.lateByMinutes > 0)
    .sort((a, b) => (b.lateByMinutes || 0) - (a.lateByMinutes || 0))
    .slice(0, count)
    .map(emp => ({
      id: emp.id,
      userId: emp.userId,
      name: emp.name,
      team: emp.team,
      shiftName: emp.shiftName,
      shiftStartTime: emp.shiftStartTime,
      lateByMinutes: emp.lateByMinutes || 0,
    }));
}

export function getNotPunchedInEmployees(employees: Employee[]): Employee[] {
  const currentTime = new Date();
  const currentHour = currentTime.getHours();
  const currentMinute = currentTime.getMinutes();
  const currentTimeInMinutes = currentHour * 60 + currentMinute;

  return employees.filter(emp => {
    if (emp.status === 'Punched_In') return false;
    
    const [shiftHour, shiftMinute] = emp.shiftStartTime.split(':').map(Number);
    const shiftStartInMinutes = shiftHour * 60 + shiftMinute;
    
    return currentTimeInMinutes >= shiftStartInMinutes;
  });
}