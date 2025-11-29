@echo off
echo ========================================
echo Multi-Agent System Backend
echo ========================================
echo.
echo Installing dependencies...
pip install -r requirements.txt
echo.
echo Starting server...
python run_server.py
