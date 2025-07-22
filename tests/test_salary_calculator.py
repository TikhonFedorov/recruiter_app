import pytest
from unittest.mock import Mock, patch
from services.validators import SalaryValidator
from app.exceptions import ValidationError

class TestSalaryValidator:
    
    def test_validate_salary_data_success(self):
        """Тест успешной валидации"""
        data = {
            'base_salary': 100000
        }
        
        result = SalaryValidator.validate_salary_data(data)
        assert result == data
    
    def test_validate_salary_data_missing_fields(self):
        """Тест валидации с отсутствующими полями"""
        data = {}
        
        with pytest.raises(ValidationError) as exc_info:
            SalaryValidator.validate_salary_data(data)
        
        assert "Отсутствуют обязательные поля" in str(exc_info.value)
    
    def test_validate_salary_data_negative_salary(self):
        """Тест валидации с отрицательной зарплатой"""
        data = {
            'base_salary': -50000
        }
        
        with pytest.raises(ValidationError) as exc_info:
            SalaryValidator.validate_salary_data(data)
        
        assert "не может быть отрицательной" in str(exc_info.value)
    
    def test_validate_salary_data_invalid_type(self):
        """Тест валидации с неверным типом данных"""
        data = {
            'base_salary': 'not_a_number'
        }
        
        with pytest.raises(ValidationError) as exc_info:
            SalaryValidator.validate_salary_data(data)
        
        assert "должна быть числом" in str(exc_info.value)

class TestSalaryAPI:
    
    def test_salary_calculator_page(self, client):
        """Тест страницы калькулятора зарплаты"""
        response = client.get('/salary_calculator/')
        assert response.status_code == 200
    
    def test_calculate_salary_success(self, client):
        """Тест успешного расчета зарплаты"""
        data = {
            'base_salary': 100000
        }
        
        response = client.post('/salary_calculator/calculate', json=data)
        assert response.status_code == 200
        assert response.json['success'] is True
    
    def test_calculate_salary_validation_error(self, client):
        """Тест ошибки валидации"""
        data = {}
        
        response = client.post('/salary_calculator/calculate', json=data)
        assert response.status_code == 400
        assert response.json['success'] is False
        assert "Отсутствуют обязательные поля" in response.json['error']