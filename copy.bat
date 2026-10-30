@echo off
setlocal enabledelayedexpansion
cd /d "%~dp0"

echo ===================================================
echo   ARTHA Project Source Code Bundle Generator
echo ===================================================
echo.

:: 1. Resolve Node.js executable
set "NODE_CMD="
if exist "%~dp0node\node.exe" (
    set "NODE_CMD=%~dp0node\node.exe"
) else (
    where node >nul 2>&1
    if !ERRORLEVEL! EQU 0 (
        for /f "delims=" %%I in ('where node') do (
            if not defined NODE_CMD set "NODE_CMD=%%I"
        )
    )
)

if not defined NODE_CMD if exist "D:\sdk\node-v24.13.0-win-x64\node.exe" (
    set "NODE_CMD=D:\sdk\node-v24.13.0-win-x64\node.exe"
)

if not defined NODE_CMD (
    echo [ERROR] Node.js is required but was not found in PATH or standard directories.
    echo Please install Node.js from https://nodejs.org/ to run this script.
    echo.
    if "%~1"=="" pause
    exit /b 1
)

echo [INFO] Node runtime : !NODE_CMD!
echo [INFO] Target bundle: %~dp0ARTHA.md
echo.

:: 2. Execute bundle generator script
"!NODE_CMD!" "%~dp0scripts\generate-artha-md.mjs" %*

if !ERRORLEVEL! EQU 0 (
    echo.
    echo ===================================================
    echo   [SUCCESS] ARTHA.md generated successfully!
    echo ===================================================
) else (
    echo.
    echo ===================================================
    echo   [ERROR] Failed to generate ARTHA.md (Code: !ERRORLEVEL!)
    echo ===================================================
)

echo.
if "%~1"=="" if not defined CI pause
exit /b !ERRORLEVEL!
