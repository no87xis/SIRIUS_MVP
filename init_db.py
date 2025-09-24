#!/usr/bin/env python3
"""
Скрипт для инициализации базы данных
Создает таблицы и добавляет начальные данные
"""

import sys
import os
from pathlib import Path

# Добавляем корневую папку проекта в путь
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from app.db import engine, Base, SessionLocal
from app.models import User, UserRole, Product, ProductStatus
from app.services.auth import get_password_hash
from app.product_constants import DEFAULT_STATUS


def create_tables():
    """Создает все таблицы в базе данных"""
    print("Создание таблиц...")
    Base.metadata.create_all(bind=engine)
    print("✅ Таблицы созданы успешно")


def create_default_users():
    """Создает пользователей по умолчанию"""
    print("Создание пользователей по умолчанию...")
    
    db = SessionLocal()
    try:
        # Проверяем, есть ли уже пользователи
        if db.query(User).count() > 0:
            print("⚠️ Пользователи уже существуют, пропускаем создание")
            return
        
        # Создаем администратора
        admin_user = User(
            username="admin",
            hashed_password=get_password_hash("admin123"),
            role=UserRole.ADMIN,
            is_active=True,
            is_superuser=True
        )
        db.add(admin_user)
        
        # Создаем менеджера
        manager_user = User(
            username="manager",
            hashed_password=get_password_hash("manager123"),
            role=UserRole.MANAGER,
            is_active=True,
            is_superuser=False
        )
        db.add(manager_user)
        
        # Создаем обычного пользователя
        user_user = User(
            username="user",
            hashed_password=get_password_hash("user123"),
            role=UserRole.USER,
            is_active=True,
            is_superuser=False
        )
        db.add(user_user)
        
        db.commit()
        print("✅ Пользователи созданы успешно")
        print("   - admin / admin123 (Администратор)")
        print("   - manager / manager123 (Менеджер)")
        print("   - user / user123 (Пользователь)")
        
    except Exception as e:
        print(f"❌ Ошибка при создании пользователей: {e}")
        db.rollback()
    finally:
        db.close()


def create_sample_products():
    """Создает примеры товаров"""
    print("Создание примеров товаров...")
    
    db = SessionLocal()
    try:
        # Проверяем, есть ли уже товары
        if db.query(Product).count() > 0:
            print("⚠️ Товары уже существуют, пропускаем создание")
            return
        
        # Создаем примеры товаров
        sample_products = [
            {
                "name": "iPhone 15 Pro",
                "description": "Новейший смартфон Apple с титановым корпусом",
                "detailed_description": "iPhone 15 Pro оснащен чипом A17 Pro, камерой 48 МП и поддержкой USB-C",
                "quantity": 5,
                "min_stock": 2,
                "buy_price_eur": 999.00,
                "sell_price_rub": 120000.00,
                "supplier_name": "Apple Inc.",
                "availability_status": ProductStatus.IN_STOCK
            },
            {
                "name": "Samsung Galaxy S24",
                "description": "Флагманский смартфон Samsung с ИИ-функциями",
                "detailed_description": "Galaxy S24 с процессором Snapdragon 8 Gen 3 и камерой 200 МП",
                "quantity": 3,
                "min_stock": 1,
                "buy_price_eur": 899.00,
                "sell_price_rub": 95000.00,
                "supplier_name": "Samsung Electronics",
                "availability_status": ProductStatus.IN_STOCK
            },
            {
                "name": "MacBook Air M3",
                "description": "Ультратонкий ноутбук Apple с чипом M3",
                "detailed_description": "MacBook Air с 13-дюймовым дисплеем Liquid Retina и 18-часовой батареей",
                "quantity": 0,
                "min_stock": 1,
                "buy_price_eur": 1199.00,
                "sell_price_rub": 150000.00,
                "supplier_name": "Apple Inc.",
                "availability_status": ProductStatus.ON_ORDER
            }
        ]
        
        for product_data in sample_products:
            product = Product(**product_data)
            db.add(product)
        
        db.commit()
        print("✅ Примеры товаров созданы успешно")
        
    except Exception as e:
        print(f"❌ Ошибка при создании товаров: {e}")
        db.rollback()
    finally:
        db.close()


def main():
    """Основная функция инициализации"""
    print("🚀 Инициализация базы данных Sirius Group...")
    print("=" * 50)
    
    try:
        # Создаем таблицы
        create_tables()
        
        # Создаем пользователей
        create_default_users()
        
        # Создаем примеры товаров
        create_sample_products()
        
        print("=" * 50)
        print("✅ Инициализация завершена успешно!")
        print("\n📋 Следующие шаги:")
        print("1. Запустите сервер: python -m uvicorn app.main:app --host 0.0.0.0 --port 8000")
        print("2. Откройте браузер: http://localhost:8000")
        print("3. Войдите как admin / admin123")
        
    except Exception as e:
        print(f"❌ Критическая ошибка: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
