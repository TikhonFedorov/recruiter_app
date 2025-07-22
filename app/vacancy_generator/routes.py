
from flask import render_template, request, Blueprint, jsonify
import requests
import os
from dotenv import load_dotenv

# Загружаем переменные окружения из .env файла
load_dotenv()

vacancy_generator_bp = Blueprint('vacancy_generator', __name__)

# Получение API ключей из переменных окружения
YANDEX_API_KEY = os.getenv("YANDEX_API_KEY")
FOLDER_ID = os.getenv("YANDEX_FOLDER_ID")


@vacancy_generator_bp.route('/', methods=['GET'])
def vacancy_generator():
    return render_template('vacancy_generator.html')


@vacancy_generator_bp.route('/generate_job', methods=['POST'])
def generate_job():
    """
    Генерация вакансии с помощью Yandex GPT API
    """
    # Проверка наличия API ключей
    if not YANDEX_API_KEY or not FOLDER_ID:
        return jsonify({
            "error": "API ключи Yandex не настроены. Установите переменные окружения YANDEX_API_KEY и YANDEX_FOLDER_ID"
        }), 500

    # Получение данных из запроса
    data = request.json

    # Валидация входных данных
    required_fields = ['job_title', 'company', 'tasks', 'requirements', 'conditions']
    if not data or not all(key in data for key in required_fields):
        return jsonify({
            "error": f"Необходимы поля: {', '.join(required_fields)}"
        }), 400

    # Формирование улучшенного промпта для Yandex GPT
    prompt_text = f"""
Создай профессиональное описание вакансии на основе предоставленных данных. 
Важно: НЕ копируй текст дословно, а расширяй и улучшай его, делая более привлекательным и структурированным.

ИСХОДНЫЕ ДАННЫЕ:
Название вакансии: {data['job_title']}
Компания: {data['company']}
Задачи: {data['tasks']}
Требования: {data['requirements']}
Условия: {data['conditions']}

ТРЕБОВАНИЯ К ФОРМАТИРОВАНИЮ:
- НЕ используй символы ** для выделения
- Заголовки разделов пиши обычным текстом
- Для списков используй символ • (не дефис -)
- Пункты списков разделяй точкой с запятой ;
- Последний пункт в списке заканчивай точкой

СТРУКТУРА ВАКАНСИИ:
{data['job_title']} в {data['company']}

О компании:
[Создай краткое, но привлекательное описание компании, её миссии и направления деятельности]

Задачи и обязанности:
• [Первая задача];
• [Вторая задача];
• [Третья задача].

Требования к кандидату:
• [Первое требование];
• [Второе требование];
• [Третье требование].

Условия работы:
• [Первое условие];
• [Второе условие];
• [Третье условие].

Что мы предлагаем:
• [Первое преимущество];
• [Второе преимущество];
• [Третье преимущество].

Как присоединиться к команде:
[Добавь информацию о процессе собеседования и следующих шагах]

ПРИНЦИПЫ НАПИСАНИЯ:
- Используй активные формулировки и глаголы действия
- Добавляй конкретные примеры и достижения
- Создавай эмоциональную связь с потенциальными кандидатами
- Подчеркивай уникальные возможности и преимущества
- Делай текст динамичным и современным
- НЕ объясняй технические термины, просто используй их профессионально
- Строго соблюдай форматирование со списками через • и ;
"""

    # Формирование запроса для Yandex GPT
    request_data = {
        "modelUri": f"gpt://{FOLDER_ID}/yandexgpt-lite",
        "completionOptions": {
            "stream": False,
            "temperature": 0.7,
            "maxTokens": "1000"
        },
        "messages": [
            {
                "role": "system",
                "text": "Ты опытный HR-специалист и копирайтер, который создает привлекательные описания вакансий. Твоя задача - превращать сухие данные в живые, мотивирующие тексты, которые привлекают лучших кандидатов. Пиши профессионально, но вдохновляюще. Строго соблюдай требования к форматированию: используй • для списков, разделяй пункты через ; и НЕ используй ** для выделения."
            },
            {
                "role": "user",
                "text": prompt_text
            }
        ]
    }

    # Настройка заголовков для запроса
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Api-Key {YANDEX_API_KEY}"
    }

    # URL для Yandex GPT API
    url = "https://llm.api.cloud.yandex.net/foundationModels/v1/completion"

    try:
        # Отправка запроса к API
        response = requests.post(url, headers=headers, json=request_data)

        # Проверка статуса ответа
        if response.status_code == 200:
            return jsonify(response.json())
        else:
            return jsonify({
                "error": f"Ошибка API: {response.status_code}",
                "details": response.text
            }), response.status_code

    except requests.exceptions.RequestException as e:
        return jsonify({
            "error": f"Ошибка при выполнении запроса: {str(e)}"
        }), 500