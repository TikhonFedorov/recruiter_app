import pytest
import os
import sys

# Добавляем корневую директорию в путь
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app

@pytest.fixture
def app():
    """Создание тестового приложения"""
    app = create_app('testing')
    return app

@pytest.fixture
def client(app):
    """Тестовый клиент"""
    return app.test_client()

@pytest.fixture
def runner(app):
    """Тестовый runner для CLI команд"""
    return app.test_cli_runner()