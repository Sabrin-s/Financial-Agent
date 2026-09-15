@echo off
echo Starting FinSight AI Multi-Agent Intelligence System...

start "FinSight Backend" cmd /k "cd backend && set PYTHONPATH=. && python -m uvicorn app.main:app --reload --port 8000"
timeout /t 3 >nul
start "FinSight Frontend" cmd /k "cd frontend && npm run dev"

echo.
echo ====================================================
echo FinSight AI is booting!
echo Backend API docs: http://localhost:8000/docs
echo Interactive Dashboard: http://localhost:5173
echo ====================================================
