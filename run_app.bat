@echo off
title FLOODTWIN AI - NDRF Decision Support Platform
echo =====================================================================
echo  FLOODTWIN AI - Launching Full-Stack Hyper-Local Flash Flood Platform
echo =====================================================================
echo.
echo Starting FastAPI Server on http://127.0.0.1:8000 ...
start "" "http://127.0.0.1:8000"
python backend/main.py
pause
