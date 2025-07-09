export function GET() {
  // Create a simple CSV string
  const csvContent = 'Employee ID,Name,Team,Status,Last Punch Date,Last Punch Time\n' +
    'EMP001,John Doe,Engineering,Punched_In,2023-05-01,09:05:00\n' +
    'EMP002,Jane Smith,Design,Punched_In,2023-05-01,08:55:00\n' +
    'EMP003,Bob Johnson,Marketing,Break_In,2023-05-01,09:00:00\n' +
    'EMP004,Alice Williams,Sales,Punched_In,2023-05-01,08:50:00\n' +
    'EMP005,Charlie Brown,Support,Break_Out,2023-05-01,09:15:00\n' +
    'EMP006,Eva Green,HR,Punched_In,2023-05-01,08:45:00\n' +
    'EMP007,David Miller,Finance,Punched_In,2023-05-01,09:10:00\n' +
    'EMP008,Grace Lee,Product,Break_In,2023-05-01,09:20:00';

  return new Response(csvContent, {
    headers: {
      'Content-Type': 'text/csv',
      'Content-Disposition': 'attachment; filename="monthly_report.csv"',
    },
  });
}