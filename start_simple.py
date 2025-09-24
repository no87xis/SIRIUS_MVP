#!/usr/bin/env python3
"""
Простой запуск сервера без лишних проверок
"""

import sys
import os

# Добавляем текущую папку в путь
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    print("🔍 Импорт приложения...")
    from app.main import app
    print("✅ Приложение импортировано успешно")
    
    print("🚀 Запуск сервера...")
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000, reload=True)
    
except Exception as e:
    print(f"❌ Ошибка: {e}")
    import traceback
    traceback.print_exc()
    input("Нажмите Enter для выхода...")
