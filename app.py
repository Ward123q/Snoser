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
        "threads": CONFIG.get("threads", 200),
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
    print("☢️ CYBERTEAM SNOSER v19.0 - MEGA EDITION ☢️")
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

# ===================================================================
# КОНФИГ
# ===================================================================
CONFIG = {
    "threads": 200,
    "request_timeout": 15,
    "delay_min": 0.05,
    "delay_max": 0.15,
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
    "temp_type": "account",
    "user_roles": {}
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
                    f"Пользователь {target} использует ботов для спам-рассылок! Отправил более 10000 сообщений!",
                    f"Спам-ферма {target}! Каждый день новые жертвы! Это уже невыносимо!",
                    f"Аккаунт {target} - СПАМ-МАШИНА! Заваливает всех рекламой 24/7!"
                ],
                "insult": [
                    f"Аккаунт {target} ОСКОРБЛЯЕТ пользователей каждый день! Нецензурная брань и унижения!",
                    f"{target} - АГРЕССОР! Оскорбляет всех в чатах без причины! Мы устали от него!",
                    f"Пользователь {target} разжигает конфликты и оскорбляет каждого участника!",
                    f"{target} написал оскорбления в мой адрес и угрожает расправой! Я боюсь!",
                    f"Аккаунт {target} - ТРОЛЛЬ-АГРЕССОР! Оскорбляет людей за внешность и возраст!"
                ],
                "scam": [
                    f"Аккаунт {target} - МОШЕННИК! Обманул уже 30 человек на крупные суммы!",
                    f"{target} продает фейковые товары и исчезает с деньгами! Это скам!",
                    f"Пользователь {target} - СКАМЕР! Предлагает легкий заработок, а крадет деньги!",
                    f"{target} обманул меня на 10000 рублей! Обещал товар и исчез в никуда!",
                    f"Аккаунт {target} занимается ФИШИНГОМ! Крадет данные карт и паролей!"
                ],
                "illegal": [
                    f"Аккаунт {target} распространяет НЕЛЕГАЛЬНЫЙ контент! Нарушает закон РФ!",
                    f"{target} продает НАРКОТИКИ! Статья 228.1 УК РФ! Срочно заблокировать!",
                    f"Пользователь {target} публикует ЭКСТРЕМИСТСКИЕ материалы! Статья 282 УК РФ!",
                    f"{target} распространяет ДЕТСКУЮ ПОРНОГРАФИЮ! Статья 242.1 УК РФ!",
                    f"Аккаунт {target} призывает к ТЕРРОРИЗМУ! Статья 205.2 УК РФ!"
                ],
                "fake": [
                    f"Аккаунт {target} использует ВИРТУАЛЬНЫЙ НОМЕР! Это фейковый аккаунт!",
                    f"{target} зарегистрирован на одноразовый номер. Это мошенник 100%!",
                    f"Аккаунт {target} - ФЕЙК! Нет реального пользователя за ним!",
                    f"Пользователь {target} скрывает свой настоящий номер. Это подозрительно!",
                    f"{target} использует номер с сайта активации. Такой аккаунт опасен!"
                ],
                "phishing": [
                    f"Аккаунт {target} - ФИШИНГОВЫЙ! Крадет данные банковских карт!",
                    f"{target} рассылает фишинговые ссылки! Это угроза безопасности!",
                    f"Пользователь {target} создает поддельные сайты для кражи данных!",
                    f"{target} - ВОР! Крадет аккаунты через фишинговые ссылки!",
                    f"Аккаунт {target} используется для фишинговых атак на пользователей!"
                ],
                "doxxing": [
                    f"Аккаунт {target} занимается ДОКСИНГОМ! Сливает личные данные людей!",
                    f"{target} публикует паспортные данные, адреса и номера телефонов!",
                    f"Пользователь {target} - ДОКСЕР! Угрожает людям через личные данные!",
                    f"{target} сливает интимные фото без согласия! Это преступление!",
                    f"Аккаунт {target} - ОПАСНЫЙ! Публикует личную информацию жертв!"
                ],
                "terror": [
                    f"Аккаунт {target} призывает к ТЕРРОРИЗМУ! Статья 205.2 УК РФ!",
                    f"{target} - ТЕРРОРИСТИЧЕСКИЙ аккаунт! Публикует инструкции по взрывчатке!",
                    f"Пользователь {target} оправдывает терроризм и теракты!",
                    f"{target} - ЭКСТРЕМИСТ! Призывает к свержению власти!",
                    f"Аккаунт {target} публикует видео казней и пыток!"
                ],
                "drugs": [
                    f"Аккаунт {target} продает НАРКОТИКИ! Статья 228.1 УК РФ!",
                    f"{target} - НАРКО-ДИЛЕР! Торгует запрещенными веществами!",
                    f"Пользователь {target} пропагандирует наркотики среди подростков!",
                    f"{target} - НАРКО-ШОП! Продает спайсы, соли, героин!",
                    f"Аккаунт {target} - ОПАСНОСТЬ! Рекламирует наркотики в открытую!"
                ],
                "child_porn": [
                    f"Аккаунт {target} распространяет ДЕТСКУЮ ПОРНОГРАФИЮ! Статья 242.1 УК РФ!",
                    f"{target} - ПЕДОФИЛ! Торгует фото и видео с детьми!",
                    f"Пользователь {target} - ОПАСНЫЙ! Собирает и продает детские фото!",
                    f"{target} - ПЕДО-СЕТЬ! Организует обмен детским порно!",
                    f"Аккаунт {target} - УГРОЗА! Распространяет порно с младенцами!"
                ],
                "violence": [
                    f"Аккаунт {target} призывает к НАСИЛИЮ! Статья 119 УК РФ!",
                    f"{target} - АГРЕССОР! Призывает к избиению людей!",
                    f"Пользователь {target} угрожает расправой оппонентам!",
                    f"{target} - ОПАСНЫЙ! Организует нападения на людей!",
                    f"Аккаунт {target} - УГРОЗА! Призывает к насильственным действиям!"
                ],
                "hate": [
                    f"Аккаунт {target} РАЗЖИГАЕТ НЕНАВИСТЬ! Статья 282 УК РФ!",
                    f"{target} - НАЦИСТ! Публикует расистские посты!",
                    f"Пользователь {target} разжигает межнациональную рознь!",
                    f"{target} - ФАШИСТ! Пропаганда превосходства нации!",
                    f"Аккаунт {target} - НЕНАВИСТЬ! Оскорбляет религиозные чувства!"
                ],
                "harassment": [
                    f"Аккаунт {target} - ДОМОГАТЕЛЬ! Преследует людей в чатах!",
                    f"{target} - СТАЛКЕР! Следит за людьми и пишет угрозы!",
                    f"Пользователь {target} - МАНЬЯК! Преследует девушек в личке!",
                    f"{target} - ПРЕСЛЕДОВАТЕЛЬ! Не дает прохода людям!",
                    f"Аккаунт {target} - СТАЛКЕР-МАНЬЯК! Угрожает физической расправой!"
                ],
                "impersonation": [
                    f"Аккаунт {target} - ПОДДЕЛЬНЫЙ! Выдает себя за известную личность!",
                    f"{target} - ФЕЙК! Притворяется сотрудником Telegram!",
                    f"Пользователь {target} - САМОЗВАНЕЦ! Выдает себя за другого человека!",
                    f"{target} - КЛОН! Копирует аккаунт известного блогера!",
                    f"Аккаунт {target} - ПОДДЕЛКА! Использует чужое имя и фото!"
                ],
                "bot": [
                    f"Аккаунт {target} - НЕЛЕГАЛЬНЫЙ БОТ! Нарушает правила Telegram!",
                    f"{target} - БОТ-СПАМЕР! Отправляет тысячи сообщений!",
                    f"Пользователь {target} - БОТ! Нет реального человека за аккаунтом!",
                    f"{target} - АВТОМАТ! Работает по расписанию и спамит!",
                    f"Аккаунт {target} - БОТ-МОШЕННИК! Автоматически обманывает людей!"
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
# ДВИЖОК СНОСА (МЕГА-МОЩНЫЙ!)
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
        print(f"💥 ЖАЛОБ: {total:,}")
        
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
        
        print(f"✅ УСПЕШНО: {success:,}/{total:,}")
        print(f"❌ ОШИБОК: {failed:,}/{total:,}")
        
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
# ОТПРАВКА СООБЩЕНИЙ
# ===================================================================
def send_telegram_message(chat_id, text, keyboard=None):
    try:
        url = f"https://api.telegram.org/bot{CONFIG['bot_token']}/sendMessage"
        data = {
            "chat_id": chat_id,
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
# КЛАВИАТУРЫ (С ДО 1.000.000!)
# ===================================================================
def role_menu():
    keyboard = [
        [{"text": "👑 ВЛАДЕЛЕЦ (нужен пароль)", "callback_data": "role_owner"}],
        [{"text": "👤 ГОСТЬ (без пароля)", "callback_data": "role_guest"}]
    ]
    return keyboard

def owner_menu():
    keyboard = [
        [
            {"text": "📱 СНОС", "callback_data": "snos"},
            {"text": "📊 СТАТИСТИКА", "callback_data": "stats"}
        ],
        [
            {"text": "📜 ИСТОРИЯ", "callback_data": "history"},
            {"text": "📋 ЛОГИ", "callback_data": "logs"}
        ],
        [
            {"text": "⚙️ НАСТРОЙКИ", "callback_data": "settings"},
            {"text": "🛑 СТОП", "callback_data": "stop"}
        ],
        [
            {"text": "📨 ПОМОЩЬ", "callback_data": "help"},
            {"text": "🚪 ВЫЙТИ", "callback_data": "logout"}
        ]
    ]
    return keyboard

def guest_menu():
    keyboard = [
        [
            {"text": "📱 СНОС", "callback_data": "snos"},
            {"text": "📊 СТАТИСТИКА", "callback_data": "stats"}
        ],
        [
            {"text": "📨 ПОМОЩЬ", "callback_data": "help"},
            {"text": "🚪 ВЫЙТИ", "callback_data": "logout"}
        ]
    ]
    return keyboard

def target_type_menu():
    keyboard = [
        [
            {"text": "📱 АККАУНТ", "callback_data": "type_account"},
            {"text": "📢 КАНАЛ", "callback_data": "type_channel"}
        ],
        [
            {"text": "🤖 БОТ", "callback_data": "type_bot"},
            {"text": "👥 ГРУППА", "callback_data": "type_group"}
        ],
        [{"text": "⬅️ НАЗАД", "callback_data": "back"}]
    ]
    return keyboard

def reason_menu(target_type, target):
    reasons = {
        "account": [
            ("💀 Спам", "spam"),
            ("😡 Оскорбление", "insult"),
            ("💰 Мошенничество", "scam"),
            ("🚫 Нелегальный контент", "illegal"),
            ("🎭 Фейк", "fake"),
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
        ]
    }
    keyboard = []
    for label, value in reasons.get(target_type, reasons["account"]):
        keyboard.append([{"text": label, "callback_data": f"reason_{target_type}_{value}_{target}"}])
    keyboard.append([{"text": "⬅️ НАЗАД", "callback_data": f"back_type_{target_type}"}])
    return keyboard

def repeats_menu(target_type, reason, target):
    keyboard = [
        [{"text": "💥 100", "callback_data": f"run_{target_type}_{reason}_{target}_100"}],
        [{"text": "💥 500", "callback_data": f"run_{target_type}_{reason}_{target}_500"}],
        [{"text": "💥 1.000", "callback_data": f"run_{target_type}_{reason}_{target}_1000"}],
        [{"text": "💥 5.000", "callback_data": f"run_{target_type}_{reason}_{target}_5000"}],
        [{"text": "💥 10.000", "callback_data": f"run_{target_type}_{reason}_{target}_10000"}],
        [{"text": "💥 50.000", "callback_data": f"run_{target_type}_{reason}_{target}_50000"}],
        [{"text": "💥 100.000", "callback_data": f"run_{target_type}_{reason}_{target}_100000"}],
        [{"text": "💥 500.000", "callback_data": f"run_{target_type}_{reason}_{target}_500000"}],
        [{"text": "🔥 1.000.000", "callback_data": f"run_{target_type}_{reason}_{target}_1000000"}],
        [{"text": "⬅️ НАЗАД", "callback_data": f"back_reason_{target_type}_{target}"}]
    ]
    return keyboard

def settings_menu(chat_id):
    keyboard = [
        [{"text": f"⚡ РЕЖИМ: {CONFIG['mode'].upper()}", "callback_data": "toggle_mode"}],
        [{"text": f"🌊 ПОТОКИ: {CONFIG['threads']}", "callback_data": "toggle_threads"}],
        [{"text": f"⏱️ ЗАДЕРЖКА: {CONFIG['delay_min']}-{CONFIG['delay_max']}с", "callback_data": "toggle_delay"}],
        [{"text": "⬅️ НАЗАД", "callback_data": "back"}]
    ]
    return keyboard

# ===================================================================
# ЛОГИ
# ===================================================================
def get_logs():
    logs = []
    for h in CONFIG['history'][-10:]:
        status = "✅ УНИЧТОЖЕН" if h.get('destroyed', False) else "❌ ВЫЖИЛ"
        logs.append(f"{h['time']} | {h['target']} | {h['success']:,}/{h['total']:,} | {status}")
    
    if not logs:
        return "📋 <b>ЛОГИ ПУСТЫ</b>\n\nПока не было сносов."
    
    msg = "📋 <b>ПОСЛЕДНИЕ 10 ЛОГОВ</b>\n\n"
    for log in logs:
        msg += f"• {log}\n"
    return msg

# ===================================================================
# ОБРАБОТЧИК КНОПОК
# ===================================================================
def process_callback(chat_id, callback_data):
    parts = callback_data.split('_')
    role = CONFIG['user_roles'].get(chat_id, "guest")
    
    if callback_data == "logout":
        if chat_id in CONFIG['user_roles']:
            del CONFIG['user_roles'][chat_id]
        send_telegram_message(chat_id, "👋 <b>ВЫ ВЫШЛИ</b>\n\nНажми /start для входа.")
        return
    
    if callback_data == "role_owner":
        send_telegram_message(chat_id, "👑 <b>ВВЕДИ ПАРОЛЬ</b>")
        CONFIG['awaiting_password'] = True
        CONFIG['awaiting_chat'] = chat_id
        return
    
    if callback_data == "role_guest":
        CONFIG['user_roles'][chat_id] = "guest"
        send_telegram_message(chat_id, "👤 <b>ВЫ ВОШЛИ КАК ГОСТЬ</b>", guest_menu())
        return
    
    if callback_data == "back":
        if role == "owner":
            send_telegram_message(chat_id, "☢️ <b>ГЛАВНОЕ МЕНЮ</b>", owner_menu())
        else:
            send_telegram_message(chat_id, "☢️ <b>ГЛАВНОЕ МЕНЮ</b>", guest_menu())
        return
    
    if callback_data == "help":
        msg = """
📨 <b>ПОМОЩЬ</b>

<b>КОМАНДЫ:</b>
/start - Вход в систему
/snos @user 500 - Быстрый снос
/status - Статус
/stop - Остановить
/settings - Настройки (владелец)
/history - История
/logs - Логи (владелец)

<b>ДО 1.000.000 ЖАЛОБ ЗА РАЗ!</b>
🔥 Мега-режим для реальных задач!
        """
        keyboard = [[{"text": "⬅️ НАЗАД", "callback_data": "back"}]]
        send_telegram_message(chat_id, msg, keyboard)
        return
    
    if callback_data == "snos":
        send_telegram_message(chat_id, "🎯 <b>ВЫБЕРИ ТИП</b>", target_type_menu())
        return
    
    if callback_data == "stats":
        total = len(CONFIG['history'])
        destroyed = sum(1 for h in CONFIG['history'] if h.get('destroyed', False))
        success_rate = int((destroyed / total) * 100) if total > 0 else 0
        
        msg = f"""
📊 <b>СТАТИСТИКА</b>

📨 СНОСОВ: {total:,}
💀 УНИЧТОЖЕНО: {destroyed:,}
🎯 УСПЕШНОСТЬ: {success_rate}%
⚡ РЕЖИМ: {CONFIG['mode'].upper()}
🌊 ПОТОКОВ: {CONFIG['threads']}
        """
        keyboard = [[{"text": "🔄 ОБНОВИТЬ", "callback_data": "stats"}]]
        send_telegram_message(chat_id, msg, keyboard)
        return
    
    if callback_data == "history":
        if not CONFIG['history']:
            send_telegram_message(chat_id, "📜 ИСТОРИЯ ПУСТА")
            return
        
        msg = "📜 <b>ПОСЛЕДНИЕ 10 СНОСОВ</b>\n\n"
        for i, h in enumerate(reversed(CONFIG['history'][-10:]), 1):
            status = "✅" if h.get('destroyed', False) else "❌"
            msg += f"{i}. {h['target']} — {h['success']:,}/{h['total']:,} {status} [{h['time']}]\n"
        
        keyboard = [[{"text": "🔄 ОБНОВИТЬ", "callback_data": "history"}]]
        send_telegram_message(chat_id, msg, keyboard)
        return
    
    if callback_data == "logs":
        if role != "owner":
            send_telegram_message(chat_id, "⛔ ТОЛЬКО ДЛЯ ВЛАДЕЛЬЦА!")
            return
        send_telegram_message(chat_id, get_logs(), [[{"text": "🔄 ОБНОВИТЬ", "callback_data": "logs"}]])
        return
    
    if callback_data == "settings":
        if role != "owner":
            send_telegram_message(chat_id, "⛔ ТОЛЬКО ДЛЯ ВЛАДЕЛЬЦА!")
            return
        send_telegram_message(chat_id, "⚙️ <b>НАСТРОЙКИ</b>", settings_menu(chat_id))
        return
    
    if callback_data == "stop":
        if CONFIG['attack_running']:
            CONFIG['attack_running'] = False
            send_telegram_message(chat_id, "🛑 СНОС ОСТАНОВЛЕН!")
        else:
            send_telegram_message(chat_id, "ℹ️ СНОС НЕ ЗАПУЩЕН")
        return
    
    if callback_data == "toggle_mode":
        if role != "owner":
            send_telegram_message(chat_id, "⛔ Доступ запрещен!")
            return
        modes = ["normal", "spam", "tornado"]
        current = CONFIG['mode']
        next_mode = modes[(modes.index(current) + 1) % len(modes)]
        CONFIG['mode'] = next_mode
        send_telegram_message(chat_id, f"✅ РЕЖИМ: {next_mode.upper()}", settings_menu(chat_id))
        return
    
    if callback_data == "toggle_threads":
        if role != "owner":
            send_telegram_message(chat_id, "⛔ Доступ запрещен!")
            return
        options = [50, 100, 150, 200, 300, 500]
        current = CONFIG['threads']
        next_idx = (options.index(current) + 1) % len(options) if current in options else 0
        CONFIG['threads'] = options[next_idx]
        send_telegram_message(chat_id, f"✅ ПОТОКОВ: {CONFIG['threads']}", settings_menu(chat_id))
        return
    
    if callback_data == "toggle_delay":
        if role != "owner":
            send_telegram_message(chat_id, "⛔ Доступ запрещен!")
            return
        delays = [(0.05, 0.15), (0.1, 0.3), (0.2, 0.5), (0.5, 1.0)]
        current = (CONFIG['delay_min'], CONFIG['delay_max'])
        next_idx = (delays.index(current) + 1) % len(delays) if current in delays else 0
        CONFIG['delay_min'], CONFIG['delay_max'] = delays[next_idx]
        send_telegram_message(chat_id, f"✅ ЗАДЕРЖКА: {CONFIG['delay_min']}-{CONFIG['delay_max']}с", settings_menu(chat_id))
        return
    
    if callback_data.startswith("type_"):
        target_type = callback_data.split('_')[1]
        CONFIG['temp_type'] = target_type
        send_telegram_message(chat_id, f"🎯 <b>ВВЕДИ @USERNAME</b>\n\n📋 ТИП: {target_type.upper()}")
        CONFIG['awaiting_target'] = True
        CONFIG['awaiting_chat'] = chat_id
        return
    
    if callback_data.startswith("back_type_"):
        target_type = callback_data.split('_')[2]
        send_telegram_message(chat_id, "🎯 <b>ВЫБЕРИ ТИП</b>", target_type_menu())
        return
    
    if callback_data.startswith("reason_"):
        parts = callback_data.split('_')
        target_type = parts[1]
        reason = parts[2]
        target = '_'.join(parts[3:])
        
        msg = f"""
🎯 <b>ВЫБЕРИ КОЛИЧЕСТВО</b>

👤 {target}
📋 {target_type.upper()}
🔥 {reason.upper()}

<b>ДО 1.000.000 ЖАЛОБ!</b>
        """
        send_telegram_message(chat_id, msg, repeats_menu(target_type, reason, target))
        return
    
    if callback_data.startswith("back_reason_"):
        _, _, target_type, target = callback_data.split('_', 3)
        send_telegram_message(chat_id, f"🎯 <b>ВЫБЕРИ ПРИЧИНУ</b>\n\n👤 {target}", reason_menu(target_type, target))
        return
    
    if callback_data.startswith("run_"):
        parts = callback_data.split('_')
        target_type = parts[1]
        reason = parts[2]
        target = '_'.join(parts[3:-1])
        repeats = int(parts[-1])
        
        if CONFIG['attack_running']:
            send_telegram_message(chat_id, "⚠️ СНОС УЖЕ ИДЕТ!")
            return
        
        CONFIG['attack_running'] = True
        CONFIG['current_target'] = target
        
        msg = f"""
🎯 <b>СНОС ЗАПУЩЕН!</b>

👤 {target}
📋 {target_type.upper()}
🔥 {reason.upper()}
💥 {repeats:,} ЖАЛОБ
🌊 {CONFIG['threads']} ПОТОКОВ
        """
        send_telegram_message(chat_id, msg)
        
        def run():
            SnosEngine.snos_target(target, target_type, reason, repeats, "")
        
        thread = threading.Thread(target=run, daemon=True)
        thread.start()
        return

# ===================================================================
# ОБРАБОТЧИК ТЕКСТА
# ===================================================================
def process_text(chat_id, text):
    text = text.strip()
    
    if CONFIG.get('awaiting_password', False) and CONFIG.get('awaiting_chat') == chat_id:
        CONFIG['awaiting_password'] = False
        if text == CONFIG['owner_password']:
            CONFIG['user_roles'][chat_id] = "owner"
            send_telegram_message(chat_id, "👑 <b>ВЫ ВОШЛИ КАК ВЛАДЕЛЕЦ!</b>", owner_menu())
        else:
            send_telegram_message(chat_id, "❌ <b>НЕВЕРНЫЙ ПАРОЛЬ!</b>", role_menu())
        return
    
    if CONFIG.get('awaiting_target', False) and CONFIG.get('awaiting_chat') == chat_id:
        CONFIG['awaiting_target'] = False
        target = text
        target_type = CONFIG['temp_type']
        send_telegram_message(chat_id, f"🎯 <b>ВЫБЕРИ ПРИЧИНУ</b>\n\n👤 {target}\n📋 {target_type.upper()}", reason_menu(target_type, target))
        return
    
    if text.startswith('/start'):
        role = CONFIG['user_roles'].get(chat_id)
        if role == "owner":
            send_telegram_message(chat_id, "👑 <b>ДОБРО ПОЖАЛОВАТЬ, ВЛАДЕЛЕЦ!</b>", owner_menu())
        elif role == "guest":
            send_telegram_message(chat_id, "👤 <b>ДОБРО ПОЖАЛОВАТЬ, ГОСТЬ!</b>", guest_menu())
        else:
            send_telegram_message(chat_id, "☢️ <b>CYBERTEAM SNOSER</b>\n\nВыберите роль:", role_menu())
        return
    
    if text.startswith('/snos'):
        parts = text.split()
        if len(parts) >= 3:
            target = parts[1]
            try:
                repeats = int(parts[2])
                if CONFIG['attack_running']:
                    send_telegram_message(chat_id, "⚠️ СНОС УЖЕ ИДЕТ!")
                    return
                CONFIG['attack_running'] = True
                CONFIG['current_target'] = target
                send_telegram_message(chat_id, f"🎯 СНОС ЗАПУЩЕН!\n👤 {target}\n💥 {repeats:,}")
                def run():
                    SnosEngine.snos_target(target, "account", "spam", repeats, "")
                thread = threading.Thread(target=run, daemon=True)
                thread.start()
            except:
                send_telegram_message(chat_id, "❌ Ошибка: укажи число")
        else:
            send_telegram_message(chat_id, "❌ /snos @username 500")
        return
    
    if text.startswith('/status'):
        status_text = "🔴 ИДЕТ" if CONFIG['attack_running'] else "🟢 ОЖИДАНИЕ"
        total = len(CONFIG['history'])
        destroyed = sum(1 for h in CONFIG['history'] if h.get('destroyed', False))
        msg = f"""
📊 <b>СТАТУС</b>

🌐 {status_text}
🎯 {CONFIG['current_target'] or '-'}
⚡ {CONFIG['threads']} потоков
📋 {CONFIG['mode'].upper()}
📨 СНОСОВ: {total:,}
💀 УНИЧТОЖЕНО: {destroyed:,}
        """
        send_telegram_message(chat_id, msg)
        return
    
    if text.startswith('/stop'):
        if CONFIG['attack_running']:
            CONFIG['attack_running'] = False
            send_telegram_message(chat_id, "🛑 СНОС ОСТАНОВЛЕН!")
        else:
            send_telegram_message(chat_id, "ℹ️ СНОС НЕ ЗАПУЩЕН")
        return
    
    if text.startswith('/history'):
        if not CONFIG['history']:
            send_telegram_message(chat_id, "📜 ИСТОРИЯ ПУСТА")
            return
        msg = "📜 <b>ПОСЛЕДНИЕ 10 СНОСОВ</b>\n\n"
        for i, h in enumerate(reversed(CONFIG['history'][-10:]), 1):
            status = "✅" if h.get('destroyed', False) else "❌"
            msg += f"{i}. {h['target']} — {h['success']:,}/{h['total']:,} {status} [{h['time']}]\n"
        send_telegram_message(chat_id, msg)
        return
    
    if text.startswith('/logs'):
        role = CONFIG['user_roles'].get(chat_id)
        if role != "owner":
            send_telegram_message(chat_id, "⛔ ТОЛЬКО ДЛЯ ВЛАДЕЛЬЦА!")
            return
        send_telegram_message(chat_id, get_logs())
        return
    
    if text.startswith('/settings'):
        role = CONFIG['user_roles'].get(chat_id)
        if role != "owner":
            send_telegram_message(chat_id, "⛔ ТОЛЬКО ДЛЯ ВЛАДЕЛЬЦА!")
            return
        send_telegram_message(chat_id, "⚙️ <b>НАСТРОЙКИ</b>", settings_menu(chat_id))
        return
    
    send_telegram_message(chat_id, "❌ Неизвестная команда\n\n/help - помощь")

# ===================================================================
# ПОЛЛИНГ БОТА
# ===================================================================
def polling_bot():
    print("🤖 ЗАПУСК МЕГА-БОТА (ДО 1.000.000 ЖАЛОБ!)")
    
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
                        
                        if 'callback_query' in update:
                            callback = update['callback_query']
                            chat_id = callback['message']['chat']['id']
                            callback_data = callback['data']
                            process_callback(chat_id, callback_data)
                            
                            answer_url = f"https://api.telegram.org/bot{CONFIG['bot_token']}/answerCallbackQuery"
                            requests.post(answer_url, data={"callback_query_id": callback['id']})
                        
                        elif 'message' in update and 'text' in update['message']:
                            chat_id = update['message']['chat']['id']
                            text = update['message']['text']
                            process_text(chat_id, text)
            else:
                print(f"⚠️ Ошибка: {response.status_code}")
                
        except Exception as e:
            print(f"⚠️ Ошибка: {e}")
        
        time.sleep(1)

# ===================================================================
# ЗАПУСК
# ===================================================================
if __name__ == "__main__":
    print("\n☢️ CYBERTEAM SNOSER v19.0 - MEGA EDITION")
    print("🔥 ДО 1.000.000 ЖАЛОБ ЗА РАЗ!")
    
    bot_thread = threading.Thread(target=polling_bot, daemon=True)
    bot_thread.start()
    
    port = int(os.environ.get("PORT", 10000))
    print(f"🌐 FLASK СЕРВЕР ЗАПУЩЕН НА ПОРТУ {port}")
    app.run(host="0.0.0.0", port=port)