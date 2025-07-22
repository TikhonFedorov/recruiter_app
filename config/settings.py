import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    """Базовая конфигурация"""
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'

    # API Configuration
    YANDEX_API_KEY = os.getenv('YANDEX_API_KEY')
    YANDEX_FOLDER_ID = os.getenv('YANDEX_FOLDER_ID')

    # Rate limiting
    RATELIMIT_STORAGE_URL = os.getenv('REDIS_URL', 'memory://')
    RATELIMIT_DEFAULT = "200 per day;50 per hour"

    # Logging
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    LOG_FILE = os.getenv('LOG_FILE', 'app.log')

    # Request timeout
    REQUEST_TIMEOUT = int(os.getenv('REQUEST_TIMEOUT', '30'))

    @classmethod
    def validate(cls):
        """Валидация критически важных настроек"""
        required_vars = ['YANDEX_API_KEY', 'YANDEX_FOLDER_ID']
        missing = [var for var in required_vars if not getattr(cls, var)]
        if missing:
            raise ValueError(f"Отсутствуют переменные окружения: {', '.join(missing)}")


class DevelopmentConfig(Config):
    """Конфигурация для разработки"""
    DEBUG = True
    LOG_LEVEL = 'DEBUG'


class ProductionConfig(Config):
    """Конфигурация для продакшена"""
    DEBUG = False
    LOG_LEVEL = 'WARNING'


class TestingConfig(Config):
    """Конфигурация для тестирования"""
    TESTING = True
    WTF_CSRF_ENABLED = False
    YANDEX_API_KEY = 'test-api-key'
    YANDEX_FOLDER_ID = 'test-folder-id'


config_map = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}