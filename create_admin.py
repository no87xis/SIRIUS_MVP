#!/usr/bin/env python3
"""
Создание администратора для Sirius Group MVP
"""

import sys
import os
from pathlib import Path

# Добавляем корневую папку проекта в путь
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def create_admin_user():
    """Создание администратора"""
    print("👤 Создание администратора...")
    
    try:
        from app.db import get_db_sync
        from app.models import User
        from passlib.context import CryptContext
        
        # Настройка хеширования паролей
        pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        
        # Подключение к БД
        db = get_db_sync()
        
        # Проверяем, есть ли уже админ
        existing_admin = db.query(User).filter(User.username == "admin").first()
        if existing_admin:
            print("   ✅ Администратор уже существует")
            print(f"   👤 Имя пользователя: admin")
            print(f"   🔑 Пароль: admin12345")
            db.close()
            return True
        
        # Создаем нового администратора
        admin_user = User(
            username="admin",
            email="admin@sirius.local",
            full_name="Системный администратор",
            role="admin",
            is_active=True,
            hashed_password=pwd_context.hash("admin12345")
        )
        
        db.add(admin_user)
        db.commit()
        db.close()
        
        print("   ✅ Администратор создан успешно")
        print("   👤 Имя пользователя: admin")
        print("   🔑 Пароль: admin12345")
        print("   ⚠️ Смените пароль после первого входа!")
        
        return True
        
    except Exception as e:
        print(f"   ❌ Ошибка создания администратора: {e}")
        return False

def main():
    """Основная функция"""
    print("🔐 СОЗДАНИЕ АДМИНИСТРАТОРА SIRIUS GROUP MVP")
    print("=" * 50)
    
    if create_admin_user():
        print("\n✅ Администратор готов к использованию!")
        print("\n🌐 Для входа в админ-панель:")
        print("   1. Откройте http://127.0.0.1:8000/admin")
        print("   2. Введите логин: admin")
        print("   3. Введите пароль: admin12345")
        print("   4. Смените пароль после входа!")
        return True
    else:
        print("\n❌ Не удалось создать администратора")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
