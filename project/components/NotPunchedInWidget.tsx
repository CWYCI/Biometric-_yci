'use client';

import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Employee } from '@/types/employee';
import { UserX, User, Building, Timer, Clock } from 'lucide-react';

interface NotPunchedInWidgetProps {
  employees: Employee[];
  title?: string;
}

export function NotPunchedInWidget({ employees = [], title = 'Not Punched In Yet' }: NotPunchedInWidgetProps) {
  return (
    <Card className="col-span-1 lg:col-span-2">
      <CardHeader>
        <CardTitle className="flex items-center gap-2">
          <UserX className="h-5 w-5 text-orange-600" />
          {title} ({employees.length})
        </CardTitle>
      </CardHeader>
      <CardContent>
        <div className="space-y-3 max-h-64 overflow-y-auto">
          {employees.length === 0 ? (
            <div className="text-center text-muted-foreground py-4">
              All employees have punched in!
            </div>
          ) : (
            employees.map((employee) => (
              <div
                key={employee.id}
                className="flex items-center justify-between p-3 bg-orange-50 border border-orange-200 rounded-lg"
              >
                <div className="space-y-1">
                  <div className="flex items-center gap-2">
                    <User className="h-3 w-3 text-muted-foreground" />
                    <span className="font-medium">{employee.name}</span>
                    <span className="text-sm text-muted-foreground">({employee.userId})</span>
                  </div>
                  <div className="flex items-center gap-2 text-xs text-muted-foreground">
                    <Building className="h-3 w-3" />
                    <span>{employee.team}</span>
                    <Timer className="h-3 w-3" />
                    <span>{employee.shiftName}</span>
                  </div>
                </div>
                <Badge variant="outline" className="flex items-center gap-1 text-orange-700 border-orange-300">
                  <Clock className="h-3 w-3" />
                  Shift starts: {employee.shiftStartTime}
                </Badge>
              </div>
            ))
          )}
        </div>
      </CardContent>
    </Card>
  );
}