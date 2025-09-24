# PowerShell скрипт для запуска Sirius Group MVP
# Запустите двойным щелчком или через PowerShell

Write-Host "🚀 SIRIUS GROUP MVP SERVER" -ForegroundColor Green
Write-Host "=" * 40

# Проверяем Python
Write-Host "`n🔍 Проверка Python..." -ForegroundColor Cyan
try {
    $pythonVersion = python --version 2>&1
    Write-Host "✅ Python найден: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Python не найден в PATH" -ForegroundColor Red
    Write-Host "🔧 РЕШЕНИЕ:" -ForegroundColor Yellow
    Write-Host "1. Перезагрузите компьютер после установки Python" -ForegroundColor White
    Write-Host "2. Или добавьте Python в PATH вручную" -ForegroundColor White
    Write-Host "3. Или используйте полный путь к python.exe" -ForegroundColor White
    Read-Host "`nНажмите Enter для выхода"
    exit 1
}

# Проверяем зависимости
Write-Host "`n📦 Проверка зависимостей..." -ForegroundColor Cyan
try {
    $fastapi = pip show fastapi 2>&1
    if ($fastapi -match "Name: fastapi") {
        Write-Host "✅ Зависимости готовы" -ForegroundColor Green
    } else {
        throw "FastAPI не найден"
    }
} catch {
    Write-Host "⚠️ Устанавливаем зависимости..." -ForegroundColor Yellow
    try {
        pip install -r requirements.txt
        Write-Host "✅ Зависимости установлены" -ForegroundColor Green
    } catch {
        Write-Host "❌ Ошибка установки зависимостей" -ForegroundColor Red
        Read-Host "Нажмите Enter для выхода"
        exit 1
    }
}

# Настраиваем конфигурацию
Write-Host "`n⚙️ Настройка конфигурации..." -ForegroundColor Cyan
if (-not (Test-Path ".env")) {
    if (Test-Path "env.mvp") {
        Copy-Item "env.mvp" ".env"
        Write-Host "✅ .env создан из env.mvp" -ForegroundColor Green
    } else {
        $envContent = @"
DATABASE_URL=sqlite:///./sirius.db
SECRET_KEY=Sirius_Local_Dev_ChangeMe_32chars_min
SESSION_MAX_AGE=86400
ENVIRONMENT=development
DEBUG=true
LOG_LEVEL=INFO
"@
        $envContent | Out-File -FilePath ".env" -Encoding UTF8
        Write-Host "✅ .env создан с базовыми настройками" -ForegroundColor Green
    }
} else {
    Write-Host "✅ .env уже существует" -ForegroundColor Green
}

# Тестируем импорты
Write-Host "`n🧪 Тестирование импортов..." -ForegroundColor Cyan
try {
    $importTest = python -c "from app.main import app; print('✅ Импорты работают')" 2>&1
    if ($importTest -match "✅ Импорты работают") {
        Write-Host "✅ Приложение готово к запуску" -ForegroundColor Green
    } else {
        throw "Ошибка импортов"
    }
} catch {
    Write-Host "❌ Ошибка импортов" -ForegroundColor Red
    Write-Host "🔧 Попробуйте: pip install -r requirements.txt --force-reinstall" -ForegroundColor Yellow
    Read-Host "Нажмите Enter для выхода"
    exit 1
}

# Запускаем сервер
Write-Host "`n🚀 ЗАПУСК СЕРВЕРА..." -ForegroundColor Green
Write-Host "=" * 40
Write-Host "🌐 Сервер будет доступен по адресам:" -ForegroundColor Cyan
Write-Host "`n   🏠 Главная:    http://127.0.0.1:8000" -ForegroundColor White
Write-Host "   🛒 Магазин:    http://127.0.0.1:8000/shop" -ForegroundColor White
Write-Host "   👤 Админ:      http://127.0.0.1:8000/admin" -ForegroundColor White
Write-Host "   📚 API Docs:   http://127.0.0.1:8000/docs" -ForegroundColor White
Write-Host "   🏥 Health:     http://127.0.0.1:8000/health" -ForegroundColor White
Write-Host "`n⏹️ Для остановки сервера нажмите Ctrl+C" -ForegroundColor Yellow
Write-Host "=" * 40

try {
    uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
} catch {
    Write-Host "`n❌ Ошибка запуска сервера" -ForegroundColor Red
    Write-Host "🔧 Попробуйте запустить вручную:" -ForegroundColor Yellow
    Write-Host "   uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload" -ForegroundColor White
    Read-Host "`nНажмите Enter для выхода"
}

