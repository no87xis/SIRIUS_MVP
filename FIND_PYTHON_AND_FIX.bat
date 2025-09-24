@echo off
title ПОИСК PYTHON И ИСПРАВЛЕНИЕ ПРЕФИКСА "qс"
echo.
echo    🔍 ПОИСК PYTHON И ИСПРАВЛЕНИЕ ПРЕФИКСА "qс"
echo    ===========================================
echo.

echo 🔍 Поиск Python в системе...
echo.

echo 📁 Проверяем стандартные места:
if exist "C:\Program Files\Python311\python.exe" (
    echo ✅ Найден: C:\Program Files\Python311\python.exe
    set PYTHON_PATH=C:\Program Files\Python311\python.exe
    goto :found_python
)
if exist "C:\Program Files\Python310\python.exe" (
    echo ✅ Найден: C:\Program Files\Python310\python.exe
    set PYTHON_PATH=C:\Program Files\Python310\python.exe
    goto :found_python
)
if exist "C:\Program Files\Python39\python.exe" (
    echo ✅ Найден: C:\Program Files\Python39\python.exe
    set PYTHON_PATH=C:\Program Files\Python39\python.exe
    goto :found_python
)

echo 📁 Проверяем пользовательские установки:
if exist "C:\Users\%USERNAME%\AppData\Local\Programs\Python\Python311\python.exe" (
    echo ✅ Найден: C:\Users\%USERNAME%\AppData\Local\Programs\Python\Python311\python.exe
    set PYTHON_PATH=C:\Users\%USERNAME%\AppData\Local\Programs\Python\Python311\python.exe
    goto :found_python
)
if exist "C:\Users\%USERNAME%\AppData\Local\Programs\Python\Python310\python.exe" (
    echo ✅ Найден: C:\Users\%USERNAME%\AppData\Local\Programs\Python\Python310\python.exe
    set PYTHON_PATH=C:\Users\%USERNAME%\AppData\Local\Programs\Python\Python310\python.exe
    goto :found_python
)

echo 📁 Поиск через where:
where /r C:\ python.exe 2>nul | findstr /v "WindowsApps" | findstr /v "Microsoft Store"
if %errorlevel%==0 (
    for /f "tokens=*" %%i in ('where /r C:\ python.exe 2^>nul ^| findstr /v "WindowsApps" ^| findstr /v "Microsoft Store"') do (
        echo ✅ Найден: %%i
        set PYTHON_PATH=%%i
        goto :found_python
    )
)

echo ❌ Python не найден в системе!
echo.
echo 🔧 РЕШЕНИЕ:
echo 1. Установите Python с https://python.org
echo 2. Или используйте py launcher: py -m pip uninstall qrcode -y
echo.
goto :try_py_launcher

:found_python
echo.
echo ✅ Python найден: %PYTHON_PATH%
echo.
echo 🔍 Проверяем версию:
"%PYTHON_PATH%" --version
echo.
echo 🔍 Шаг 1: Удаляем пакет qrcode...
"%PYTHON_PATH%" -m pip uninstall qrcode -y
"%PYTHON_PATH%" -m pip uninstall "qrcode[pil]" -y
echo.
echo 🔍 Шаг 2: Очищаем кэш pip...
"%PYTHON_PATH%" -m pip cache purge
echo.
echo 🔍 Шаг 3: Проверяем установленные пакеты...
"%PYTHON_PATH%" -m pip list | findstr /i qr
echo.
goto :cleanup_profiles

:try_py_launcher
echo 🔍 Пробуем py launcher...
py --version
if %errorlevel%==0 (
    echo ✅ py launcher работает!
    echo.
    echo 🔍 Удаляем qrcode через py launcher...
    py -m pip uninstall qrcode -y
    py -m pip uninstall "qrcode[pil]" -y
    py -m pip cache purge
    echo.
    echo 🔍 Проверяем установленные пакеты...
    py -m pip list | findstr /i qr
    echo.
) else (
    echo ❌ py launcher не работает
)

:cleanup_profiles
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
echo ✅ ИСПРАВЛЕНИЕ ЗАВЕРШЕНО!
echo.
echo 🔄 РЕКОМЕНДАЦИИ:
echo 1. Закройте ВСЕ терминалы
echo 2. Перезапустите Cursor
echo 3. Проверьте команды: echo ok, python --version
echo 4. Если проблема остается - перезагрузите компьютер
echo.
pause

