@echo off
title ГЛУБОКАЯ ОЧИСТКА ПРЕФИКСА "qс"
echo.
echo    🚨 ГЛУБОКАЯ ОЧИСТКА ПРЕФИКСА "qс"
echo    =================================
echo.

echo 🔍 Шаг 1: Проверяем ВСЕ профили PowerShell...
echo.

echo 📁 Проверяем профили пользователя:
if exist "%USERPROFILE%\Documents\WindowsPowerShell\Microsoft.PowerShell_profile.ps1" (
    echo ⚠️ Найден: %USERPROFILE%\Documents\WindowsPowerShell\Microsoft.PowerShell_profile.ps1
    type "%USERPROFILE%\Documents\WindowsPowerShell\Microsoft.PowerShell_profile.ps1" | findstr /i "qс"
    if %errorlevel%==0 (
        echo ❌ Найден "qс" в профиле!
        del "%USERPROFILE%\Documents\WindowsPowerShell\Microsoft.PowerShell_profile.ps1"
        echo ✅ Профиль удален
    ) else (
        echo ✅ "qс" не найден в профиле
    )
)

if exist "%USERPROFILE%\Documents\PowerShell\Microsoft.PowerShell_profile.ps1" (
    echo ⚠️ Найден: %USERPROFILE%\Documents\PowerShell\Microsoft.PowerShell_profile.ps1
    type "%USERPROFILE%\Documents\PowerShell\Microsoft.PowerShell_profile.ps1" | findstr /i "qс"
    if %errorlevel%==0 (
        echo ❌ Найден "qс" в профиле!
        del "%USERPROFILE%\Documents\PowerShell\Microsoft.PowerShell_profile.ps1"
        echo ✅ Профиль удален
    ) else (
        echo ✅ "qс" не найден в профиле
    )
)

echo.
echo 📁 Проверяем системные профили:
if exist "%WINDIR%\System32\WindowsPowerShell\v1.0\Microsoft.PowerShell_profile.ps1" (
    echo ⚠️ Найден системный профиль
    type "%WINDIR%\System32\WindowsPowerShell\v1.0\Microsoft.PowerShell_profile.ps1" | findstr /i "qс"
    if %errorlevel%==0 (
        echo ❌ Найден "qс" в системном профиле!
        echo ⚠️ Требуются права администратора для удаления
    )
)

echo.
echo 🔍 Шаг 2: Проверяем переменные окружения PowerShell...
echo.

echo PSModulePath:
echo %PSModulePath% | findstr /i "qс"
if %errorlevel%==0 (
    echo ❌ Найден "qс" в PSModulePath!
    echo Текущий PSModulePath: %PSModulePath%
) else (
    echo ✅ "qс" не найден в PSModulePath
)

echo.
echo 🔍 Шаг 3: Проверяем реестр...
echo.

reg query "HKEY_CURRENT_USER\Software\Microsoft\PowerShell" /s 2>nul | findstr /i "qс"
if %errorlevel%==0 (
    echo ❌ Найден "qс" в реестре PowerShell!
    echo ⚠️ Требуются права администратора для очистки
) else (
    echo ✅ "qс" не найден в реестре PowerShell
)

echo.
echo 🔍 Шаг 4: Проверяем модули PowerShell...
echo.

powershell -Command "Get-Module -ListAvailable | Where-Object {$_.Name -like '*qr*' -or $_.Name -like '*qс*'}"
if %errorlevel%==0 (
    echo ❌ Найден подозрительный модуль!
) else (
    echo ✅ Подозрительные модули не найдены
)

echo.
echo 🔍 Шаг 5: Создаем чистый профиль PowerShell...
echo.

echo # Чистый профиль PowerShell > "%USERPROFILE%\Documents\PowerShell\Microsoft.PowerShell_profile.ps1"
echo # Создан автоматически для исправления префикса "qс" >> "%USERPROFILE%\Documents\PowerShell\Microsoft.PowerShell_profile.ps1"
echo Write-Host "Профиль PowerShell загружен" -ForegroundColor Green >> "%USERPROFILE%\Documents\PowerShell\Microsoft.PowerShell_profile.ps1"

echo ✅ Создан чистый профиль PowerShell

echo.
echo 🔍 Шаг 6: Проверяем Cursor настройки...
echo.

if exist "%APPDATA%\Cursor\User\settings.json" (
    echo ⚠️ Найден файл настроек Cursor
    type "%APPDATA%\Cursor\User\settings.json" | findstr /i "qс"
    if %errorlevel%==0 (
        echo ❌ Найден "qс" в настройках Cursor!
        echo ⚠️ Требуется ручная очистка настроек
    ) else (
        echo ✅ "qс" не найден в настройках Cursor
    )
)

echo.
echo ✅ ГЛУБОКАЯ ОЧИСТКА ЗАВЕРШЕНА!
echo.
echo 🔄 РЕКОМЕНДАЦИИ:
echo 1. Закройте ВСЕ терминалы и Cursor
echo 2. Перезагрузите компьютер
echo 3. Запустите Cursor заново
echo 4. Если проблема остается - переустановите Cursor
echo 5. Проверьте антивирус - возможно он блокирует изменения
echo.
pause

