import requests
import logging
from typing import Dict, Any, Optional
from flask import current_app
from app.exceptions import APIError, ConfigurationError

logger = logging.getLogger(__name__)

class YandexGPTClient:
    """Клиент для работы с Yandex GPT API"""
    
    def __init__(self):
        self.api_key = current_app.config.get('YANDEX_API_KEY')
        self.folder_id = current_app.config.get('YANDEX_FOLDER_ID')
        self.base_url = "https://llm.api.cloud.yandex.net/foundationModels/v1"
        self.timeout = current_app.config.get('REQUEST_TIMEOUT', 30)
        
        if not self.api_key or not self.folder_id:
            raise ConfigurationError("Yandex API credentials not configured")
    
    def generate_completion(self, prompt: str, system_prompt: str = None, 
                          temperature: float = 0.7, max_tokens: int = 1000) -> Dict[str, Any]:
        """
        Генерация текста с помощью Yandex GPT
        
        Args:
            prompt: Пользовательский промпт
            system_prompt: Системный промпт (опционально)
            temperature: Температура генерации (0.0-1.0)
            max_tokens: Максимальное количество токенов
            
        Returns:
            Ответ от API
            
        Raises:
            APIError: При ошибке API
        """
        messages = []
        
        if system_prompt:
            messages.append({
                "role": "system",
                "text": system_prompt
            })
        
        messages.append({
            "role": "user",
            "text": prompt
        })
        
        request_data = {
            "modelUri": f"gpt://{self.folder_id}/yandexgpt-lite",
            "completionOptions": {
                "stream": False,
                "temperature": temperature,
                "maxTokens": str(max_tokens)
            },
            "messages": messages
        }
        
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Api-Key {self.api_key}"
        }
        
        try:
            logger.debug(f"Sending request to Yandex GPT API with prompt length: {len(prompt)}")
            
            response = requests.post(
                f"{self.base_url}/completion",
                headers=headers,
                json=request_data,
                timeout=self.timeout
            )
            
            if response.status_code == 200:
                logger.info("Successful API call to Yandex GPT")
                return response.json()
            else:
                error_msg = f"API returned status {response.status_code}: {response.text}"
                logger.error(error_msg)
                raise APIError(error_msg, response.status_code)
                
        except requests.exceptions.Timeout:
            logger.error("Request timeout")
            raise APIError("Request timeout", 504)
        except requests.exceptions.ConnectionError:
            logger.error("Connection error")
            raise APIError("Connection error", 503)
        except requests.exceptions.RequestException as e:
            logger.error(f"Request failed: {str(e)}")
            raise APIError(f"Request failed: {str(e)}", 500)