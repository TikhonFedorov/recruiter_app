import pytest
from unittest.mock import Mock, patch, MagicMock
from services.validators import VacancyValidator
from app.exceptions import ValidationError

class TestVacancyValidator:
    
    def test_validate_vacancy_data_success(self):
        """Тест успешной валидации"""
        data = {
            'job_title': 'Python Developer',
            'company': 'Tech Corp',
            'tasks': 'Develop web applications using Python and Flask',
            'requirements': 'Python experience, Flask knowledge',
            'conditions': 'Remote work, flexible schedule'
        }
        
        result = VacancyValidator.validate_vacancy_data(data)
        assert result == data
    
    def test_validate_vacancy_data_missing_fields(self):
        """Тест валидации с отсутствующими полями"""
        data = {'job_title': 'Python Developer'}
        
        with pytest.raises(ValidationError) as exc_info:
            VacancyValidator.validate_vacancy_data(data)
        
        assert "Отсутствуют обязательные поля" in str(exc_info.value)
    
    def test_validate_vacancy_data_empty_fields(self):
        """Тест валидации с пустыми полями"""
        data = {
            'job_title': '',
            'company': 'Tech Corp',
            'tasks': 'Develop applications',
            'requirements': 'Python experience',
            'conditions': 'Remote work'
        }
        
        with pytest.raises(ValidationError) as exc_info:
            VacancyValidator.validate_vacancy_data(data)
        
        assert "не может быть пустым" in str(exc_info.value)
    
    def test_validate_vacancy_data_too_long_fields(self):
        """Тест валидации с слишком длинными полями"""
        data = {
            'job_title': 'A' * 101,  # Превышает максимум в 100 символов
            'company': 'Tech Corp',
            'tasks': 'Develop applications',
            'requirements': 'Python experience',
            'conditions': 'Remote work'
        }
        
        with pytest.raises(ValidationError) as exc_info:
            VacancyValidator.validate_vacancy_data(data)
        
        assert "слишком длинное" in str(exc_info.value)

class TestVacancyAPI:
    
    def test_vacancy_generator_page(self, client):
        """Тест страницы генератора вакансий"""
        response = client.get('/vacancy_generator/')
        assert response.status_code == 200
    
    @patch('services.api_client.YandexGPTClient')
    def test_generate_vacancy_success(self, mock_client_class, client):
        """Тест успешной генерации вакансии"""
        # Настройка мока
        mock_client = MagicMock()
        mock_client.generate_completion.return_value = {
            "result": {"alternatives": [{"message": {"text": "Generated vacancy"}}]}
        }
        mock_client_class.return_value = mock_client
        
        data = {
            'job_title': 'Python Developer',
            'company': 'Tech Corp',
            'tasks': 'Develop web applications using Python and Flask',
            'requirements': 'Python experience, Flask knowledge',
            'conditions': 'Remote work, flexible schedule'
        }
        
        response = client.post('/vacancy_generator/generate', json=data)
        assert response.status_code == 200
        assert response.json['success'] is True
    
    def test_generate_vacancy_validation_error(self, client):
        """Тест ошибки валидации"""
        data = {
            'job_title': 'Python Developer'
            # Отсутствуют обязательные поля
        }
        
        response = client.post('/vacancy_generator/generate', json=data)
        assert response.status_code == 400
        assert response.json['success'] is False
        assert "Отсутствуют обязательные поля" in response.json['error']
    
    def test_generate_vacancy_empty_data(self, client):
        """Тест с пустыми данными"""
        response = client.post('/vacancy_generator/generate', json={})
        assert response.status_code == 400
        assert response.json['success'] is False