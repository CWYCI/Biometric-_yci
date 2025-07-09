'use client';

import { Employee } from '@/types/employee';
import { Card, CardContent, CardHeader } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import {
  Clock,
  Coffee,
  LogIn,
  LogOut,
  Wifi,
  WifiOff,
  User,
  Building,
  Timer,
  Monitor,
} from 'lucide-react';
import { cn } from '@/lib/utils';

interface EmployeeCardProps {
  employee: Employee;
}

export function EmployeeCard({ employee }: EmployeeCardProps) {
  const getStatusInfo = () => {
    if (!employee.isOnline) {
      return {
        text: 'Offline',
        icon: LogOut,
        className: 'status-offline',
        badgeVariant: 'secondary' as const,
      };
    }

    switch (employee.status) {
      case 'Punched_In':
        return {
          text: 'Working',
          icon: Clock,
          className: 'status-working',
          badgeVariant: 'default' as const,
        };
      case 'Break_In':
        return {
          text: 'On Break',
          icon: Coffee,
          className: 'status-break',
          badgeVariant: 'secondary' as const,
        };
      case 'Break_Out':
        return {
          text: 'Available',
          icon: LogIn,
          className: 'status-available',
          badgeVariant: 'secondary' as const,
        };
      case 'Punched_Out':
        return {
          text: 'Punched Out',
          icon: LogOut,
          className: 'status-punched-out',
          badgeVariant: 'destructive' as const,
        };
      default:
        return {
          text: 'Unknown',
          icon: User,
          className: 'status-offline',
          badgeVariant: 'secondary' as const,
        };
    }
  };

  const statusInfo = getStatusInfo();
  const StatusIcon = statusInfo.icon;

  return (
    <Card
      className={cn(
        'transition-all duration-200 hover:shadow-lg border-l-4',
        statusInfo.className
      )}
    >
      <CardHeader className="pb-3">
        <div className="flex items-start justify-between">
          <div className="space-y-1">
            <h3 className="font-semibold text-lg leading-none">{employee.name}</h3>
            <p className="text-sm text-muted-foreground">ID: {employee.userId}</p>
          </div>
          <div className="flex items-center space-x-2">
            {employee.isOnline ? (
              <Wifi className="h-4 w-4 text-green-600" />
            ) : (
              <WifiOff className="h-4 w-4 text-red-600" />
            )}
            <Badge variant={statusInfo.badgeVariant} className="flex items-center gap-1">
              <StatusIcon className="h-3 w-3" />
              {statusInfo.text}
            </Badge>
          </div>
        </div>
      </CardHeader>

      <CardContent className="space-y-3">
        <div className="grid grid-cols-1 gap-2 text-sm">
          <div className="flex items-center gap-2">
            <Building className="h-4 w-4 text-muted-foreground" />
            <span className="font-medium">{employee.team}</span>
            <span className="text-muted-foreground">({employee.teamId})</span>
          </div>

          <div className="flex items-center gap-2">
            <Timer className="h-4 w-4 text-muted-foreground" />
            <span>
              {employee.shiftName} ({employee.shiftStartTime} - {employee.shiftEndTime})
            </span>
          </div>

          {employee.lateByMinutes && employee.lateByMinutes > 0 && (
            <div className="flex items-center gap-2 text-red-600">
              <Clock className="h-4 w-4" />
              <span className="font-medium">Late by: {employee.lateByMinutes} min</span>
            </div>
          )}

          <div className="flex items-center gap-2 text-xs text-muted-foreground">
            <Clock className="h-3 w-3" />
            <span>Last Punch: {employee.lastPunchDate} {employee.lastPunchTime}</span>
          </div>

          <div className="flex items-center gap-2 text-xs text-muted-foreground">
            <Monitor className="h-3 w-3" />
            <span>Device: {employee.deviceIp}</span>
          </div>
        </div>
      </CardContent>
    </Card>
  );
}