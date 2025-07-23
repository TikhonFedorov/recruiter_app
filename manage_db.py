#!/usr/bin/env python3
"""
Скрипт для управления базой данных
"""

import os
import sys
from flask_app import create_app
from app.models import db
from app.models import User

def init_db():
    """Инициализация базы данных"""
    app = create_app('development')
    with app.app_context():
        print("Создание таблиц...")
        db.create_all()
        print("✅ Таблицы созданы успешно!")

def drop_db():
    """Удаление всех таблиц"""
    app = create_app('development')
    with app.app_context():
        print("⚠️  Удаление всех таблиц...")
        db.drop_all()
        print("✅ Таблицы удалены!")

def reset_db():
    """Пересоздание базы данных"""
    print("Пересоздание базы данных...")
    drop_db()
    init_db()

def list_users():
    """Список всех пользователей"""
    app = create_app('development')
    with app.app_context():
        users = User.query.all()
        if not users:
            print("👥 Пользователей не найдено")
            return
        
        print(f"👥 Найдено пользователей: {len(users)}")
        print("-" * 80)
        for user in users:
            print(f"ID: {user.id}")
            print(f"Имя: {user.name}")
            print(f"Email: {user.email}")
            print(f"Компания: {user.company or 'Не указана'}")
            print(f"Должность: {user.position or 'Не указана'}")
            print(f"Создан: {user.created_at}")
            print(f"Последний вход: {user.last_login or 'Никогда'}")
            print("-" * 80)

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Использование:")
        print("  python manage_db.py init     - создать таблицы")
        print("  python manage_db.py drop     - удалить таблицы") 
        print("  python manage_db.py reset    - пересоздать БД")
        print("  python manage_db.py users    - показать пользователей")
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == 'init':
        init_db()
    elif command == 'drop':
        confirm = input("Вы уверены? Все данные будут удалены! (yes/no): ")
        if confirm.lower() == 'yes':
            drop_db()
    elif command == 'reset':
        confirm = input("Пересоздать БД? Все данные будут потеряны! (yes/no): ")
        if confirm.lower() == 'yes':
            reset_db()
    elif command == 'users':
        list_users()
    else:
        print(f"❌ Неизвестная команда: {command}")
