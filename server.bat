@echo off
setlocal enabledelayedexpansion
cd /d "%~dp0"
title ARTHA - Accounting Software

echo ========================================================
echo   ARTHA Accounting Software - Server ^& Service Launcher
echo ========================================================
echo.
echo   Directory    : %~dp0
echo.

:: 1. Verify Node.js availability
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

if not defined NODE_CMD (
    echo [ERROR] Node.js is required but was not found in PATH or the app directory.
    echo Please install Node.js v18 or higher from https://nodejs.org/
    echo.
    pause
    exit /b 1
)

:: 2. Pre-bundle Tesseract assets if script is present
if exist "%~dp0scripts\bundle-tesseract-assets.mjs" (
    "%NODE_CMD%" "%~dp0scripts\bundle-tesseract-assets.mjs" >nul 2>&1
)

:: 3. Launch ARTHA.exe launcher
if exist "%~dp0ARTHA.exe" (
    echo   [OK] Launching ARTHA Launcher App [ARTHA.exe]...
    echo   Frontend and backend services will run as background services.
    echo   All real-time logs are monitored inside ARTHA.exe.
    echo.
    start "" "%~dp0ARTHA.exe" %*
    ping 127.0.0.1 -n 2 >nul
    exit /b 0
)

:: 4. Fallback if ARTHA.exe is missing
echo [WARNING] ARTHA.exe was not found in %~dp0.
echo Building ARTHA launcher now...
if exist "%~dp0launcher\ARTHA.Launcher.csproj" (
    where dotnet >nul 2>&1
    if !ERRORLEVEL! EQU 0 (
        echo Compiling ARTHA.exe via .NET...
        pushd "%~dp0launcher"
        dotnet publish -c Release -r win-x64 --self-contained true /p:PublishSingleFile=true /p:EnableCompressionInSingleFile=true /p:IncludeNativeLibrariesForSelfExtract=true -o "%~dp0publish-launcher" >nul 2>&1
        popd
        if exist "%~dp0publish-launcher\ARTHA.exe" (
            copy /y "%~dp0publish-launcher\ARTHA.exe" "%~dp0ARTHA.exe" >nul
            start "" "%~dp0ARTHA.exe" %*
            exit /b 0
        )
    )
)

echo [ERROR] Could not launch or build ARTHA.exe.
pause
exit /b 1
