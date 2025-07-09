@echo off
title StatusBoard Frontend Setup
echo ----------------------------------------
echo 🚀 Starting StatusBoard Frontend Setup...
echo ----------------------------------------

REM Navigate to project root
cd /d "C:\Biometric Project"

REM Create project folder
mkdir statusboard-frontend
cd statusboard-frontend

REM Create Next.js app with TypeScript
echo ⚙️ Creating Next.js app (with TypeScript + Tailwind)...
npx create-next-app@latest . --ts --app --no-eslint

echo ----------------------------------------
echo 📦 Installing additional dependencies...
REM Install ShadCN UI, Tailwind tools, Socket.IO
npm install @shadcn/ui @radix-ui/react-icons tailwind-variants class-variance-authority
npm install socket.io-client

echo ----------------------------------------
echo 🔐 Creating .env.local with backend URL...
echo NEXT_PUBLIC_BACKEND_URL=http://localhost:5000 > .env.local

echo ----------------------------------------
echo ✅ Setup complete. Starting development server...
npm run dev

pause
