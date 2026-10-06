@echo off
setlocal
cd /d "%~dp0"
title LanQiao Python OJ

rem ---- find a working Python ----
set "PYEXE="
py -3.13 -c "print(1)" >nul 2>nul && set "PYEXE=py -3.13"
if not defined PYEXE py -c "print(1)" >nul 2>nul && set "PYEXE=py"
if not defined PYEXE python -c "print(1)" >nul 2>nul && set "PYEXE=python"

if not defined PYEXE (
  echo [ERROR] Python 3.10 or newer is not found.
  echo         Install it from https://www.python.org/downloads/
  echo         and tick "Add python.exe to PATH" during setup.
  echo.
  pause
  exit /b 1
)

if not exist problems\p01_year_string.json (
  echo [HINT] problem set is empty. Build it first:
  echo        %PYEXE% generator\build_problems.py
  echo.
)

set PYTHONDONTWRITEBYTECODE=1
set PYTHONIOENCODING=utf-8
chcp 65001 >nul
echo ============================================================
echo  LanQiao Cup Python practice OJ  (local, offline)
echo  Using : %PYEXE%
echo  The browser opens by itself. If port 8000 is busy,
echo  the window will print the address actually used.
echo  Stop  : close this window
echo ============================================================
echo.

%PYEXE% server\app.py

echo.
echo Server has stopped.
pause
