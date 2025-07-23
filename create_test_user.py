#!/usr/bin/env python3
"""
Скрипт для создания тестового пользователя
"""

from flask_app import create_app, db
from app.models import User

def create_test_user():
    """Создание тестового пользователя для разработки"""
    
    app = create_app('development')
    
    with app.app_context():
        # Создаем таблицы если их нет
        db.create_all()
        
        # Проверяем, существует ли уже тестовый пользователь
        existing_user = User.query.filter_by(email='admin@recruiter.com').first()
        if existing_user:
            print("❌ Тестовый пользователь уже существует!")
            print(f"Email: {existing_user.email}")
            print(f"Имя: {existing_user.name}")
            return
        
        # Создаем тестового пользователя
        test_user = User(
            name='HR Администратор',
            email='admin@recruiter.com',
            company='ТехКорп',
            position='Senior HR Manager',
            phone='+7 (999) 123-45-67'
        )
        test_user.set_password('admin123')
        
        try:
            db.session.add(test_user)
            db.session.commit()
            print("✅ Тестовый пользователь создан успешно!")
            print(f"Email: {test_user.email}")
            print(f"Пароль: admin123")
            print(f"Имя: {test_user.name}")
            print(f"Компания: {test_user.company}")
        except Exception as e:
            db.session.rollback()
            print(f"❌ Ошибка при создании пользователя: {e}")

def create_additional_test_users():
    """Создание дополнительных тестовых пользователей"""
    
    app = create_app('development')
    
    with app.app_context():
        test_users = [
            {
                'name': 'Анна Иванова',
                'email': 'anna@recruiter.com',
                'password': 'recruiter123',
                'company': 'IT Solutions',
                'position': 'Recruiter',
                'phone': '+7 (999) 234-56-78'
            },
            {
                'name': 'Петр Сидоров',
                'email': 'petr@recruiter.com',
                'password': 'hr123456',
                'company': 'StartupHub',
                'position': 'HR Business Partner',
                'phone': '+7 (999) 345-67-89'
            }
        ]
        
        for user_data in test_users:
            existing = User.query.filter_by(email=user_data['email']).first()
            if not existing:
                user = User(
                    name=user_data['name'],
                    email=user_data['email'],
                    company=user_data['company'],
                    position=user_data['position'],
                    phone=user_data['phone']
                )
                user.set_password(user_data['password'])
                db.session.add(user)
                print(f"✅ Создан пользователь: {user_data['email']}")
            else:
                print(f"⚠️  Пользователь {user_data['email']} уже существует")
        
        try:
            db.session.commit()
            print("✅ Все пользователи созданы успешно!")
        except Exception as e:
            db.session.rollback()
            print(f"❌ Ошибка: {e}")

if __name__ == '__main__':
    print("Создание тестовых пользователей...")
    create_test_user()
    print("\nСоздание дополнительных пользователей...")
    create_additional_test_users()
    
    print("\n" + "="*50)
    print("ДАННЫЕ ДЛЯ ВХОДА:")
    print("="*50)
    print("1. admin@recruiter.com / admin123")
    print("2. anna@recruiter.com / recruiter123") 
    print("3. petr@recruiter.com / hr123456")
    print("="*50)
