'use client';

import { Statistics } from '@/types/employee';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import {
  Users,
  UserCheck,
  Clock,
  Coffee,
  UserX,
  LogIn,
  LogOut,
  ArrowRightLeft,
} from 'lucide-react';

interface StatisticsBarProps {
  statistics: Statistics;
}

export function StatisticsBar({ statistics }: StatisticsBarProps) {
  const formatLastEvent = (event?: { timestamp: string; userId: string; name: string }) => {
    if (!event) return 'N/A';
    const date = new Date(event.timestamp);
    return `${date.toLocaleString()} (${event.userId})`;
  };

  return (
    <div className="space-y-4 mb-6">
      {/* First Row - Main Statistics (5 columns) */}
      <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-5 gap-3">
        <Card className="transition-all hover:shadow-md">
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Total Employees</CardTitle>
            <Users className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{statistics.totalEmployees}</div>
          </CardContent>
        </Card>

        <Card className="transition-all hover:shadow-md">
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Present Today</CardTitle>
            <UserCheck className="h-4 w-4 text-green-600" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold text-green-600">{statistics.presentToday}</div>
          </CardContent>
        </Card>

        <Card className="transition-all hover:shadow-md">
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Absent Today</CardTitle>
            <UserX className="h-4 w-4 text-red-600" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold text-red-600">{statistics.absentToday}</div>
          </CardContent>
        </Card>

        <Card className="transition-all hover:shadow-md">
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Working Employee</CardTitle>
            <Clock className="h-4 w-4 text-blue-600" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold text-blue-600">{statistics.workingNow}</div>
          </CardContent>
        </Card>

        <Card className="transition-all hover:shadow-md">
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Not Punched In</CardTitle>
            <UserX className="h-4 w-4 text-orange-600" />
          </CardHeader>
          <CardContent>
            <div className="text-lg font-bold text-orange-600">{statistics.notPunchedIn} employees</div>
          </CardContent>
        </Card>
      </div>

      {/* Second Row - Last Events (5 columns) */}
      <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-5 gap-3">
        <Card className="transition-all hover:shadow-md">
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-xs font-medium">Last Punch In</CardTitle>
            <LogIn className="h-3 w-3 text-green-600" />
          </CardHeader>
          <CardContent>
            <div className="text-xs text-muted-foreground break-all">
              {formatLastEvent(statistics.lastPunchIn)}
            </div>
          </CardContent>
        </Card>

        <Card className="transition-all hover:shadow-md">
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-xs font-medium">Last Punch Out</CardTitle>
            <LogOut className="h-3 w-3 text-red-600" />
          </CardHeader>
          <CardContent>
            <div className="text-xs text-muted-foreground break-all">
              {formatLastEvent(statistics.lastPunchOut)}
            </div>
          </CardContent>
        </Card>

        <Card className="transition-all hover:shadow-md">
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-xs font-medium">Last Break In</CardTitle>
            <ArrowRightLeft className="h-3 w-3 text-yellow-600" />
          </CardHeader>
          <CardContent>
            <div className="text-xs text-muted-foreground break-all">
              {formatLastEvent(statistics.lastBreakIn)}
            </div>
          </CardContent>
        </Card>

        <Card className="transition-all hover:shadow-md">
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-xs font-medium">Last Break Out</CardTitle>
            <Coffee className="h-3 w-3 text-purple-600" />
          </CardHeader>
          <CardContent>
            <div className="text-xs text-muted-foreground break-all">
              {formatLastEvent(statistics.lastBreakOut)}
            </div>
          </CardContent>
        </Card>

        <Card className="transition-all hover:shadow-md">
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-xs font-medium">Last Early Log Out</CardTitle>
            <LogOut className="h-3 w-3 text-orange-600" />
          </CardHeader>
          <CardContent>
            <div className="text-xs text-muted-foreground break-all">
              {formatLastEvent(statistics.lastEarlyLogOut)}
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}