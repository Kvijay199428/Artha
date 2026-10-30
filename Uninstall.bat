@echo off
setlocal
title ARTHA - Uninstall

echo ========================================================
echo   ARTHA Accounting Software - Uninstaller
echo ========================================================
echo.
echo This will remove ARTHA desktop shortcuts, start menu entries,
echo and Windows application registration.
echo.
set /p CONFIRM=Do you want to proceed with uninstallation? (Y/N): 
if /i not "%CONFIRM%"=="Y" exit /b 0

:: 1. Remove shortcuts
set "DESKTOP_LNK=%USERPROFILE%\Desktop\ARTHA.lnk"
if exist "%DESKTOP_LNK%" (
    del /f /q "%DESKTOP_LNK%"
    echo [OK] Removed Desktop shortcut.
)

set "SM_DIR=%APPDATA%\Microsoft\Windows\Start Menu\Programs\ARTHA"
if exist "%SM_DIR%" (
    rmdir /s /q "%SM_DIR%"
    echo [OK] Removed Start Menu shortcut.
)

:: 2. Clean registry
reg delete "HKCU\Software\Microsoft\Windows\CurrentVersion\Uninstall\ARTHA" /f >nul 2>&1
echo [OK] Removed Windows Registry application registration.

echo.
echo ========================================================
echo   ARTHA has been successfully uninstalled.
echo   Note: Your invoices and databases in '%~dp0data'
echo   were safely preserved.
echo ========================================================
echo.
pause

