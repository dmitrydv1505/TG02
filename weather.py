import requests
from config import API_KEY

conditions_translation = {
    "clear": "ясно",
    "partly-cloudy": "малооблачно",
    # Остальные переводы погодных условий
}

def get_weather(API_KEY, lat, lon):
    params = {'lat': lat, 'lon': lon}
    url = f'https://api.weather.yandex.ru/v2/forecast?'
    headers = {'X-Yandex-API-Key': API_KEY}
    try:
        response = requests.get(url, headers=headers, params=params)

        if response.status_code == 200:
            return response.json()
        else:
            print(f"Ошибка: получен код состояния {response.status_code}")
            print(f"Ответ: {response.text}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"Ошибка соединения: {e}")
        return None

def get_weather_info(API_KEY, lat, lon):
    weather_data = get_weather(API_KEY, lat, lon)

    if weather_data:
        temp = weather_data.get('fact', {}).get('temp')
        condition = weather_data.get('fact', {}).get('condition')

        if temp is not None and condition is not None:
            condition_in_russian = conditions_translation.get(condition, "неизвестно")
            return f"Текущая температура: {temp}°C\nПогодные условия: {condition_in_russian}"
        else:
            print("Ошибка: не удалось извлечь данные о температуре или погодных условиях.")
            return "Не удалось получить данные о погоде."
    else:
        print("Ошибка: данные о погоде отсутствуют.")
        return "Не удалось получить данные о погоде."
