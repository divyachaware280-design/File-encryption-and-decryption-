@echo off
title File Encryption and Decryption System
cd /d "%~dp0"

where python >nul 2>nul
if errorlevel 1 (
    echo Python is not installed or not in PATH.
    echo Download it from https://www.python.org/downloads/ and tick "Add Python to PATH".
    pause
    exit /b 1
)

python -c "import cryptography" >nul 2>nul
if errorlevel 1 (
    echo Installing required package: cryptography ...
    python -m pip install cryptography
    if errorlevel 1 (
        echo Installation failed. Check your internet connection.
        pause
        exit /b 1
    )
)

:menu
cls
echo ==========================================
echo    FILE ENCRYPTION AND DECRYPTION SYSTEM
echo           AES-256-GCM + Scrypt
echo ==========================================
echo.
echo   1. Encrypt a file
echo   2. Decrypt a file
echo   3. Exit
echo.
set "choice="
set /p choice=Enter your choice (1-3): 

if "%choice%"=="1" goto encrypt
if "%choice%"=="2" goto decrypt
if "%choice%"=="3" exit /b 0
echo Invalid choice.
timeout /t 2 >nul
goto menu

:encrypt
echo.
set "f="
set /p f=Enter file path (or drag and drop the file here): 
set "f=%f:"=%"
if not defined f goto menu
python file_crypto.py encrypt "%f%"
echo.
pause
goto menu

:decrypt
echo.
set "f="
set /p f=Enter .enc file path (or drag and drop the file here): 
set "f=%f:"=%"
if not defined f goto menu
python file_crypto.py decrypt "%f%"
echo.
pause
goto menu
