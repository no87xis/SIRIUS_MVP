@echo off
title ПОЛНЫЙ ТЕСТ ТЕРМИНАЛА ПОСЛЕ ПЕРЕЗАГРУЗКИ
echo.
echo    🧪 ПОЛНЫЙ ТЕСТ ТЕРМИНАЛА ПОСЛЕ ПЕРЕЗАГРУЗКИ
echo    ===========================================
echo.

echo 🔍 ТЕСТ 1: Базовые команды cmd
echo ================================
echo.
echo Тест echo:
echo test
echo.
echo Тест dir:
dir /b | findstr /v "\.bat$" | findstr /v "\.txt$" | findstr /v "\.md$" | findstr /v "\.py$"
echo.
echo Тест cd:
cd
echo.

echo 🔍 ТЕСТ 2: Python команды
echo ==========================
echo.
echo Тест python --version:
python --version
echo.
echo Тест py --version:
py --version
echo.
echo Тест pip list:
pip list 2>nul | findstr /i "qr"
if %errorlevel%==0 (
    echo ❌ Найден пакет qr!
) else (
    echo ✅ Пакеты qr не найдены
)
echo.

echo 🔍 ТЕСТ 3: PowerShell команды
echo ==============================
echo.
echo Тест PowerShell:
powershell -Command "Write-Host 'PowerShell работает' -ForegroundColor Green"
echo.
echo Тест Get-Command:
powershell -Command "Get-Command python -ErrorAction SilentlyContinue"
echo.

echo 🔍 ТЕСТ 4: Кодировка
echo ====================
echo.
echo Текущая кодировка:
chcp
echo.
echo Тест русских символов:
echo Привет мир!
echo.

echo 🔍 ТЕСТ 5: Переменные окружения
echo ===============================
echo.
echo PATH:
echo %PATH% | findstr /i "qс"
if %errorlevel%==0 (
    echo ❌ Найден "qс" в PATH!
) else (
    echo ✅ "qс" не найден в PATH
)
echo.
echo PSModulePath:
echo %PSModulePath% | findstr /i "qс"
if %errorlevel%==0 (
    echo ❌ Найден "qс" в PSModulePath!
) else (
    echo ✅ "qс" не найден в PSModulePath
)
echo.

echo 🔍 ТЕСТ 6: Профили PowerShell
echo =============================
echo.
if exist "%USERPROFILE%\Documents\WindowsPowerShell\Microsoft.PowerShell_profile.ps1" (
    echo ❌ Найден профиль WindowsPowerShell
    type "%USERPROFILE%\Documents\WindowsPowerShell\Microsoft.PowerShell_profile.ps1" | findstr /i "qс"
    if %errorlevel%==0 (
        echo ❌ Найден "qс" в профиле!
    ) else (
        echo ✅ "qс" не найден в профиле
    )
) else (
    echo ✅ Профиль WindowsPowerShell не найден
)
echo.
if exist "%USERPROFILE%\Documents\PowerShell\Microsoft.PowerShell_profile.ps1" (
    echo ⚠️ Найден профиль PowerShell
    type "%USERPROFILE%\Documents\PowerShell\Microsoft.PowerShell_profile.ps1" | findstr /i "qс"
    if %errorlevel%==0 (
        echo ❌ Найден "qс" в профиле!
    ) else (
        echo ✅ "qс" не найден в профиле
    )
) else (
    echo ✅ Профиль PowerShell не найден
)
echo.

echo 🔍 ТЕСТ 7: Настройки Cursor
echo ============================
echo.
if exist "%APPDATA%\Cursor\User\settings.json" (
    echo ⚠️ Найден settings.json
    type "%APPDATA%\Cursor\User\settings.json" | findstr /i "qс"
    if %errorlevel%==0 (
        echo ❌ Найден "qс" в settings.json!
    ) else (
        echo ✅ "qс" не найден в settings.json
    )
) else (
    echo ✅ settings.json не найден
)
echo.

echo 🔍 ТЕСТ 8: Модули PowerShell
echo ============================
echo.
powershell -Command "Get-Module -ListAvailable | Where-Object {$_.Name -like '*qr*' -or $_.Name -like '*qс*'}"
if %errorlevel%==0 (
    echo ❌ Найдены подозрительные модули!
) else (
    echo ✅ Подозрительные модули не найдены
)
echo.

echo ✅ ТЕСТ ЗАВЕРШЕН!
echo.
echo 📊 РЕЗУЛЬТАТЫ:
echo - Если все тесты показывают ✅ - проблема решена!
echo - Если есть ❌ - проблема частично решена
echo - Если много ❌ - проблема не решена
echo.
pause
