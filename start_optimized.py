#!/usr/bin/env python3
"""
Оптимизированный скрипт запуска сервера Sirius Group
Быстрый старт с минимальными зависимостями
"""

import sys
import os
import time
import asyncio
from pathlib import Path

# Добавляем корневую папку проекта в путь
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))


def check_environment():
    """Проверка окружения"""
    print("🔍 Проверка окружения...")
    
    # Проверяем Python версию
    if sys.version_info < (3, 8):
        print("❌ Требуется Python 3.8 или выше")
        return False
    
    # Проверяем основные зависимости
    try:
        import fastapi
        import uvicorn
        import sqlalchemy
        print("✅ Основные зависимости найдены")
    except ImportError as e:
        print(f"❌ Отсутствует зависимость: {e}")
        return False
    
    return True


def check_database():
    """Проверка базы данных"""
    print("🗄️ Проверка базы данных...")
    
    try:
        from app.config import settings
        from app.db import engine
        
        # Простая проверка подключения
        with engine.connect() as conn:
            conn.execute("SELECT 1")
        
        print("✅ База данных доступна")
        return True
        
    except Exception as e:
        print(f"⚠️ Проблема с базой данных: {e}")
        print("💡 База данных будет создана при первом запуске")
        return True  # Не критично для старта


def start_server():
    """Запуск сервера"""
    print("🚀 Запуск оптимизированного сервера...")
    
    try:
        import uvicorn
        from app.main import app
        
        print("✅ Приложение загружено успешно")
        print("🌐 Сервер будет доступен по адресу: http://localhost:8000")
        print("📚 API документация: http://localhost:8000/docs")
        print("🛑 Для остановки нажмите Ctrl+C")
        print("-" * 50)
        
        # Запуск с оптимизированными настройками
        uvicorn.run(
            app,
            host="127.0.0.1",  # Только локальный доступ для безопасности
            port=8000,
            reload=False,  # Отключаем reload для стабильности
            log_level="info",
            access_log=True,
            workers=1,  # Один воркер для стабильности
            loop="asyncio"
        )
        
    except ImportError as e:
        print(f"❌ Ошибка импорта: {e}")
        print("💡 Убедитесь, что установлены все зависимости: pip install -r requirements.txt")
        return False
    except Exception as e:
        print(f"❌ Ошибка запуска: {e}")
        return False


def main():
    """Основная функция"""
    print("🚀 Оптимизированный запуск Sirius Group")
    print("=" * 50)
    
    start_time = time.time()
    
    # Проверяем окружение
    if not check_environment():
        sys.exit(1)
    
    # Проверяем базу данных
    check_database()
    
    # Запускаем сервер
    print(f"⏱️ Время подготовки: {time.time() - start_time:.2f}s")
    start_server()


if __name__ == "__main__":
    main()
