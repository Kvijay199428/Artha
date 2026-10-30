@echo off
setlocal
cd /d "%~dp0"
title ARTHA - BusyWin Data Importer

echo ========================================================
echo   ARTHA Accounting Software - BusyWin Data Importer
echo ========================================================
echo.
echo Source: C:\BusyWin\DATA\COMP0001
echo Target: %~dp0data
echo.

where python >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Python is required to run the BusyWin importer.
    pause
    exit /b 1
)

python "%~dp0scripts\import-busywin.py" %*

echo.
pause

