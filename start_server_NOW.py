#!/usr/bin/env python3
"""
НЕМЕДЛЕННЫЙ ЗАПУСК СЕРВЕРА SIRIUS
Запуск без использования терминала с проблемным префиксом
"""

import sys
import os
import subprocess
from pathlib import Path

def main():
    print("🚀 ЗАПУСК СЕРВЕРА SIRIUS БЕЗ ТЕРМИНАЛА")
    print("=" * 50)
    
    # Проверяем Python
    print(f"🐍 Python версия: {sys.version}")
    
    # Проверяем рабочую директорию
    current_dir = Path.cwd()
    print(f"📁 Рабочая папка: {current_dir}")
    
    # Проверяем основные файлы
    required_files = ["app/main.py", "requirements.txt", "env.mvp"]
    missing_files = []
    
    for file in required_files:
        if Path(file).exists():
            print(f"   ✅ {file}")
        else:
            print(f"   ❌ {file}")
            missing_files.append(file)
    
    if missing_files:
        print(f"\n❌ Отсутствуют файлы: {missing_files}")
        return False
    
    # Создаем .env если нет
    if not Path(".env").exists() and Path("env.mvp").exists():
        import shutil
        shutil.copy("env.mvp", ".env")
        print("✅ .env создан из env.mvp")
    
    # Проверяем зависимости
    print("\n📦 Проверка зависимостей...")
    try:
        import fastapi
        import uvicorn
        import sqlalchemy
        print("   ✅ Основные зависимости установлены")
    except ImportError as e:
        print(f"   ❌ Отсутствует: {e}")
        print("   🔧 Устанавливаем зависимости...")
        
        try:
            subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], 
                          check=True, capture_output=True, text=True)
            print("   ✅ Зависимости установлены")
        except subprocess.CalledProcessError as e:
            print(f"   ❌ Ошибка установки: {e}")
            return False
    
    # Тестируем импорт приложения
    print("\n🧪 Тестирование импорта...")
    try:
        from app.main import app
        print("   ✅ Приложение импортировано успешно")
    except Exception as e:
        print(f"   ❌ Ошибка импорта: {e}")
        return False
    
    # Запускаем сервер
    print("\n🚀 ЗАПУСК СЕРВЕРА...")
    print("🌐 Сервер будет доступен на:")
    print("   📱 Главная:     http://127.0.0.1:8000")
    print("   🛒 Магазин:     http://127.0.0.1:8000/shop")
    print("   👤 Админка:     http://127.0.0.1:8000/admin")
    print("   📚 API Docs:    http://127.0.0.1:8000/docs")
    print("   🏥 Health:      http://127.0.0.1:8000/health")
    print("\n⏹️ Для остановки нажмите Ctrl+C")
    print("=" * 50)
    
    try:
        import uvicorn
        uvicorn.run(
            "app.main:app",
            host="127.0.0.1",
            port=8000,
            reload=True,
            log_level="info",
            access_log=True
        )
    except KeyboardInterrupt:
        print("\n⏹️ Сервер остановлен")
    except Exception as e:
        print(f"\n❌ Ошибка запуска сервера: {e}")
        return False
    
    return True

if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"\n💥 Критическая ошибка: {e}")
        input("Нажмите Enter для выхода...")
        sys.exit(1)
