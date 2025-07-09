'use client';

import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { LateEmployee } from '@/types/employee';
import { Clock, User, Building, Timer } from 'lucide-react';

interface TopLateComersCardProps {
  title: string;
  employees: LateEmployee[];
}

export function TopLateComersCard({ title, employees }: TopLateComersCardProps) {
  return (
    <Card className="col-span-1 lg:col-span-2">
      <CardHeader>
        <CardTitle className="flex items-center gap-2">
          <Clock className="h-5 w-5 text-red-600" />
          {title}
        </CardTitle>
      </CardHeader>
      <CardContent>
        <div className="space-y-3 max-h-64 overflow-y-auto">
          {employees.length === 0 ? (
            <div className="text-center text-muted-foreground py-4">
              No late employees found
            </div>
          ) : (
            employees.map((employee, index) => (
              <div
                key={employee.id}
                className="flex items-center justify-between p-3 bg-muted/50 rounded-lg"
              >
                <div className="flex items-center gap-3">
                  <Badge variant="outline" className="w-8 h-8 rounded-full p-0 flex items-center justify-center">
                    {index + 1}
                  </Badge>
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
                      <span>{employee.shiftName} (Start: {employee.shiftStartTime})</span>
                    </div>
                  </div>
                </div>
                <Badge variant="destructive" className="flex items-center gap-1">
                  <Clock className="h-3 w-3" />
                  {employee.lateByMinutes} min late
                </Badge>
              </div>
            ))
          )}
        </div>
      </CardContent>
    </Card>
  );
}