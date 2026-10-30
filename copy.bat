@echo off
setlocal
cd /d "%~dp0"

echo ===================================================
echo   ARTHA Source Code Generator
echo ===================================================
echo.

where node >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Node.js is required but was not found in PATH.
    echo Please install Node.js from https://nodejs.org/ to run this script.
    echo.
    if "%~1"=="" pause
    exit /b 1
)

node "%~dp0scripts\generate-artha-md.mjs"

if %ERRORLEVEL% EQU 0 (
    echo.
    echo [SUCCESS] ARTHA.md generated successfully in the project root!
) else (
    echo.
    echo [ERROR] Failed to generate ARTHA.md.
)

echo.
if "%~1"=="" pause
