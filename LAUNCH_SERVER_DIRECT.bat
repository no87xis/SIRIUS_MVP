@echo off
title Sirius Group MVP Server - Direct Launch
color 0A

echo.
echo ========================================
echo    🚀 SIRIUS GROUP MVP SERVER
echo    Direct Launch (No Terminal Issues)
echo ========================================
echo.

echo 🔍 Проверка Python...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python не найден!
    echo.
    echo 🔧 РЕШЕНИЕ:
    echo 1. Установите Python с https://www.python.org/downloads/
    echo 2. Или запустите install_python.ps1 от имени администратора
    echo.
    pause
    exit /b 1
)

echo ✅ Python найден!
python --version

echo.
echo 📦 Проверка зависимостей...
pip show fastapi >nul 2>&1
if %errorlevel% neq 0 (
    echo ⚠️ Устанавливаем зависимости...
    pip install -r requirements.txt
    if %errorlevel% neq 0 (
        echo ❌ Ошибка установки зависимостей
        pause
        exit /b 1
    )
    echo ✅ Зависимости установлены
) else (
    echo ✅ Зависимости готовы
)

echo.
echo ⚙️ Настройка конфигурации...
if not exist .env (
    if exist env.mvp (
        copy env.mvp .env >nul
        echo ✅ .env создан из env.mvp
    ) else (
        echo DATABASE_URL=sqlite:///./sirius.db > .env
        echo SECRET_KEY=Sirius_Local_Dev_ChangeMe_32chars_min >> .env
        echo SESSION_MAX_AGE=86400 >> .env
        echo ENVIRONMENT=development >> .env
        echo DEBUG=true >> .env
        echo LOG_LEVEL=INFO >> .env
        echo ✅ .env создан с базовыми настройками
    )
) else (
    echo ✅ .env уже существует
)

echo.
echo 🧪 Тестирование импортов...
python -c "from app.main import app; print('✅ Импорты работают')" 2>nul
if %errorlevel% neq 0 (
    echo ❌ Ошибка импортов
    echo 🔧 Попробуйте: pip install -r requirements.txt --force-reinstall
    pause
    exit /b 1
)

echo.
echo 🚀 ЗАПУСК СЕРВЕРА...
echo ========================================
echo 🌐 Сервер будет доступен по адресам:
echo.
echo    🏠 Главная:    http://127.0.0.1:8000
echo    🛒 Магазин:    http://127.0.0.1:8000/shop
echo    👤 Админ:      http://127.0.0.1:8000/admin
echo    📚 API Docs:   http://127.0.0.1:8000/docs
echo    🏥 Health:     http://127.0.0.1:8000/health
echo.
echo ⏹️ Для остановки сервера нажмите Ctrl+C
echo ========================================
echo.

REM Запускаем сервер
uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload

echo.
echo ⏹️ Сервер остановлен
pause



