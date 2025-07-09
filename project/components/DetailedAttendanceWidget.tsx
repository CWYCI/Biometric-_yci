'use client';

import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from '@/components/ui/table';
import { Employee } from '@/types/employee';
import { FileText, User, Clock, Calendar } from 'lucide-react';

interface DetailedAttendanceWidgetProps {
  employees?: Employee[];
  title?: string;
}

export function DetailedAttendanceWidget({ 
  employees = [], 
  title = 'Detailed Attendance' 
}: DetailedAttendanceWidgetProps) {
  // For demo purposes, we'll show a static table if no employees are provided
  const hasEmployees = employees.length > 0;

  return (
    <Card className="col-span-1 lg:col-span-2">
      <CardHeader>
        <CardTitle className="flex items-center gap-2">
          <FileText className="h-5 w-5 text-blue-600" />
          {title}
        </CardTitle>
      </CardHeader>
      <CardContent>
        <div className="max-h-64 overflow-y-auto">
          <Table>
            <TableHeader>
              <TableRow>
                <TableHead>Employee</TableHead>
                <TableHead>Status</TableHead>
                <TableHead>Punch Time</TableHead>
                <TableHead>Shift</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {hasEmployees ? (
                employees.map((employee) => (
                  <TableRow key={employee.id}>
                    <TableCell>
                      <div className="flex items-center gap-2">
                        <User className="h-4 w-4 text-muted-foreground" />
                        <span>{employee.name}</span>
                      </div>
                    </TableCell>
                    <TableCell>
                      <Badge 
                        variant={employee.status === 'Punched_In' ? 'default' : 
                                employee.status === 'Punched_Out' ? 'destructive' : 
                                'outline'}
                        className={employee.status === 'Punched_In' ? 'bg-green-500 hover:bg-green-600' : ''}
                      >
                        {employee.status.replace('_', ' ')}
                      </Badge>
                    </TableCell>
                    <TableCell>
                      <div className="flex items-center gap-2">
                        <Clock className="h-4 w-4 text-muted-foreground" />
                        <span>{employee.lastPunchTime}</span>
                      </div>
                    </TableCell>
                    <TableCell>
                      <div className="flex items-center gap-2">
                        <Calendar className="h-4 w-4 text-muted-foreground" />
                        <span>{employee.shiftName} ({employee.shiftStartTime}-{employee.shiftEndTime})</span>
                      </div>
                    </TableCell>
                  </TableRow>
                ))
              ) : (
                // Demo data when no employees are provided
                <>
                  <TableRow>
                    <TableCell>John Smith</TableCell>
                    <TableCell><Badge variant="default" className="bg-green-500 hover:bg-green-600">Punched In</Badge></TableCell>
                    <TableCell>09:05 AM</TableCell>
                    <TableCell>Morning (09:00-17:00)</TableCell>
                  </TableRow>
                  <TableRow>
                    <TableCell>Jane Doe</TableCell>
                    <TableCell><Badge variant="outline">Break In</Badge></TableCell>
                    <TableCell>12:30 PM</TableCell>
                    <TableCell>Morning (09:00-17:00)</TableCell>
                  </TableRow>
                  <TableRow>
                    <TableCell>Mike Johnson</TableCell>
                    <TableCell><Badge variant="destructive">Punched Out</Badge></TableCell>
                    <TableCell>17:15 PM</TableCell>
                    <TableCell>Morning (09:00-17:00)</TableCell>
                  </TableRow>
                </>
              )}
            </TableBody>
          </Table>
        </div>
      </CardContent>
    </Card>
  );
}