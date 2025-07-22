from typing import Dict, List, Optional
import re
from app.exceptions import ValidationError

class VacancyValidator:
    """Валидатор для данных вакансии"""
    
    REQUIRED_FIELDS = ['job_title', 'company', 'tasks', 'requirements', 'conditions']
    
    # Максимальные длины полей
    MAX_LENGTHS = {
        'job_title': 100,
        'company': 100,
        'tasks': 1000,
        'requirements': 1000,
        'conditions': 1000
    }
    
    # Минимальные длины полей
    MIN_LENGTHS = {
        'job_title': 3,
        'company': 2,
        'tasks': 10,
        'requirements': 10,
        'conditions': 10
    }
    
    @classmethod
    def validate_vacancy_data(cls, data: Dict) -> Dict:
        """
        Валидация данных вакансии
        
        Args:
            data: Словарь с данными вакансии
            
        Returns:
            Очищенные данные
            
        Raises:
            ValidationError: При ошибке валидации
        """
        if not data:
            raise ValidationError("Данные не предоставлены")
        
        # Проверка обязательных полей
        cls._validate_required_fields(data)
        
        # Проверка на пустые значения и длину
        cls._validate_field_lengths(data)
        
        # Очистка данных
        cleaned_data = cls._clean_data(data)
        
        return cleaned_data
    
    @classmethod
    def _validate_required_fields(cls, data: Dict) -> None:
        """Проверка наличия обязательных полей"""
        missing_fields = [field for field in cls.REQUIRED_FIELDS if field not in data]
        if missing_fields:
            raise ValidationError(f"Отсутствуют обязательные поля: {', '.join(missing_fields)}")
    
    @classmethod
    def _validate_field_lengths(cls, data: Dict) -> None:
        """Проверка длины полей"""
        for field in cls.REQUIRED_FIELDS:
            value = data.get(field, '').strip()
            
            if not value:
                raise ValidationError(f"Поле '{field}' не может быть пустым")
            
            # Проверка минимальной длины
            min_length = cls.MIN_LENGTHS.get(field, 1)
            if len(value) < min_length:
                raise ValidationError(f"Поле '{field}' слишком короткое (минимум {min_length} символов)")
            
            # Проверка максимальной длины
            max_length = cls.MAX_LENGTHS.get(field, 1000)
            if len(value) > max_length:
                raise ValidationError(f"Поле '{field}' слишком длинное (максимум {max_length} символов)")
    
    @classmethod
    def _clean_data(cls, data: Dict) -> Dict:
        """Очистка данных от лишних пробелов"""
        cleaned = {}
        for field in cls.REQUIRED_FIELDS:
            cleaned[field] = data[field].strip()
        return cleaned

class SalaryValidator:
    """Валидатор для данных калькулятора зарплаты"""
    
    @classmethod
    def validate_salary_data(cls, data: Dict) -> Dict:
        """
        Валидация данных для расчета зарплаты
        
        Args:
            data: Словарь с данными для расчета
            
        Returns:
            Очищенные данные
            
        Raises:
            ValidationError: При ошибке валидации
        """
        if not data:
            raise ValidationError("Данные не предоставлены")
        
        # Базовая валидация - можно расширить в зависимости от требований
        required_fields = ['base_salary']
        
        missing_fields = [field for field in required_fields if field not in data]
        if missing_fields:
            raise ValidationError(f"Отсутствуют обязательные поля: {', '.join(missing_fields)}")
        
        # Валидация числовых значений
        if 'base_salary' in data:
            try:
                salary = float(data['base_salary'])
                if salary < 0:
                    raise ValidationError("Базовая зарплата не может быть отрицательной")
                if salary > 10000000:
                    raise ValidationError("Базовая зарплата слишком большая")
            except (ValueError, TypeError):
                raise ValidationError("Базовая зарплата должна быть числом")
        
        return data