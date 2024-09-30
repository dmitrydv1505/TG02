# В этом коде используется `api.ipify.org`,
# который возвращает ваш текущий внешний IP-адрес в формате JSON.
# Убедитесь, что библиотека `requests` установлена;

import requests

def get_external_ip():
    try:
        # Отправляем запрос на сервис, который возвращает ваш внешний IP
        response = requests.get('https://api.ipify.org?format=json')
        # Проверяем, успешен ли запрос
        if response.status_code == 200:
            # Извлекаем IP-адрес из ответа
            ip_address = response.json().get('ip')
            return ip_address
        else:
            return "Не удалось получить IP-адрес: ошибка запроса"
    except requests.RequestException as e:
        return f"Произошла ошибка при попытке получить IP-адрес: {e}"

# Пример использования функции
# external_ip = get_external_ip()
# print(f"Ваш внешний IP-адрес: {external_ip}")

