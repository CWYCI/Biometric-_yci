# StatusBoard - Bio Metric Attendance System

A real-time employee attendance monitoring dashboard built with Next.js, TypeScript, and Tailwind CSS.

## 🚀 Quick Start

### Prerequisites
- Node.js 18+ installed
- npm or yarn package manager

### Installation & Setup

1. **Clone or download this project**
2. **Install dependencies:**
   ```bash
   npm install
   ```

3. **Run the development server:**
   ```bash
   npm run dev
   ```

4. **Open your browser:**
   Navigate to [http://localhost:3000](http://localhost:3000)

## 📁 **Essential Project Structure**

```
statusboard/
├── **app/**                    # Next.js App Router
│   ├── api/                   # API routes
│   ├── globals.css           # Global styles
│   ├── layout.tsx            # Root layout
│   └── page.tsx              # Main dashboard page
├── **components/**            # React components
│   ├── ui/                   # shadcn/ui components
│   ├── AttendancePieChart.tsx
│   ├── EmployeeCard.tsx
│   ├── NotPunchedInYetCard.tsx
│   ├── StatisticsBar.tsx
│   └── TopLateComersCard.tsx
├── **lib/**                   # Utility functions
│   ├── business-logic.ts     # Core business logic
│   └── utils.ts              # Helper utilities
├── **types/**                 # TypeScript definitions
│   └── employee.ts           # Employee interfaces
├── package.json              # Dependencies
├── tailwind.config.ts        # Tailwind configuration
├── tsconfig.json            # TypeScript configuration
└── next.config.js           # Next.js configuration
```

## 🎨 Features

- **Real-time Dashboard** - Live employee status updates
- **Statistics Overview** - Comprehensive attendance metrics
- **Visual Charts** - Interactive pie charts with vibrant colors
- **Export Reports** - Download daily/weekly/monthly CSV reports
- **Print Support** - Print-friendly layouts
- **Responsive Design** - Works on all devices
- **Mock Data** - Works without backend for demo

## 🛠️ Available Scripts

```bash
npm run dev      # Start development server
npm run build    # Build for production
npm run start    # Start production server
npm run lint     # Run ESLint
```

## 🎯 Key Components

- **StatisticsBar**: Two-row layout with 5 cards each
- **AttendancePieChart**: Vibrant RGB color-coded status distribution
- **EmployeeCard**: Individual employee status cards
- **TopLateComersCard**: Late arrivals tracking
- **NotPunchedInYetCard**: Employees who haven't checked in

## 🌈 Color Scheme

The dashboard uses a professional color palette:
- **Working**: Vibrant Green (`rgb(34, 197, 94)`)
- **On Break**: Vibrant Orange (`rgb(251, 146, 60)`)
- **Available**: Vibrant Blue (`rgb(59, 130, 246)`)
- **Punched Out**: Vibrant Red (`rgb(239, 68, 68)`)
- **Offline**: Cool Gray (`rgb(156, 163, 175)`)

## 📱 Responsive Design

- Mobile-first approach
- Tablet and desktop optimized
- Print-friendly layouts
- High contrast mode support

## 🔧 Configuration

The app works with mock data by default. To connect to a real backend:

1. Set `NEXT_PUBLIC_BACKEND_URL` in your environment
2. Ensure your backend provides the expected API endpoints
3. The app will automatically switch from mock to real data

---

**Ready to run!** Just execute `npm run dev` and visit `http://localhost:3000`