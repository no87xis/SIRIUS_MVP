#!/usr/bin/env python3
"""
Скрипт для запуска сервера Sirius Group
"""

import sys
import os
from pathlib import Path

# Добавляем корневую папку проекта в путь
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def main():
    """Запуск сервера"""
    print("🚀 Запуск сервера Sirius Group...")
    
    try:
        import uvicorn
        from app.main import app
        
        print("✅ Приложение загружено успешно")
        print("🌐 Сервер будет доступен по адресу: http://localhost:8000")
        print("📚 API документация: http://localhost:8000/docs")
        print("🛑 Для остановки нажмите Ctrl+C")
        print("-" * 50)
        
        uvicorn.run(
            app,
            host="0.0.0.0",
            port=8000,
            reload=True,
            log_level="info"
        )
        
    except ImportError as e:
        print(f"❌ Ошибка импорта: {e}")
        print("💡 Убедитесь, что установлены все зависимости: pip install -r requirements.txt")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Ошибка запуска: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
