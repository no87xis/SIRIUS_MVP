#!/usr/bin/env python3
"""
Запуск сервера Sirius Group MVP
Альтернативный способ запуска без терминала
"""

import sys
import os
import subprocess
import webbrowser
import time
from pathlib import Path

def check_python():
    """Проверка Python"""
    print("🐍 Проверка Python...")
    version = sys.version_info
    print(f"   Версия: {version.major}.{version.minor}.{version.micro}")
    
    if version.major >= 3 and version.minor >= 10:
        print("   ✅ Python >= 3.10 - OK")
        return True
    else:
        print("   ❌ Требуется Python >= 3.10")
        return False

def check_dependencies():
    """Проверка зависимостей"""
    print("📦 Проверка зависимостей...")
    
    try:
        import fastapi
        import uvicorn
        import sqlalchemy
        print("   ✅ Основные зависимости установлены")
        return True
    except ImportError as e:
        print(f"   ❌ Отсутствует зависимость: {e}")
        print("   🔧 Установите зависимости: pip install -r requirements.txt")
        return False

def check_config():
    """Проверка конфигурации"""
    print("⚙️ Проверка конфигурации...")
    
    # Проверяем .env
    if not Path(".env").exists():
        if Path("env.mvp").exists():
            import shutil
            shutil.copy("env.mvp", ".env")
            print("   ✅ .env создан из env.mvp")
        else:
            # Создаем базовый .env
            env_content = """# Local Development Configuration
DATABASE_URL=sqlite:///./sirius.db
SECRET_KEY=Sirius_Local_Dev_ChangeMe_32chars_min
SESSION_MAX_AGE=86400
ENVIRONMENT=development
DEBUG=true
LOG_LEVEL=INFO
"""
            with open(".env", "w") as f:
                f.write(env_content)
            print("   ✅ .env создан с базовыми настройками")
    else:
        print("   ✅ .env существует")
    
    # Создаем необходимые директории
    dirs = ["logs", "backups", "app/static", "app/templates"]
    for dir_path in dirs:
        Path(dir_path).mkdir(parents=True, exist_ok=True)
    
    print("   ✅ Директории созданы")
    return True

def test_imports():
    """Тестирование импортов"""
    print("🧪 Тестирование импортов...")
    
    try:
        from app.main import app
        print("   ✅ Импорты работают")
        return True
    except Exception as e:
        print(f"   ❌ Ошибка импортов: {e}")
        return False

def start_server():
    """Запуск сервера"""
    print("🚀 Запуск сервера...")
    
    try:
        import uvicorn
        from app.main import app
        
        print("   🌐 Сервер запускается на http://127.0.0.1:8000")
        print("   📚 API документация: http://127.0.0.1:8000/docs")
        print("   🛒 Магазин: http://127.0.0.1:8000/shop")
        print("   👤 Админ: http://127.0.0.1:8000/admin")
        print("   🏥 Health: http://127.0.0.1:8000/health")
        print("\n   ⏹️ Для остановки нажмите Ctrl+C")
        print("   " + "="*50)
        
        # Запускаем сервер
        uvicorn.run(
            app,
            host="127.0.0.1",
            port=8000,
            reload=True,
            log_level="info"
        )
        
    except Exception as e:
        print(f"   ❌ Ошибка запуска сервера: {e}")
        return False

def main():
    """Основная функция"""
    print("🚀 ЗАПУСК СЕРВЕРА SIRIUS GROUP MVP")
    print("=" * 50)
    
    # Проверки
    checks = [
        ("Проверка Python", check_python),
        ("Проверка зависимостей", check_dependencies),
        ("Проверка конфигурации", check_config),
        ("Тестирование импортов", test_imports)
    ]
    
    for check_name, check_func in checks:
        print(f"\n📋 {check_name}...")
        if not check_func():
            print(f"\n❌ {check_name} не пройдена!")
            print("🔧 Исправьте ошибки и повторите запуск")
            return False
    
    print("\n" + "=" * 50)
    print("✅ ВСЕ ПРОВЕРКИ ПРОЙДЕНЫ!")
    print("🚀 ЗАПУСКАЕМ СЕРВЕР...")
    print("=" * 50)
    
    # Запускаем сервер
    start_server()
    
    return True

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⏹️ Сервер остановлен пользователем")
    except Exception as e:
        print(f"\n❌ Критическая ошибка: {e}")
        sys.exit(1)
