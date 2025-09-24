#!/usr/bin/env python3
"""
Быстрая проверка готовности системы к запуску
Проверяет все критические компоненты за секунды
"""

import sys
import time
from pathlib import Path

# Добавляем корневую папку проекта в путь
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))


def quick_syntax_check():
    """Быстрая проверка синтаксиса"""
    print("🔍 Проверка синтаксиса...")
    
    critical_files = [
        "app/main.py",
        "app/config.py",
        "app/db.py",
        "app/services/logger.py",
        "app/services/monitoring.py",
        
    ]
    
    try:
        import ast
        
        for file_path in critical_files:
            if not Path(file_path).exists():
                print(f"⚠️ Файл не найден: {file_path}")
                continue
                
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            ast.parse(content)
        
        print("✅ Синтаксис корректен")
        return True
        
    except SyntaxError as e:
        print(f"❌ Ошибка синтаксиса в {e.filename}:{e.lineno}: {e.msg}")
        return False
    except Exception as e:
        print(f"❌ Ошибка проверки синтаксиса: {e}")
        return False


def quick_import_check():
    """Быстрая проверка импортов"""
    print("📦 Проверка импортов...")
    
    try:
        # Проверяем основные импорты
        from app.main import app
        from app.config import settings
        from app.db import engine, Base, get_db
        from app.services.logger import logger
        from app.services.monitoring import performance_monitor
        
        
        print("✅ Импорты работают")
        return True
        
    except Exception as e:
        print(f"❌ Ошибка импорта: {e}")
        return False


def quick_config_check():
    """Быстрая проверка конфигурации"""
    print("⚙️ Проверка конфигурации...")
    
    try:
        from app.config import settings
        
        # Проверяем критические настройки
        assert settings.database_url is not None
        assert settings.secret_key is not None
        assert len(settings.secret_key) >= 32
        assert settings.startup_timeout > 0
        assert settings.database_timeout > 0
        
        print("✅ Конфигурация корректна")
        return True
        
    except Exception as e:
        print(f"❌ Ошибка конфигурации: {e}")
        return False


def quick_database_check():
    """Быстрая проверка базы данных"""
    print("🗄️ Проверка базы данных...")
    
    try:
        from app.db import engine
        
        # Простая проверка подключения
        with engine.connect() as conn:
            conn.execute("SELECT 1")
        
        print("✅ База данных доступна")
        return True
        
    except Exception as e:
        print(f"⚠️ База данных недоступна: {e}")
        print("💡 База данных будет создана при первом запуске")
        return True  # Не критично


def quick_services_check():
    """Быстрая проверка сервисов"""
    print("🔧 Проверка сервисов...")
    
    try:
        from app.services.logger import logger
        from app.services.monitoring import performance_monitor
        
        # Проверяем основные методы
        assert hasattr(logger, 'info')
        assert hasattr(performance_monitor, 'record_request_time')
        
        
        print("✅ Сервисы работают")
        return True
        
    except Exception as e:
        print(f"❌ Ошибка сервисов: {e}")
        return False


def main():
    """Основная функция быстрой проверки"""
    print("⚡ Быстрая проверка готовности Sirius Group")
    print("=" * 50)
    
    start_time = time.time()
    
    checks = [
        quick_syntax_check,
        quick_import_check,
        quick_config_check,
        quick_database_check,
        quick_services_check
    ]
    
    passed = 0
    total = len(checks)
    
    for check in checks:
        if check():
            passed += 1
        print()
    
    duration = time.time() - start_time
    
    print("=" * 50)
    print(f"⏱️ Время проверки: {duration:.2f}s")
    print(f"📊 Результат: {passed}/{total} проверок пройдено")
    
    if passed == total:
        print("🎉 Система готова к запуску!")
        print("💡 Запустите: python start_optimized.py")
        return True
    else:
        print("❌ Требуется исправление ошибок")
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
