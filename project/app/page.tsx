'use client';

import { useState, useEffect } from 'react';
import { io, Socket } from 'socket.io-client';
import { Employee, Statistics, PieChartSegment, LateEmployee } from '@/types/employee';
import { EmployeeCard } from '@/components/EmployeeCard';
import { StatisticsBar } from '@/components/StatisticsBar';
import { AttendancePieChart } from '@/components/AttendancePieChart';
import { LateComersWidget } from '@/components/LateComersWidget';
import { NotPunchedInWidget } from '@/components/NotPunchedInWidget';
import { DetailedAttendanceWidget } from '@/components/DetailedAttendanceWidget';
import { Button } from '@/components/ui/button';
import { Toaster } from '@/components/ui/sonner';
import {
  Download,
  FileText,
  Calendar,
  CalendarDays,
  Printer,
  Wifi,
  WifiOff,
  RefreshCw,
  AlertTriangle,
} from 'lucide-react';
import {
  calculateStatistics,
  generatePieChartData,
  getTopLateComers,
  getNotPunchedInEmployees,
  calculateLateness,
} from '@/lib/business-logic';
import { fetchWithPortFallback } from '@/lib/utils';
import { toast } from 'sonner';

export default function StatusBoard() {
  const [employees, setEmployees] = useState<Employee[]>([]);
  const [yesterdayLateComers, setYesterdayLateComers] = useState<LateEmployee[]>([]);
  const [socket, setSocket] = useState<Socket | null>(null);
  const [isConnected, setIsConnected] = useState(false);
  const [isLoading, setIsLoading] = useState(true);
  const [lastUpdate, setLastUpdate] = useState<Date>(new Date());
  const [isRefreshing, setIsRefreshing] = useState(false);

  // Calculate derived data
  const statistics = calculateStatistics(employees);
  const pieChartData = generatePieChartData(employees);
  const todayLateComers = getTopLateComers(employees, 10);
  const notPunchedInEmployees = getNotPunchedInEmployees(employees);
  
  // Periodically check backend health when disconnected
  useEffect(() => {
    let healthCheckInterval: NodeJS.Timeout;
    
    // Only start health check if not connected and not already refreshing
    if (!isConnected && !isRefreshing && !isLoading) {
      healthCheckInterval = setInterval(async () => {
        try {
          // Check if API base URL is defined
      // The backend might be running on port 5000 or 5001 (fallback)
      const apiBaseUrl = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:5000';
      
      // Use the fetchWithPortFallback helper to try both ports
      const response = await fetchWithPortFallback(`${apiBaseUrl}/health`, {
            method: 'GET',
            headers: { 'Cache-Control': 'no-cache' },
            signal: AbortSignal.timeout(2000) // 2 second timeout
          });
          
          if (response.ok) {
            // Backend is back online, refresh the page
            toast.success('Backend connection restored! Refreshing data...');
            clearInterval(healthCheckInterval);
            setTimeout(() => window.location.reload(), 1500);
          }
        } catch (error) {
          // Silent fail - we don't want to spam the console
        }
      }, 30000); // Check every 30 seconds
    }
    
    return () => {
      if (healthCheckInterval) clearInterval(healthCheckInterval);
    };
  }, [isConnected, isRefreshing, isLoading]);

  // Fetch initial data
  useEffect(() => {
    const fetchInitialData = async () => {
      try {
        setIsLoading(true);
        


        try {
          // Fetch real employee data from backend with timeout
          const controller = new AbortController();
          const timeoutId = setTimeout(() => controller.abort(), 5000); // 5 second timeout
          
          // Check if API base URL is defined
          // The backend might be running on port 5000 or 5001 (fallback)
          const apiBaseUrl = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:5000';
          
          // Use the fetchWithPortFallback helper to try both ports
          const employeesResponse = await fetchWithPortFallback(
            `${apiBaseUrl}/api/employees`,
            { signal: controller.signal }
          );
          
          clearTimeout(timeoutId);
          
          if (employeesResponse.ok) {
            const employeesData: Employee[] = await employeesResponse.json();
            const processedEmployees = employeesData.map(emp => ({
              ...emp,
              lateByMinutes: calculateLateness(emp),
            }));
            setEmployees(processedEmployees);
          } else {
            throw new Error(`Backend error: ${employeesResponse.status} ${employeesResponse.statusText}`);
          }
        } catch (error) {
          console.error('Backend connection error:', error);
          
          if (error instanceof DOMException && error.name === 'AbortError') {
            toast.error('Connection timed out. Please check if the backend server is running.');
          } else {
            toast.error('Failed to connect to backend. Please ensure the server is running.');
          }
          
          setEmployees([]);
        }

        // Try to fetch yesterday's late comers with timeout
        try {
          const controller = new AbortController();
          const timeoutId = setTimeout(() => controller.abort(), 5000); // 5 second timeout
          
          // Check if API base URL is defined
          // The backend might be running on port 5000 or 5001 (fallback)
          const apiBaseUrl = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:5000';
          
          // Use the fetchWithPortFallback helper to try both ports
          const lateComersResponse = await fetchWithPortFallback(
            `${apiBaseUrl}/api/yesterdays-late-comers`,
            { signal: controller.signal }
          );
          
          clearTimeout(timeoutId);
          
          if (lateComersResponse.ok) {
            const lateComersData = await lateComersResponse.json();
            setYesterdayLateComers(lateComersData);
          } else {
            console.error(`Backend error when fetching late comers: ${lateComersResponse.status} ${lateComersResponse.statusText}`);
            // Instead of throwing, we'll handle the error gracefully
            setYesterdayLateComers([]);
            // Only show a toast if it's not a 404 (which could be normal if there are no late comers)
            if (lateComersResponse.status !== 404) {
              toast.warning(`Could not load yesterday's late comers data. (Status: ${lateComersResponse.status})`);
            }
          }
        } catch (error) {
          console.error('Could not fetch yesterday\'s late comers:', error);
          
          if (error instanceof DOMException && error.name === 'AbortError') {
            toast.error('Connection timed out while fetching late comers data.');
          } else {
            // Don't show another toast if we already showed one for the employees fetch
            // or if we're already handling the error in the else block above
            if (employees.length > 0 && !(error instanceof TypeError && error.message.includes('lateComersResponse'))) {
              toast.warning('Could not load yesterday\'s late comers data.');
            }
          }
          
          setYesterdayLateComers([]);
        }

        toast.success('Dashboard data loaded successfully');
      } catch (error) {
        console.error('Error fetching initial data:', error);
        toast.error('Failed to load dashboard data. Please refresh the page.');
      } finally {
        setIsLoading(false);
      }
    };

    fetchInitialData();
  }, [employees.length]);

  // // Setup Socket.IO connection with retry mechanism
  // useEffect(() => {
  //   let retryCount = 0;
  //   const maxRetries = 3;
  //   const retryDelay = 3000; // 3 seconds
  //   let retryTimeout: NodeJS.Timeout;

  //   const connectSocket = () => {
  //     try {
  //       // Ensure we have a fallback for the socket URL
  //       // Try port 5000 first, then fall back to 5001 if connection fails
  //       const socketUrl = process.env.NEXT_PUBLIC_SOCKET_URL || 'http://localhost:5000';
  //       console.log('Connecting to socket at:', socketUrl);
        
  //       const socketInstance = io(socketUrl, {
  //         timeout: 5000,
  //         forceNew: true,
  //         reconnection: true,
  //         reconnectionAttempts: 5,
  //         reconnectionDelay: 1000,
  //       });
  //       setSocket(socketInstance);

  //       socketInstance.on('connect', () => {
  //         setIsConnected(true);
  //         retryCount = 0; // Reset retry count on successful connection
  //         toast.success('Real-time connection established');
  //       });

  //       socketInstance.on('disconnect', () => {
  //         setIsConnected(false);
  //         toast.warning('Real-time connection lost. Attempting to reconnect...');
  //       });

  //       socketInstance.on('connect_error', (error) => {
  //         setIsConnected(false);
  //         console.warn('Socket connection error:', error);
          
  //         // Try port 5001 if we're currently using 5000 and this is the first retry
  //         const currentUrl = socketInstance.io.uri;
  //         if (retryCount === 0 && currentUrl.includes('5000')) {
  //           retryCount++;
  //           console.log('Trying alternate port 5001...');
            
  //           // Clear any existing timeout
  //           if (retryTimeout) clearTimeout(retryTimeout);
            
  //           // Try connecting to port 5001
  //           retryTimeout = setTimeout(() => {
  //             console.log('Attempting to connect to port 5001...');
  //             socketInstance.disconnect();
  //             const alternateUrl = currentUrl.replace('5000', '5001');
  //             console.log('Connecting to socket at:', alternateUrl);
  //             const alternateInstance = io(alternateUrl, {
  //               timeout: 5000,
  //               forceNew: true,
  //               reconnection: true,
  //               reconnectionAttempts: 5,
  //               reconnectionDelay: 1000,
  //             });
  //             setSocket(alternateInstance);
              
  //             // Set up event handlers for the new socket
  //             alternateInstance.on('connect', () => {
  //               setIsConnected(true);
  //               retryCount = 0;
  //               toast.success('Real-time connection established on alternate port');
  //             });
              
  //             alternateInstance.on('disconnect', () => {
  //               setIsConnected(false);
  //               toast.warning('Real-time connection lost. Attempting to reconnect...');
  //             });
              
  //             alternateInstance.on('connect_error', (error) => {
  //               setIsConnected(false);
  //               console.warn('Socket connection error on alternate port:', error);
                
  //               // Continue with normal retry logic
  //               if (retryCount < maxRetries) {
  //                 retryCount++;
  //                 console.log(`Retrying connection (${retryCount}/${maxRetries}) in ${retryDelay/1000}s...`);
                  
  //                 if (retryTimeout) clearTimeout(retryTimeout);
                  
  //                 retryTimeout = setTimeout(() => {
  //                   console.log('Attempting to reconnect...');
  //                   alternateInstance.disconnect();
  //                   connectSocket();
  //                 }, retryDelay);
  //               } else {
  //                 toast.error('Failed to establish real-time connection after multiple attempts');
  //               }
  //             });
              
  //             alternateInstance.on('employee_update', (updatedEmployee: Employee) => {
  //               setEmployees(prev => {
  //                 const updated = prev.map(emp => 
  //                   emp.id === updatedEmployee.id 
  //                     ? { ...updatedEmployee, lateByMinutes: calculateLateness(updatedEmployee) }
  //                     : emp
  //                 );
  //                 setLastUpdate(new Date());
  //                 return updated;
  //               });
  //               toast.info(`Employee ${updatedEmployee.name} status updated`);
  //             });
  //           }, 1000);
            
  //           return;
  //         }
          
  //         // Implement manual retry if socket.io reconnection fails
  //         if (retryCount < maxRetries) {
  //           retryCount++;
  //           console.log(`Retrying connection (${retryCount}/${maxRetries}) in ${retryDelay/1000}s...`);
            
  //           // Clear any existing timeout
  //           if (retryTimeout) clearTimeout(retryTimeout);
            
  //           // Set new retry timeout
  //           retryTimeout = setTimeout(() => {
  //             console.log('Attempting to reconnect...');
  //             socketInstance.disconnect();
  //             connectSocket();
  //           }, retryDelay);
  //         } else {
  //           toast.error('Failed to establish real-time connection after multiple attempts');
          
  //       });

  //       socketInstance.on('employee_update', (updatedEmployee: Employee) => {
  //         setEmployees(prev => {
  //           const updated = prev.map(emp => 
  //             emp.id === updatedEmployee.id 
  //               ? { ...updatedEmployee, lateByMinutes: calculateLateness(updatedEmployee) }
  //               : emp
  //           );
  //           setLastUpdate(new Date());
  //           return updated;
  //         });
  //         toast.info(`Employee ${updatedEmployee.name} status updated`);
  //       });

  //       return () => {
  //         if (retryTimeout) clearTimeout(retryTimeout);
  //         socketInstance.disconnect();
  //       };
  //     } catch (error) {
  //       console.error('Socket.IO setup failed:', error);
  //       toast.error('Failed to initialize real-time connection');
  //     }
  //   };

  //   const cleanup = connectSocket();
  //   return cleanup;
  // }, []);

  const handlePrint = () => {
    window.print();
  };

  const handleDownloadReport = async (reportType: 'daily' | 'weekly' | 'monthly') => {
    const toastId = toast.loading(`Generating ${reportType} report...`);
    
    try {
      const controller = new AbortController();
      const timeoutId = setTimeout(() => controller.abort(), 10000); // 10 second timeout for reports
      
      // Check if API base URL is defined
      // The backend might be running on port 5000 or 5001 (fallback)
      const apiBaseUrl = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:5000';
      
      // Use the fetchWithPortFallback helper to try both ports
      const response = await fetchWithPortFallback(
        `${apiBaseUrl}/api/export-${reportType}`,
        { signal: controller.signal }
      );
      
      clearTimeout(timeoutId);
      
      if (!response.ok) {
        const errorText = await response.text().catch(() => 'Unknown error');
        throw new Error(`Failed to generate ${reportType} report: ${response.status} ${errorText}`);
      }

      const blob = await response.blob();
      
      // Check if the blob is empty or too small (likely an error)
      if (blob.size < 10) { // Arbitrary small size check
        throw new Error(`Generated ${reportType} report appears to be empty`);
      }
      
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.style.display = 'none';
      a.href = url;
      a.download = `attendance_${reportType}_${new Date().toISOString().split('T')[0]}.csv`;
      document.body.appendChild(a);
      a.click();
      window.URL.revokeObjectURL(url);
      document.body.removeChild(a);
      
      toast.success(`${reportType.charAt(0).toUpperCase() + reportType.slice(1)} report downloaded successfully`, {
        id: toastId
      });
    } catch (error) {
      console.error(`Error downloading ${reportType} report:`, error);
      
      if (error instanceof DOMException && error.name === 'AbortError') {
        toast.error(`Report generation timed out. Please try again later.`, {
          id: toastId
        });
      } else {
        toast.error(`Failed to download ${reportType} report: ${error instanceof Error ? error.message : 'Unknown error'}`, {
          id: toastId
        });
      }
    }
  };

  const handleRefresh = async () => {
    setIsRefreshing(true);
    toast.loading('Reconnecting to backend...');
    
    try {
      // Try to ping the backend before full refresh
      // Check if API base URL is defined
      // The backend might be running on port 5000 or 5001 (fallback)
      const apiBaseUrl = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:5000';
      
      // Use the fetchWithPortFallback helper to try both ports
      const response = await fetchWithPortFallback(`${apiBaseUrl}/health`, {
        method: 'GET',
        headers: { 'Cache-Control': 'no-cache' },
        signal: AbortSignal.timeout(3000) // 3 second timeout
      });
      
      if (response.ok) {
        toast.success('Backend connection restored! Refreshing data...');
        // Wait a moment for the toast to be visible
        setTimeout(() => window.location.reload(), 1000);
      } else {
        throw new Error('Backend not responding properly');
      }
    } catch (error) {
      console.error('Refresh connection error:', error);
      toast.error('Could not connect to backend. Please check if the server is running.');
      setIsRefreshing(false);
    }
  };

  if (isLoading) {
    return (
      <div className="min-h-screen bg-background flex items-center justify-center">
        <div className="text-center space-y-4">
          <RefreshCw className="h-8 w-8 animate-spin mx-auto text-primary" />
          <p className="text-lg text-muted-foreground">Loading StatusBoard...</p>
          <p className="text-sm text-muted-foreground">This may take a moment while connecting to the backend server</p>
          <Button 
            variant="outline" 
            size="sm" 
            className="mt-4"
            onClick={handleRefresh}
            disabled={isRefreshing}
          >
            <RefreshCw className={`h-4 w-4 mr-2 ${isRefreshing ? 'animate-spin' : ''}`} />
            {isRefreshing ? 'Connecting...' : 'Retry Connection'}
          </Button>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-background">
      {/* Header */}
      <header className="sticky top-0 z-50 bg-primary text-primary-foreground shadow-lg no-print">
        <div className="container mx-auto px-4 py-4">
          <div className="flex flex-col lg:flex-row lg:items-center lg:justify-between gap-4">
            <div className="flex items-center gap-4">
              <div>
                <h1 className="text-2xl font-bold">StatusBoard - Bio Metric</h1>
                <div className="flex items-center gap-2 text-sm opacity-90">
                  {isConnected ? (
                    <>
                      <Wifi className="h-4 w-4 text-green-400" />
                      <span className="text-green-400">Live Updates Active</span>
                    </>
                  ) : (
                    <>
                      <WifiOff className="h-4 w-4 text-yellow-400" />
                      <span className="text-yellow-400">Waiting for Connection</span>
                      <Button 
                        variant="ghost" 
                        size="sm" 
                        className="ml-2 h-6 px-2 py-0 text-xs"
                        onClick={handleRefresh}
                        disabled={isRefreshing}
                      >
                        <RefreshCw className={`h-3 w-3 mr-1 ${isRefreshing ? 'animate-spin' : ''}`} />
                        {isRefreshing ? 'Connecting...' : 'Reconnect'}
                      </Button>
                    </>
                  )}
                  <span>•</span>
                  <span>Last Update: {lastUpdate.toLocaleTimeString()}</span>
                </div>
              </div>
            </div>
            
            <div className="flex flex-wrap gap-2">
              <Button
                onClick={() => handleDownloadReport('daily')}
                variant="secondary"
                size="sm"
                className="flex items-center gap-2"
              >
                <FileText className="h-4 w-4" />
                Daily Report
              </Button>
              <Button
                onClick={() => handleDownloadReport('weekly')}
                variant="outline"
                size="sm"
                className="flex items-center gap-2 bg-accent text-accent-foreground hover:bg-accent/90"
              >
                <Calendar className="h-4 w-4" />
                Weekly Report
              </Button>
              <Button
                onClick={() => handleDownloadReport('monthly')}
                size="sm"
                className="flex items-center gap-2 bg-green-600 hover:bg-green-700 text-white"
              >
                <CalendarDays className="h-4 w-4" />
                Monthly Report
              </Button>
              <Button
                onClick={handlePrint}
                size="sm"
                className="flex items-center gap-2 bg-red-600 hover:bg-red-700 text-white print-button"
              >
                <Printer className="h-4 w-4" />
                Print
              </Button>
              <Button
                onClick={handleRefresh}
                variant="ghost"
                size="sm"
                className="flex items-center gap-2"
              >
                <RefreshCw className="h-4 w-4" />
                Refresh
              </Button>
            </div>
          </div>
        </div>
      </header>

      {/* Backend Status Alert */}
      {!isConnected && (
        <div className="bg-yellow-50 border-l-4 border-yellow-400 p-4 mx-4 mt-4">
          <div className="flex items-center">
            <AlertTriangle className="h-5 w-5 text-yellow-400 mr-3" />
            <div>
              <p className="text-sm text-yellow-700 font-medium">Backend Connection Issue</p>
              <p className="text-xs text-yellow-600 mt-1">
                Unable to connect to the backend server. Data may be stale or incomplete.
                <Button 
                  variant="link" 
                  size="sm" 
                  className="px-1 h-auto text-xs text-yellow-700 font-medium"
                  onClick={handleRefresh}
                  disabled={isRefreshing}
                >
                  {isRefreshing ? 'Reconnecting...' : 'Try reconnecting'}
                </Button>
              </p>
            </div>
          </div>
        </div>
      )}
      
      {/* Main Content */}
      <main className="container mx-auto px-4 py-6 space-y-6">
        {/* Statistics */}
        <StatisticsBar statistics={statistics} />

        {/* Analytics Row */}
        <div className="grid grid-cols-1 lg:grid-cols-2 xl:grid-cols-3 gap-6">
          <AttendancePieChart data={pieChartData} />
          <LateComersWidget title="Today's Top 10 Late Comers" lateComers={todayLateComers} />
          <NotPunchedInWidget employees={notPunchedInEmployees} />
        </div>

        {/* Yesterday's Late Comers and Detailed Attendance */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          <LateComersWidget title="Yesterday's Top 10 Late Comers" lateComers={yesterdayLateComers} />
          
          {/* Detailed Attendance Widget */}
          <DetailedAttendanceWidget employees={employees} />
        </div>

        {/* Employee Grid */}
        <div className="space-y-4">
          <div className="flex items-center justify-between">
            <h2 className="text-2xl font-bold">Employee Status ({employees.length})</h2>
            <div className="text-sm text-muted-foreground">
              Online: {employees.filter(emp => emp.isOnline).length} | 
              Offline: {employees.filter(emp => !emp.isOnline).length}
            </div>
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
            {employees.map((employee) => (
              <EmployeeCard key={employee.id} employee={employee} />
            ))}
          </div>
          
          {employees.length === 0 && (
            <div className="text-center py-12">
              <p className="text-lg text-muted-foreground">No employee data available</p>
              <Button onClick={handleRefresh} className="mt-4">
                <RefreshCw className="h-4 w-4 mr-2" />
                Refresh Data
              </Button>
            </div>
          )}
        </div>
      </main>

      <Toaster position="top-right" richColors />
    </div>
  );
}