@echo off
title ГЛУБОКОЕ РАССЛЕДОВАНИЕ CURSOR
echo.
echo    🔍 ГЛУБОКОЕ РАССЛЕДОВАНИЕ CURSOR
echo    ================================
echo.

echo 🔍 Шаг 1: Проверяем процессы Cursor...
echo.
tasklist | findstr /i cursor
echo.

echo 🔍 Шаг 2: Проверяем автозагрузку Cursor...
echo.
if exist "%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup" (
    dir "%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup" | findstr /i cursor
)
echo.

echo 🔍 Шаг 3: Проверяем реестр Cursor...
echo.
reg query "HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Run" | findstr /i cursor
echo.

echo 🔍 Шаг 4: Проверяем переменные окружения Cursor...
echo.
set | findstr /i cursor
echo.

echo 🔍 Шаг 5: Проверяем настройки Cursor...
echo.
if exist "%APPDATA%\Cursor\User\settings.json" (
    echo Содержимое settings.json:
    type "%APPDATA%\Cursor\User\settings.json"
    echo.
    echo Поиск "qс" в settings.json:
    type "%APPDATA%\Cursor\User\settings.json" | findstr /i "qс"
    if %errorlevel%==0 (
        echo ❌ Найден "qс" в settings.json!
    ) else (
        echo ✅ "qс" не найден в settings.json
    )
) else (
    echo ❌ settings.json не найден
)
echo.

echo 🔍 Шаг 6: Проверяем расширения Cursor...
echo.
if exist "%APPDATA%\Cursor\extensions" (
    echo Расширения Cursor:
    dir "%APPDATA%\Cursor\extensions" /b
    echo.
    echo Поиск подозрительных расширений:
    dir "%APPDATA%\Cursor\extensions" /b | findstr /i "qr"
    if %errorlevel%==0 (
        echo ❌ Найдены подозрительные расширения!
    ) else (
        echo ✅ Подозрительные расширения не найдены
    )
) else (
    echo ❌ Папка расширений не найдена
)
echo.

echo 🔍 Шаг 7: Проверяем логи Cursor...
echo.
if exist "%APPDATA%\Cursor\logs" (
    echo Поиск "qс" в логах Cursor:
    findstr /s /i "qс" "%APPDATA%\Cursor\logs\*" 2>nul
    if %errorlevel%==0 (
        echo ❌ Найден "qс" в логах Cursor!
    ) else (
        echo ✅ "qс" не найден в логах
    )
) else (
    echo ❌ Папка логов не найдена
)
echo.

echo 🔍 Шаг 8: Проверяем конфигурацию терминала Cursor...
echo.
if exist "%APPDATA%\Cursor\User\settings.json" (
    echo Поиск настроек терминала:
    type "%APPDATA%\Cursor\User\settings.json" | findstr /i "terminal"
    echo.
    echo Поиск настроек shell:
    type "%APPDATA%\Cursor\User\settings.json" | findstr /i "shell"
) else (
    echo ❌ settings.json не найден
)
echo.

echo ✅ РАССЛЕДОВАНИЕ ЗАВЕРШЕНО!
echo.
echo 🔄 РЕКОМЕНДАЦИИ:
echo 1. Найдите подозрительные процессы Cursor
echo 2. Проверьте автозагрузку и реестр
echo 3. Удалите подозрительные расширения
echo 4. Очистите настройки терминала
echo.
pause
