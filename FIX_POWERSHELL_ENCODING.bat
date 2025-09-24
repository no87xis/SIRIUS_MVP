@echo off
title ИСПРАВЛЕНИЕ КОДИРОВКИ POWERSHELL
echo.
echo    🔧 ИСПРАВЛЕНИЕ КОДИРОВКИ POWERSHELL
echo    ===================================
echo.

echo 🔍 Шаг 1: Проверяем текущую кодировку...
echo.

echo Текущая кодовая страница:
chcp

echo.
echo 🔍 Шаг 2: Устанавливаем правильную кодировку...
echo.

echo Устанавливаем UTF-8 (65001)...
chcp 65001

echo.
echo 🔍 Шаг 3: Проверяем кодировку после изменения...
echo.

chcp

echo.
echo 🔍 Шаг 4: Тестируем команды...
echo.

echo Тест команды echo:
echo test

echo.
echo Тест команды dir:
dir /b | head -5

echo.
echo 🔍 Шаг 5: Проверяем PowerShell...
echo.

powershell -Command "Write-Host 'Тест PowerShell' -ForegroundColor Green"

echo.
echo 🔍 Шаг 6: Очищаем профили PowerShell...
echo.

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
echo 🔍 Шаг 7: Создаем чистый профиль PowerShell...
echo.

echo # Чистый профиль PowerShell > "%USERPROFILE%\Documents\PowerShell\Microsoft.PowerShell_profile.ps1"
echo # Создан автоматически для исправления кодировки >> "%USERPROFILE%\Documents\PowerShell\Microsoft.PowerShell_profile.ps1"
echo [Console]::OutputEncoding = [System.Text.Encoding]::UTF8 >> "%USERPROFILE%\Documents\PowerShell\Microsoft.PowerShell_profile.ps1"
echo $OutputEncoding = [System.Text.Encoding]::UTF8 >> "%USERPROFILE%\Documents\PowerShell\Microsoft.PowerShell_profile.ps1"
echo Write-Host "Профиль PowerShell загружен с UTF-8" -ForegroundColor Green >> "%USERPROFILE%\Documents\PowerShell\Microsoft.PowerShell_profile.ps1"

echo ✅ Создан чистый профиль PowerShell с UTF-8

echo.
echo ✅ ИСПРАВЛЕНИЕ КОДИРОВКИ ЗАВЕРШЕНО!
echo.
echo 🔄 РЕКОМЕНДАЦИИ:
echo 1. Закройте ВСЕ терминалы
echo 2. Перезапустите Cursor
echo 3. Проверьте терминал - кракозябры должны исчезнуть
echo 4. Если проблема остается - перезагрузите компьютер
echo.
pause

