export function GET() {
  // Create a simple CSV string
  const csvContent = 'Employee ID,Name,Team,Status,Last Punch Date,Last Punch Time\n' +
    'EMP001,John Doe,Engineering,Punched_In,2023-05-01,09:05:00\n' +
    'EMP002,Jane Smith,Design,Punched_In,2023-05-01,08:55:00\n' +
    'EMP003,Bob Johnson,Marketing,Break_In,2023-05-01,09:00:00';

  return new Response(csvContent, {
    headers: {
      'Content-Type': 'text/csv',
      'Content-Disposition': 'attachment; filename="daily_report.csv"',
    },
  });
}