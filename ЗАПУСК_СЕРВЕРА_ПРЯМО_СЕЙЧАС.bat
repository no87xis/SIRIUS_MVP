@echo off
chcp 65001 >nul
title ЗАПУСК СЕРВЕРА SIRIUS - БЕЗ ПРОБЛЕМ С ТЕРМИНАЛОМ
color 0A

echo.
echo ========================================
echo    🚀 ЗАПУСК СЕРВЕРА SIRIUS
echo ========================================
echo.

echo 🔍 Поиск Python...

REM Проверяем разные варианты Python
set PYTHON_CMD=
if exist "C:\Python*\python.exe" (
    for /f %%i in ('dir /b "C:\Python*\python.exe" 2^>nul') do set PYTHON_CMD=%%i
)

REM Пробуем стандартные команды
py --version >nul 2>&1
if %errorlevel% equ 0 (
    set PYTHON_CMD=py
    echo    ✅ Найден Python launcher: py
    goto :run_server
)

python --version >nul 2>&1
if %errorlevel% equ 0 (
    set PYTHON_CMD=python
    echo    ✅ Найден Python: python
    goto :run_server
)

python3 --version >nul 2>&1
if %errorlevel% equ 0 (
    set PYTHON_CMD=python3
    echo    ✅ Найден Python3: python3
    goto :run_server
)

echo    ❌ Python не найден в PATH
echo.
echo 🔧 РЕШЕНИЯ:
echo 1. Установите Python с python.org
echo 2. Добавьте Python в PATH
echo 3. Или используйте полный путь к python.exe
echo.
pause
exit /b 1

:run_server
echo.
echo 🚀 Запуск сервера через %PYTHON_CMD%...
echo.

REM Переходим в папку проекта
cd /d "%~dp0"

REM Запускаем наш скрипт
%PYTHON_CMD% start_server_NOW.py

if %errorlevel% neq 0 (
    echo.
    echo ❌ Ошибка запуска сервера
    echo.
    echo 🔧 Попробуйте:
    echo 1. Установить зависимости: %PYTHON_CMD% -m pip install -r requirements.txt
    echo 2. Проверить код: %PYTHON_CMD% -c "from app.main import app; print('OK')"
    echo.
    pause
    exit /b 1
)

echo.
echo ✅ Скрипт завершен
pause
