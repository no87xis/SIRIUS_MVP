@echo off
title ЭКСТРЕННОЕ ИСПРАВЛЕНИЕ ПРЕФИКСА "qс" - УЛУЧШЕННАЯ ВЕРСИЯ
echo.
echo    🚨 ЭКСТРЕННОЕ ИСПРАВЛЕНИЕ "qс" - УЛУЧШЕННАЯ ВЕРСИЯ
echo    ===================================================
echo.

echo 🔍 Поиск Python...
set PYTHON_PATH=
for %%i in (python.exe) do set PYTHON_PATH=%%~$PATH:i
if "%PYTHON_PATH%"=="" (
    echo ❌ Python не найден в PATH
    echo 🔍 Поиск в стандартных местах...
    if exist "C:\Program Files\Python311\python.exe" set PYTHON_PATH=C:\Program Files\Python311\python.exe
    if exist "C:\Program Files\Python310\python.exe" set PYTHON_PATH=C:\Program Files\Python310\python.exe
    if exist "C:\Program Files\Python39\python.exe" set PYTHON_PATH=C:\Program Files\Python39\python.exe
    if exist "C:\Users\%USERNAME%\AppData\Local\Programs\Python\Python311\python.exe" set PYTHON_PATH=C:\Users\%USERNAME%\AppData\Local\Programs\Python\Python311\python.exe
    if exist "C:\Users\%USERNAME%\AppData\Local\Programs\Python\Python310\python.exe" set PYTHON_PATH=C:\Users\%USERNAME%\AppData\Local\Programs\Python\Python310\python.exe
)

if "%PYTHON_PATH%"=="" (
    echo ❌ Python не найден! Установите Python или добавьте в PATH
    pause
    exit /b 1
)

echo ✅ Python найден: %PYTHON_PATH%

echo.
echo 🔍 Шаг 1: Удаляем пакет qrcode...
"%PYTHON_PATH%" -m pip uninstall qrcode -y
"%PYTHON_PATH%" -m pip uninstall "qrcode[pil]" -y

echo.
echo 🔍 Шаг 2: Очищаем кэш pip...
"%PYTHON_PATH%" -m pip cache purge

echo.
echo 🔍 Шаг 3: Проверяем переменные окружения...
echo Текущий PATH: %PATH%
echo.
echo 🔍 Поиск "qс" в PATH...
echo %PATH% | findstr /i "qс" >nul
if %errorlevel%==0 (
    echo ⚠️ Найден "qс" в PATH!
    echo 🔧 Очищаем PATH...
    for /f "tokens=*" %%a in ('echo %PATH%') do (
        set "CLEAN_PATH=%%a"
        set "CLEAN_PATH=!CLEAN_PATH:qс=!"
    )
    echo Новый PATH: !CLEAN_PATH!
    echo.
    echo ⚠️ ВНИМАНИЕ: Для изменения системных переменных нужны права администратора
    echo Запустите этот скрипт от имени администратора для полного исправления
) else (
    echo ✅ "qс" не найден в PATH
)

echo.
echo 🔍 Шаг 4: Очищаем профили PowerShell...
if exist "%USERPROFILE%\Documents\WindowsPowerShell\Microsoft.PowerShell_profile.ps1" (
    echo ⚠️ Найден профиль: %USERPROFILE%\Documents\WindowsPowerShell\Microsoft.PowerShell_profile.ps1
    del "%USERPROFILE%\Documents\WindowsPowerShell\Microsoft.PowerShell_profile.ps1"
    echo ✅ Профиль удален
)
if exist "%USERPROFILE%\Documents\PowerShell\Microsoft.PowerShell_profile.ps1" (
    echo ⚠️ Найден профиль: %USERPROFILE%\Documents\PowerShell\Microsoft.PowerShell_profile.ps1
    del "%USERPROFILE%\Documents\PowerShell\Microsoft.PowerShell_profile.ps1"
    echo ✅ Профиль удален
)

echo.
echo 🔍 Шаг 5: Проверяем установленные пакеты...
"%PYTHON_PATH%" -m pip list | findstr /i qr

echo.
echo ✅ ИСПРАВЛЕНИЕ ЗАВЕРШЕНО!
echo.
echo 🔄 РЕКОМЕНДАЦИИ:
echo 1. Закройте ВСЕ терминалы
echo 2. Перезапустите Cursor
echo 3. Проверьте команды: echo ok, python --version
echo 4. Если проблема остается - перезагрузите компьютер
echo 5. Для полного исправления запустите скрипт от имени администратора
echo.
pause

