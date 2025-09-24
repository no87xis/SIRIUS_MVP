@echo off
title ПОИСК И УДАЛЕНИЕ ПОДОЗРИТЕЛЬНОГО МОДУЛЯ
echo.
echo    🚨 ПОИСК И УДАЛЕНИЕ ПОДОЗРИТЕЛЬНОГО МОДУЛЯ
echo    ==========================================
echo.

echo 🔍 Шаг 1: Полный список модулей PowerShell...
echo.

powershell -Command "Get-Module -ListAvailable | Format-Table Name, Version, ModuleBase -AutoSize"

echo.
echo 🔍 Шаг 2: Поиск модулей с кириллическими символами...
echo.

powershell -Command "Get-Module -ListAvailable | Where-Object {$_.Name -match '[а-яё]' -or $_.Name -like '*qr*' -or $_.Name -like '*qс*'}"

echo.
echo 🔍 Шаг 3: Поиск модулей в стандартных местах...
echo.

echo 📁 Проверяем: %USERPROFILE%\Documents\WindowsPowerShell\Modules
if exist "%USERPROFILE%\Documents\WindowsPowerShell\Modules" (
    dir "%USERPROFILE%\Documents\WindowsPowerShell\Modules" /b
    echo.
    echo 🔍 Поиск "qс" в модулях:
    findstr /s /i "qс" "%USERPROFILE%\Documents\WindowsPowerShell\Modules\*" 2>nul
    if %errorlevel%==0 (
        echo ❌ Найден "qс" в модулях!
    ) else (
        echo ✅ "qс" не найден в модулях
    )
) else (
    echo ❌ Папка модулей не найдена
)

echo.
echo 📁 Проверяем: %USERPROFILE%\Documents\PowerShell\Modules
if exist "%USERPROFILE%\Documents\PowerShell\Modules" (
    dir "%USERPROFILE%\Documents\PowerShell\Modules" /b
    echo.
    echo 🔍 Поиск "qс" в модулях:
    findstr /s /i "qс" "%USERPROFILE%\Documents\PowerShell\Modules\*" 2>nul
    if %errorlevel%==0 (
        echo ❌ Найден "qс" в модулях!
    ) else (
        echo ✅ "qс" не найден в модулях
    )
) else (
    echo ❌ Папка модулей не найдена
)

echo.
echo 📁 Проверяем системные модули: %WINDIR%\System32\WindowsPowerShell\v1.0\Modules
if exist "%WINDIR%\System32\WindowsPowerShell\v1.0\Modules" (
    dir "%WINDIR%\System32\WindowsPowerShell\v1.0\Modules" /b | findstr /i "qr"
    if %errorlevel%==0 (
        echo ❌ Найдены подозрительные системные модули!
    ) else (
        echo ✅ Подозрительные системные модули не найдены
    )
)

echo.
echo 🔍 Шаг 4: Поиск файлов с "qс" в системе...
echo.

echo 🔍 Поиск в папке пользователя:
findstr /s /i "qс" "%USERPROFILE%\*" 2>nul | findstr /v "AppData\Local\Temp" | findstr /v "AppData\Roaming\Microsoft\Windows\Recent"

echo.
echo 🔍 Шаг 5: Проверяем автозагрузку...
echo.

echo 📁 Проверяем автозагрузку пользователя:
if exist "%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup" (
    dir "%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup" /b
)

echo.
echo 📁 Проверяем системную автозагрузку:
if exist "%ALLUSERSPROFILE%\Microsoft\Windows\Start Menu\Programs\Startup" (
    dir "%ALLUSERSPROFILE%\Microsoft\Windows\Start Menu\Programs\Startup" /b
)

echo.
echo ✅ ПОИСК ЗАВЕРШЕН!
echo.
echo 🔄 РЕКОМЕНДАЦИИ:
echo 1. Найдите подозрительный модуль в списке выше
echo 2. Удалите его вручную
echo 3. Перезагрузите компьютер
echo 4. Проверьте терминал
echo.
pause

