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
        "total_snos": len(CONFIG.get("history", [])),
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
    print("☢️ CYBERTEAM SNOSER v18.0 - ULTRA BOT ☢️")
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
    "current_target_type": "account",
    "current_reason": "spam",
    "history": [],
    "last_update_id": 0,
    "awaiting_target": False,
    "awaiting_repeats": False,
    "temp_target": "",
    "temp_type": "account"
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
                ],
                "phishing": [
                    f"Аккаунт {target} - ФИШИНГОВЫЙ! Крадет данные банковских карт!",
                    f"{target} рассылает фишинговые ссылки! Это угроза безопасности!"
                ],
                "doxxing": [
                    f"Аккаунт {target} занимается ДОКСИНГОМ! Сливает личные данные людей!",
                    f"{target} публикует паспортные данные, адреса и номера телефонов!"
                ],
                "terror": [
                    f"Аккаунт {target} призывает к ТЕРРОРИЗМУ! Статья 205.2 УК РФ!",
                    f"{target} - ТЕРРОРИСТИЧЕСКИЙ аккаунт! Публикует инструкции по взрывчатке!"
                ],
                "drugs": [
                    f"Аккаунт {target} продает НАРКОТИКИ! Статья 228.1 УК РФ!",
                    f"{target} - НАРКО-ДИЛЕР! Торгует запрещенными веществами!"
                ],
                "child_porn": [
                    f"Аккаунт {target} распространяет ДЕТСКУЮ ПОРНОГРАФИЮ! Статья 242.1 УК РФ!",
                    f"{target} - ПЕДОФИЛ! Торгует фото и видео с детьми!"
                ],
                "violence": [
                    f"Аккаунт {target} призывает к НАСИЛИЮ! Статья 119 УК РФ!",
                    f"{target} - АГРЕССОР! Призывает к избиению людей!"
                ],
                "hate": [
                    f"Аккаунт {target} РАЗЖИГАЕТ НЕНАВИСТЬ! Статья 282 УК РФ!",
                    f"{target} - НАЦИСТ! Публикует расистские посты!"
                ],
                "harassment": [
                    f"Аккаунт {target} - ДОМОГАТЕЛЬ! Преследует людей в чатах!",
                    f"{target} - СТАЛКЕР! Следит за людьми и пишет угрозы!"
                ],
                "impersonation": [
                    f"Аккаунт {target} - ПОДДЕЛЬНЫЙ! Выдает себя за известную личность!",
                    f"{target} - ФЕЙК! Притворяется сотрудником Telegram!"
                ],
                "bot": [
                    f"Аккаунт {target} - НЕЛЕГАЛЬНЫЙ БОТ! Нарушает правила Telegram!",
                    f"{target} - БОТ-СПАМЕР! Отправляет тысячи сообщений!"
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
        success = 0
        failed = 0
        lock = threading.Lock()
        total = repeats
        
        print(f"🎯 ЦЕЛЬ: {target}")
        print(f"📋 ТИП: {target_type.upper()}")
        print(f"🔥 ПРИЧИНА: {reason.upper()}")
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
            'reason': reason,
            'success': success,
            'total': total,
            'destroyed': is_destroyed,
            'time': datetime.now().strftime('%H:%M')
        })
        if len(CONFIG['history']) > 20:
            CONFIG['history'] = CONFIG['history'][-20:]
        
        return is_destroyed

# ===================================================================
# ОТПРАВКА СООБЩЕНИЙ В TELEGRAM
# ===================================================================
def send_telegram_message(text, keyboard=None):
    try:
        url = f"https://api.telegram.org/bot{CONFIG['bot_token']}/sendMessage"
        data = {
            "chat_id": CONFIG['owner_id'],
            "text": text,
            "parse_mode": "HTML",
            "disable_web_page_preview": True
        }
        if keyboard:
            data["reply_markup"] = json.dumps({"inline_keyboard": keyboard})
        requests.post(url, data=data, timeout=5)
    except:
        pass

# ===================================================================
# КЛАВИАТУРЫ БОТА
# ===================================================================
def main_menu():
    keyboard = [
        [
            {"text": "📱 СНОС АККАУНТА", "callback_data": "type_account"},
            {"text": "📢 СНОС КАНАЛА", "callback_data": "type_channel"}
        ],
        [
            {"text": "🤖 СНОС БОТА", "callback_data": "type_bot"},
            {"text": "👥 СНОС ГРУППЫ", "callback_data": "type_group"}
        ],
        [
            {"text": "📊 СТАТИСТИКА", "callback_data": "stats"},
            {"text": "📜 ИСТОРИЯ", "callback_data": "history"}
        ],
        [
            {"text": "⚙️ НАСТРОЙКИ", "callback_data": "settings"},
            {"text": "🛑 СТОП", "callback_data": "stop"}
        ],
        [
            {"text": "🌐 ГЛОБАЛЬНЫЙ РЕЙД", "callback_data": "global_raid"},
            {"text": "🔍 НАЙТИ ЦЕЛЬ", "callback_data": "find_target"}
        ]
    ]
    return keyboard

def reason_menu(target_type, target):
    reasons = {
        "account": [
            ("💀 Спам", "spam"),
            ("😡 Оскорбление", "insult"),
            ("💰 Мошенничество", "scam"),
            ("🚫 Нелегальный контент", "illegal"),
            ("🎭 Виртуальный номер", "fake"),
            ("🎣 Фишинг", "phishing"),
            ("🔓 Доксинг", "doxxing"),
            ("💣 Терроризм", "terror"),
            ("💊 Наркотики", "drugs"),
            ("🔞 Детское порно", "child_porn"),
            ("⚔️ Насилие", "violence"),
            ("👿 Ненависть", "hate"),
            ("🕵️ Преследование", "harassment"),
            ("🎭 Самозванство", "impersonation"),
            ("🤖 Нелегальный бот", "bot")
        ],
        "channel": [
            ("🔞 Порнография", "porn"),
            ("💊 Наркотики", "drugs"),
            ("💣 Терроризм", "terror"),
            ("⚔️ Ненависть", "hate"),
            ("💰 Мошенничество", "scam"),
            ("🔓 Доксинг", "doxxing"),
            ("👶 Детское порно", "child_porn"),
            ("⚔️ Насилие", "violence"),
            ("🚫 Нелегальный контент", "illegal"),
            ("📨 Спам", "spam"),
            ("🎣 Фишинг", "phishing"),
            ("🎭 Самозванство", "impersonation"),
            ("🕵️ Преследование", "harassment"),
            ("☢️ Радикализм", "radical"),
            ("📰 Фейк-новости", "fake_news")
        ],
        "bot": [
            ("📨 Спам-бот", "spam"),
            ("💰 Мошенничество", "scam"),
            ("🎣 Фишинг", "phishing"),
            ("🚫 Нелегальный контент", "illegal"),
            ("💊 Наркотики", "drugs"),
            ("👶 Детское порно", "child_porn"),
            ("⚔️ Насилие", "violence"),
            ("👿 Ненависть", "hate"),
            ("🔓 Доксинг", "doxxing"),
            ("🕵️ Преследование", "harassment"),
            ("🎭 Самозванство", "impersonation"),
            ("📰 Фейк-новости", "fake_news"),
            ("☢️ Радикализм", "radical"),
            ("💣 Терроризм", "terror"),
            ("💾 Кража данных", "data_theft")
        ],
        "group": [
            ("📨 Спам", "spam"),
            ("👿 Ненависть", "hate"),
            ("💰 Мошенничество", "scam"),
            ("🚫 Нелегальный контент", "illegal"),
            ("💊 Наркотики", "drugs"),
            ("👶 Детское порно", "child_porn"),
            ("⚔️ Насилие", "violence"),
            ("💣 Терроризм", "terror"),
            ("🔓 Доксинг", "doxxing"),
            ("🕵️ Преследование", "harassment"),
            ("☢️ Радикализм", "radical"),
            ("📰 Фейк-новости", "fake_news"),
            ("🎭 Самозванство", "impersonation"),
            ("🎣 Фишинг", "phishing"),
            ("🔞 Порнография", "porn")
        ]
    }
    
    keyboard = []
    for label, value in reasons.get(target_type, reasons["account"]):
        keyboard.append([{"text": label, "callback_data": f"reason_{target_type}_{value}_{target}"}])
    keyboard.append([{"text": "⬅️ НАЗАД", "callback_data": "back"}])
    return keyboard

def repeats_menu(target_type, reason, target):
    keyboard = [
        [{"text": "💥 100", "callback_data": f"run_{target_type}_{reason}_{target}_100"}],
        [{"text": "💥 500", "callback_data": f"run_{target_type}_{reason}_{target}_500"}],
        [{"text": "💥 1000", "callback_data": f"run_{target_type}_{reason}_{target}_1000"}],
        [{"text": "💥 3000", "callback_data": f"run_{target_type}_{reason}_{target}_3000"}],
        [{"text": "💥 5000", "callback_data": f"run_{target_type}_{reason}_{target}_5000"}],
        [{"text": "⬅️ НАЗАД", "callback_data": f"back_reason_{target_type}_{target}"}]
    ]
    return keyboard

def settings_menu():
    keyboard = [
        [{"text": f"⚡ РЕЖИМ: {CONFIG['mode'].upper()}", "callback_data": "toggle_mode"}],
        [{"text": f"🌊 ПОТОКИ: {CONFIG['threads']}", "callback_data": "toggle_threads"}],
        [{"text": f"⏱️ ЗАДЕРЖКА: {CONFIG['delay_min']}-{CONFIG['delay_max']}с", "callback_data": "toggle_delay"}],
        [{"text": "⬅️ НАЗАД", "callback_data": "back"}]
    ]
    return keyboard

# ===================================================================
# ОБРАБОТЧИК КОМАНД
# ===================================================================
def process_callback(callback_data):
    parts = callback_data.split('_')
    
    if callback_data == "back":
        send_telegram_message("☢️ <b>ГЛАВНОЕ МЕНЮ</b>\n\nВыбери действие:", main_menu())
        return
    
    if callback_data.startswith("back_reason_"):
        _, _, target_type, target = callback_data.split('_', 3)
        msg = f"🎯 <b>ВЫБЕРИ ПРИЧИНУ</b>\n\n👤 ЦЕЛЬ: {target}\n📋 ТИП: {target_type.upper()}"
        send_telegram_message(msg, reason_menu(target_type, target))
        return
    
    if callback_data == "stats":
        total = len(CONFIG['history'])
        destroyed = sum(1 for h in CONFIG['history'] if h.get('destroyed', False))
        success_rate = int((destroyed / total) * 100) if total > 0 else 0
        
        msg = f"""
📊 <b>СТАТИСТИКА СНОСЕРА</b>

📨 ВСЕГО СНОСОВ: {total}
💀 УНИЧТОЖЕНО: {destroyed}
🎯 УСПЕШНОСТЬ: {success_rate}%
⚡ РЕЖИМ: {CONFIG['mode'].upper()}
🌊 ПОТОКОВ: {CONFIG['threads']}
⏱️ ЗАДЕРЖКА: {CONFIG['delay_min']}-{CONFIG['delay_max']}с
        """
        keyboard = [[{"text": "🔄 ОБНОВИТЬ", "callback_data": "stats"}]]
        send_telegram_message(msg, keyboard)
        return
    
    if callback_data == "history":
        if not CONFIG['history']:
            send_telegram_message("📜 <b>ИСТОРИЯ ПУСТА</b>\n\nПока не было сносов.")
            return
        
        msg = "📜 <b>ПОСЛЕДНИЕ 20 СНОСОВ</b>\n\n"
        for i, h in enumerate(reversed(CONFIG['history']), 1):
            status = "✅ УНИЧТОЖЕН" if h.get('destroyed', False) else "❌ ВЫЖИЛ"
            msg += f"{i}. {h['target']} — {h['success']}/{h['total']} ({status}) [{h['time']}]\n"
        
        keyboard = [[{"text": "🔄 ОБНОВИТЬ", "callback_data": "history"}]]
        send_telegram_message(msg, keyboard)
        return
    
    if callback_data == "settings":
        send_telegram_message("⚙️ <b>НАСТРОЙКИ</b>\n\nНажми для изменения:", settings_menu())
        return
    
    if callback_data == "stop":
        if CONFIG['attack_running']:
            CONFIG['attack_running'] = False
            msg = "🛑 <b>СНОС ОСТАНОВЛЕН!</b>"
        else:
            msg = "ℹ️ СНОС НЕ ЗАПУЩЕН"
        send_telegram_message(msg)
        return
    
    if callback_data == "toggle_mode":
        modes = ["normal", "spam", "tornado"]
        current = CONFIG['mode']
        next_mode = modes[(modes.index(current) + 1) % len(modes)]
        CONFIG['mode'] = next_mode
        send_telegram_message(f"✅ РЕЖИМ ИЗМЕНЕН: {next_mode.upper()}", settings_menu())
        return
    
    if callback_data == "toggle_threads":
        options = [50, 100, 150, 200, 300, 500]
        current = CONFIG['threads']
        next_idx = (options.index(current) + 1) % len(options) if current in options else 0
        CONFIG['threads'] = options[next_idx]
        send_telegram_message(f"✅ ПОТОКОВ: {CONFIG['threads']}", settings_menu())
        return
    
    if callback_data == "toggle_delay":
        delays = [(0.05, 0.15), (0.1, 0.3), (0.2, 0.5), (0.5, 1.0)]
        current = (CONFIG['delay_min'], CONFIG['delay_max'])
        next_idx = (delays.index(current) + 1) % len(delays) if current in delays else 0
        CONFIG['delay_min'], CONFIG['delay_max'] = delays[next_idx]
        send_telegram_message(f"✅ ЗАДЕРЖКА: {CONFIG['delay_min']}-{CONFIG['delay_max']}с", settings_menu())
        return
    
    if callback_data == "global_raid":
        msg = """
🌐 <b>ГЛОБАЛЬНЫЙ РЕЙД</b>

Автоматический поиск и снос целей по ключевым словам.

<b>ВВЕДИ КЛЮЧЕВЫЕ СЛОВА</b>
(через запятую, например: спам, мошенник, наркотики)
"""
        send_telegram_message(msg)
        CONFIG['awaiting_target'] = True
        CONFIG['temp_type'] = "global_raid"
        return
    
    if callback_data == "find_target":
        msg = """
🔍 <b>ПОИСК ЦЕЛИ</b>

Введи ключевое слово для поиска каналов/аккаунтов.
Например: крипта, мошенник, порно
"""
        send_telegram_message(msg)
        CONFIG['awaiting_target'] = True
        CONFIG['temp_type'] = "find_target"
        return
    
    if callback_data.startswith("type_"):
        target_type = callback_data.split('_')[1]
        CONFIG['temp_type'] = target_type
        msg = f"🎯 <b>ВВЕДИ @USERNAME ИЛИ ССЫЛКУ</b>\n\n📋 ТИП: {target_type.upper()}"
        send_telegram_message(msg)
        CONFIG['awaiting_target'] = True
        return
    
    if callback_data.startswith("reason_"):
        parts = callback_data.split('_')
        target_type = parts[1]
        reason = parts[2]
        target = '_'.join(parts[3:])
        
        msg = f"""
🎯 <b>ВЫБЕРИ КОЛИЧЕСТВО ЖАЛОБ</b>

👤 ЦЕЛЬ: {target}
📋 ТИП: {target_type.upper()}
🔥 ПРИЧИНА: {reason.upper()}
        """
        send_telegram_message(msg, repeats_menu(target_type, reason, target))
        return
    
    if callback_data.startswith("run_"):
        parts = callback_data.split('_')
        target_type = parts[1]
        reason = parts[2]
        target = '_'.join(parts[3:-1])
        repeats = int(parts[-1])
        
        if CONFIG['attack_running']:
            send_telegram_message("⚠️ СНОС УЖЕ ИДЕТ! Дождись завершения.")
            return
        
        CONFIG['attack_running'] = True
        CONFIG['current_target'] = target
        
        msg = f"""
🎯 <b>СНОС ЗАПУЩЕН!</b>

👤 ЦЕЛЬ: {target}
📋 ТИП: {target_type.upper()}
🔥 ПРИЧИНА: {reason.upper()}
💥 ЖАЛОБ: {repeats}
🌊 ПОТОКОВ: {CONFIG['threads']}
        """
        send_telegram_message(msg)
        
        def run():
            SnosEngine.snos_target(target, target_type, reason, repeats, "")
        
        thread = threading.Thread(target=run, daemon=True)
        thread.start()
        return

# ===================================================================
# ОБРАБОТЧИК ТЕКСТОВЫХ СООБЩЕНИЙ
# ===================================================================
def process_text(text):
    text = text.strip()
    
    if CONFIG['awaiting_target']:
        CONFIG['awaiting_target'] = False
        temp_type = CONFIG['temp_type']
        
        if temp_type == "global_raid":
            keywords = [k.strip() for k in text.split(',')]
            msg = f"🌐 <b>ГЛОБАЛЬНЫЙ РЕЙД ЗАПУЩЕН!</b>\n\n🔍 КЛЮЧЕВЫЕ СЛОВА: {', '.join(keywords)}"
            send_telegram_message(msg)
            # Запускаем поиск и снос
            return
        
        if temp_type == "find_target":
            msg = f"🔍 <b>ПОИСК ПО КЛЮЧУ: {text}</b>\n\n⏳ ИЩУ ЦЕЛИ..."
            send_telegram_message(msg)
            # Здесь можно добавить логику поиска
            return
        
        # Обычный выбор типа
        target_type = temp_type
        msg = f"🎯 <b>ВЫБЕРИ ПРИЧИНУ</b>\n\n👤 ЦЕЛЬ: {text}\n📋 ТИП: {target_type.upper()}"
        send_telegram_message(msg, reason_menu(target_type, text))
        return
    
    # Обработка команд
    if text.startswith('/start'):
        send_telegram_message("☢️ <b>CYBERTEAM SNOSER</b>\n\nВыбери действие:", main_menu())
        return
    
    if text.startswith('/snos'):
        parts = text.split()
        if len(parts) >= 3:
            target = parts[1]
            try:
                repeats = int(parts[2])
                if CONFIG['attack_running']:
                    send_telegram_message("⚠️ СНОС УЖЕ ИДЕТ!")
                    return
                CONFIG['attack_running'] = True
                CONFIG['current_target'] = target
                send_telegram_message(f"🎯 СНОС ЗАПУЩЕН!\n\n👤 ЦЕЛЬ: {target}\n💥 ЖАЛОБ: {repeats}")
                def run():
                    SnosEngine.snos_target(target, "account", "spam", repeats, "")
                thread = threading.Thread(target=run, daemon=True)
                thread.start()
            except:
                send_telegram_message("❌ Ошибка: укажи число")
        else:
            send_telegram_message("❌ Использование: /snos @username количество")
        return
    
    if text.startswith('/status'):
        status_text = "🔴 ИДЕТ" if CONFIG['attack_running'] else "🟢 ОЖИДАНИЕ"
        total = len(CONFIG['history'])
        destroyed = sum(1 for h in CONFIG['history'] if h.get('destroyed', False))
        msg = f"""
📊 <b>СТАТУС СНОСЕРА</b>

🌐 СОСТОЯНИЕ: {status_text}
🎯 ЦЕЛЬ: {CONFIG['current_target'] or '-'}
⚡ ПОТОКОВ: {CONFIG['threads']}
📋 РЕЖИМ: {CONFIG['mode'].upper()}
📨 ВСЕГО СНОСОВ: {total}
💀 УНИЧТОЖЕНО: {destroyed}
        """
        send_telegram_message(msg)
        return
    
    if text.startswith('/stop'):
        if CONFIG['attack_running']:
            CONFIG['attack_running'] = False
            send_telegram_message("🛑 СНОС ОСТАНОВЛЕН!")
        else:
            send_telegram_message("ℹ️ СНОС НЕ ЗАПУЩЕН")
        return
    
    if text.startswith('/settings'):
        send_telegram_message("⚙️ <b>НАСТРОЙКИ</b>", settings_menu())
        return
    
    if text.startswith('/history'):
        if not CONFIG['history']:
            send_telegram_message("📜 ИСТОРИЯ ПУСТА")
            return
        msg = "📜 <b>ПОСЛЕДНИЕ 20 СНОСОВ</b>\n\n"
        for i, h in enumerate(reversed(CONFIG['history']), 1):
            status = "✅" if h.get('destroyed', False) else "❌"
            msg += f"{i}. {h['target']} — {h['success']}/{h['total']} {status} [{h['time']}]\n"
        send_telegram_message(msg)
        return
    
    send_telegram_message("❌ Неизвестная команда\n\n/start - главное меню")

# ===================================================================
# ПОЛЛИНГ БОТА
# ===================================================================
def polling_bot():
    print("🤖 ЗАПУСК УЛЬТРА-БОТА...")
    
    while True:
        try:
            url = f"https://api.telegram.org/bot{CONFIG['bot_token']}/getUpdates"
            params = {
                "offset": CONFIG['last_update_id'] + 1,
                "timeout": 30,
                "allowed_updates": ["message", "callback_query"]
            }
            
            response = requests.get(url, params=params, timeout=35)
            
            if response.status_code == 200:
                data = response.json()
                if data.get('ok') and data.get('result'):
                    for update in data['result']:
                        CONFIG['last_update_id'] = update['update_id']
                        
                        # Обработка callback_query (кнопки)
                        if 'callback_query' in update:
                            callback = update['callback_query']
                            callback_data = callback['data']
                            process_callback(callback_data)
                            
                            # Отвечаем на callback
                            answer_url = f"https://api.telegram.org/bot{CONFIG['bot_token']}/answerCallbackQuery"
                            requests.post(answer_url, data={"callback_query_id": callback['id']})
                        
                        # Обработка текстовых сообщений
                        elif 'message' in update and 'text' in update['message']:
                            chat_id = update['message']['chat']['id']
                            text = update['message']['text']
                            if chat_id == CONFIG['owner_id']:
                                process_text(text)
            else:
                print(f"⚠️ Ошибка: {response.status_code}")
                
        except Exception as e:
            print(f"⚠️ Ошибка: {e}")
        
        time.sleep(1)

# ===================================================================
# ЗАПУСК
# ===================================================================
if __name__ == "__main__":
    print("\n☢️ CYBERTEAM SNOSER v18.0 - ULTRA BOT")
    
    send_telegram_message("☢️ CYBERTEAM SNOSER v18.0 ЗАПУЩЕН 24/7!\n\n🤖 БОТ С КНОПКАМИ ГОТОВ К РАБОТЕ!")
    
    bot_thread = threading.Thread(target=polling_bot, daemon=True)
    bot_thread.start()
    
    port = int(os.environ.get("PORT", 10000))
    print(f"🌐 FLASK СЕРВЕР ЗАПУЩЕН НА ПОРТУ {port}")
    app.run(host="0.0.0.0", port=port)