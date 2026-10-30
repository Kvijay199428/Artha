@echo off
setlocal enabledelayedexpansion
cd /d "%~dp0"
title ARTHA - Setup & Installer

echo ========================================================
echo   ARTHA Accounting Software - Setup ^& Installation
echo ========================================================
echo.
echo   Current Location: %~dp0
echo.

:: 1. Launch Setup-ARTHA.exe if GUI installer is present
if "%1"=="" (
    if exist "%~dp0Setup-ARTHA.exe" (
        echo Launching ARTHA Graphical Setup Wizard...
        start "" "%~dp0Setup-ARTHA.exe"
        exit /b 0
    )
)

:: 2. CLI Setup mode
echo Configuring ARTHA Accounting Software...

:: Verify Node
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
    echo [ERROR] Node.js is not found. Please install Node.js from https://nodejs.org/
    pause
    exit /b 1
)

echo [1/4] Checking dependencies...
if not exist "%~dp0node_modules" (
    echo Installing node dependencies...
    call npm install
)

echo [2/4] Bundling Tesseract OCR assets...
if exist "%~dp0scripts\bundle-tesseract-assets.mjs" (
    "%NODE_CMD%" "%~dp0scripts\bundle-tesseract-assets.mjs"
)

echo [3/4] Creating Windows Shortcuts...
powershell -NoProfile -ExecutionPolicy Bypass -Command "$wsh = New-Object -ComObject WScript.Shell; $exe = Join-Path '%~dp0' 'ARTHA.exe'; $ico = Join-Path '%~dp0' 'release-templates\_system-scripts\app-icon.ico'; if(-not (Test-Path $ico)){ $ico = $exe }; $desktop = [Environment]::GetFolderPath('Desktop'); $sc = $wsh.CreateShortcut((Join-Path $desktop 'ARTHA.lnk')); $sc.TargetPath = $exe; $sc.WorkingDirectory = '%~dp0'; $sc.IconLocation = \"$ico,0\"; $sc.Description = 'ARTHA Accounting Software'; $sc.Save(); $sm = Join-Path ([Environment]::GetFolderPath('Programs')) 'ARTHA'; if(-not (Test-Path $sm)){ New-Item -ItemType Directory -Path $sm -Force | Out-Null }; $sc2 = $wsh.CreateShortcut((Join-Path $sm 'ARTHA.lnk')); $sc2.TargetPath = $exe; $sc2.WorkingDirectory = '%~dp0'; $sc2.IconLocation = \"$ico,0\"; $sc2.Description = 'ARTHA Accounting Software'; $sc2.Save(); Write-Host '  Shortcuts created on Desktop and Start Menu.'"

echo [4/4] Registering Windows Application...
powershell -NoProfile -ExecutionPolicy Bypass -Command "$reg = 'HKCU:\Software\Microsoft\Windows\CurrentVersion\Uninstall\ARTHA'; if(-not (Test-Path $reg)){ New-Item -Path $reg -Force | Out-Null }; Set-ItemProperty -Path $reg -Name 'DisplayName' -Value 'ARTHA Accounting Software'; Set-ItemProperty -Path $reg -Name 'DisplayVersion' -Value '1.10.80'; Set-ItemProperty -Path $reg -Name 'Publisher' -Value 'DiceCodes'; Set-ItemProperty -Path $reg -Name 'InstallLocation' -Value '%~dp0'; Set-ItemProperty -Path $reg -Name 'DisplayIcon' -Value (Join-Path '%~dp0' 'release-templates\_system-scripts\app-icon.ico'); Set-ItemProperty -Path $reg -Name 'UninstallString' -Value (Join-Path '%~dp0' 'Uninstall.bat');"

echo.
echo ========================================================
echo   ARTHA setup successfully completed!
echo   You can launch ARTHA from your Desktop shortcut or
echo   by running server.bat / ARTHA.exe.
echo ========================================================
echo.
pause

