export interface Employee {
  id: string;
  userId: string;
  name: string;
  shiftName: string;
  shiftStartTime: string;
  shiftEndTime: string;
  team: string;
  teamId: string;
  lastPunchDate: string;
  lastPunchTime: string;
  status: 'Punched_In' | 'Punched_Out' | 'Break_In' | 'Break_Out';
  deviceIp: string;
  isOnline: boolean;
  lateByMinutes?: number;
}

export interface Statistics {
  totalEmployees: number;
  presentToday: number;
  workingNow: number;
  onBreak: number;
  notPunchedIn: number;
  absentToday: number;
  lastPunchIn?: LastEvent;
  lastPunchOut?: LastEvent;
  lastBreakIn?: LastEvent;
  lastBreakOut?: LastEvent;
  lastEarlyLogOut?: LastEvent;
}

export interface LastEvent {
  timestamp: string;
  userId: string;
  name: string;
}

export interface PieChartSegment {
  name: string;
  value: number;
  color: string;
}

export interface LateEmployee {
  id: string;
  userId: string;
  name: string;
  team: string;
  shiftName: string;
  shiftStartTime: string;
  lateByMinutes: number;
}