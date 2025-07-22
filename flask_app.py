from flask import Flask, render_template, jsonify
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import logging
import os
from config.settings import config_map
from app.exceptions import BaseAppException

# Создаём Limiter один раз, без передачи app
limiter = Limiter(
    key_func=get_remote_address,
    default_limits=[]
)

def create_app(config_name=None):
    """Фабрика приложений Flask"""

    if config_name is None:
        config_name = os.getenv('FLASK_ENV', 'development')

    app = Flask(__name__)

    # Загрузка конфигурации
    config_class = config_map.get(config_name, config_map['default'])
    app.config.from_object(config_class)

    # Валидация конфигурации
    try:
        config_class.validate()
    except ValueError as e:
        if not app.config.get('TESTING', False):
            app.logger.error(f"Configuration error: {e}")
            raise

    # Настройка логирования
    setup_logging(app)

    # Настройка rate limiting
    limiter.default_limits = app.config['RATELIMIT_DEFAULT'].split(';')
    limiter.init_app(app)

    # Регистрация blueprints
    register_blueprints(app)

    # Регистрация обработчиков ошибок
    register_error_handlers(app)

    # Основные маршруты
    @app.route('/')
    def index():
        return render_template('index.html')

    @app.route('/health')
    def health_check():
        """Проверка здоровья приложения"""
        return jsonify({"status": "healthy", "version": "1.0.0"})

    return app

def setup_logging(app):
    """Настройка логирования"""
    if app.config.get('TESTING', False):
        return

    log_level = getattr(logging, app.config.get('LOG_LEVEL', 'INFO'))
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    console_handler.setLevel(log_level)

    if not app.config.get('DEBUG', False):
        file_handler = logging.FileHandler(app.config.get('LOG_FILE', 'app.log'))
        file_handler.setFormatter(formatter)
        file_handler.setLevel(log_level)
        app.logger.addHandler(file_handler)

    app.logger.addHandler(console_handler)
    app.logger.setLevel(log_level)

def register_blueprints(app):
    """Регистрация blueprints"""
    from app.salary_calculator.routes import salary_calculator_bp
    from app.vacancy_generator.routes import vacancy_generator_bp

    app.register_blueprint(salary_calculator_bp, url_prefix='/salary_calculator')
    app.register_blueprint(vacancy_generator_bp, url_prefix='/vacancy_generator')

    if not app.config.get('TESTING', False):
        app.logger.info("Registered routes:")
        for rule in app.url_map.iter_rules():
            app.logger.info(f"  {rule.rule} -> {rule.endpoint}")

def register_error_handlers(app):
    """Регистрация обработчиков ошибок"""

    @app.errorhandler(BaseAppException)
    def handle_app_exception(e):
        if not app.config.get('TESTING', False):
            app.logger.error(f"App exception: {e.message}")
        return jsonify({"error": e.message}), e.status_code

    @app.errorhandler(404)
    def page_not_found(e):
        if not app.config.get('TESTING', False):
            app.logger.warning(f"404 error: {e}")
        return render_template('404.html'), 404

    @app.errorhandler(500)
    def internal_server_error(e):
        if not app.config.get('TESTING', False):
            app.logger.error(f"Internal server error: {str(e)}")
        return render_template('500.html'), 500

    @app.errorhandler(429)
    def rate_limit_exceeded(e):
        if not app.config.get('TESTING', False):
            app.logger.warning(f"Rate limit exceeded: {e}")
        return jsonify({"error": "Превышен лимит запросов"}), 429

    @app.errorhandler(400)
    def bad_request(e):
        if not app.config.get('TESTING', False):
            app.logger.warning(f"Bad request: {e}")
        return jsonify({"error": "Неверный запрос"}), 400

if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=5000, debug=app.config['DEBUG'])