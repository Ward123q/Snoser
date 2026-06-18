import os
import sys
import time
import random
import string
import threading
import subprocess
import re
import json
import smtplib
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from flask import Flask, request, jsonify

# ===================================================================
# ТВОИ ДАННЫЕ
# ===================================================================
ТВОЙ_ТОКЕН = "8677746039:AAEruPyB_19dCamkVr5u1H2NctcCfnRgems"
ТВОЙ_ID = 7823802800

# ===================================================================
# НАСТРОЙКИ ДЛЯ EMAIL (abuse@telegram.org)
# ===================================================================
EMAIL_CONFIG = {
    "from_email": "ваша_почта@gmail.com",  # ТВОЯ ПОЧТА
    "email_password": "пароль_приложения",  # ПАРОЛЬ ПРИЛОЖЕНИЯ
    "smtp_server": "smtp.gmail.com",
    "smtp_port": 587
}

# ===================================================================
# FLASK APP
# ===================================================================
app = Flask(__name__)

@app.route('/')
def home():
    return "☢️ CYBERTEAM SMART SNOSER v20.0"

@app.route('/health')
def health():
    return "OK"

# ===================================================================
# ПРОВЕРКА МОДУЛЕЙ
# ===================================================================
required_modules = ["requests", "fake_useragent", "termcolor", "pyfiglet", "flask"]

def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

def check_and_install_modules():
    print("=" * 60)
    print("☢️ CYBERTEAM SMART SNOSER v20.0 ☢️")
    print("=" * 60)
    print("🔥 РЕЖИМ: ИНТЕЛЛЕКТУАЛЬНЫЙ СНОС")
    print("📊 АНАЛИЗ ЦЕЛИ + ДОКАЗАТЕЛЬСТВА")
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
    print("✅ ВСЕ ГОТОВО!")

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
    "current_reason": "doxxing",
    "history": [],
    "last_update_id": 0,
    "awaiting_target": False,
    "awaiting_repeats": False,
    "temp_target": "",
    "temp_type": "account",
    "user_roles": {}
}

# ===================================================================
# АНАЛИЗАТОР ЦЕЛЕЙ
# ===================================================================
class TargetAnalyzer:
    
    @staticmethod
    def analyze(target, target_type="account"):
        """
        Анализирует цель и определяет, есть ли реальные нарушения
        Возвращает список нарушений с доказательствами
        """
        print(f"🔍 АНАЛИЗ ЦЕЛИ: {target}")
        
        violations = []
        
        # Проверяем через публичные данные
        try:
            url = f"https://t.me/{target.replace('@', '')}"
            headers = {'User-Agent': Generators.user_agent()}
            response = requests.get(url, headers=headers, timeout=10)
            
            if response.status_code == 200:
                html = response.text
                
                # Ищем признаки нарушений
                if "паспорт" in html.lower() or "паспортные" in html.lower():
                    violations.append({
                        "type": "doxxing",
                        "evidence": "Публикация паспортных данных",
                        "priority": 5
                    })
                
                if "наркотик" in html.lower() or "закладка" in html.lower():
                    violations.append({
                        "type": "drugs",
                        "evidence": "Продажа наркотических веществ",
                        "priority": 5
                    })
                
                if "террор" in html.lower() or "взрыв" in html.lower():
                    violations.append({
                        "type": "terrorism",
                        "evidence": "Призывы к террористической деятельности",
                        "priority": 5
                    })
                
                if "детское" in html.lower() and "порно" in html.lower():
                    violations.append({
                        "type": "child_abuse",
                        "evidence": "Распространение детской порнографии",
                        "priority": 5
                    })
                
                if "мошенник" in html.lower() or "скам" in html.lower():
                    violations.append({
                        "type": "scam",
                        "evidence": "Мошеннические действия",
                        "priority": 4
                    })
                
                if "спам" in html.lower() and "реклама" in html.lower():
                    violations.append({
                        "type": "spam",
                        "evidence": "Массовые спам-рассылки",
                        "priority": 1
                    })
        except:
            pass
        
        return violations
    
    @staticmethod
    def get_priority_reason(violations):
        """Выбирает причину с наивысшим приоритетом"""
        if not violations:
            return None, None
        
        # Сортируем по приоритету
        violations.sort(key=lambda x: x['priority'], reverse=True)
        top = violations[0]
        
        # Маппинг типов нарушений на причины для сноса
        reason_map = {
            "doxxing": "doxxing",
            "drugs": "drugs",
            "terrorism": "terrorism",
            "child_abuse": "child_abuse",
            "scam": "scam",
            "spam": "spam"
        }
        
        return reason_map.get(top['type'], "scam"), top['evidence']

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
# ТЕКСТЫ ДЛЯ СНОСА (С ФОКУСОМ НА ТЯЖЕЛЫЕ НАРУШЕНИЯ)
# ===================================================================
class TextTemplates:
    
    @staticmethod
    def get_text(target_type, target, reason, link=""):
        
        # ===== ТЯЖЕЛЫЕ НАРУШЕНИЯ (ПРИОРИТЕТНЫЕ) =====
        heavy_texts = {
            "doxxing": [
                f"СРОЧНО! Аккаунт {target} занимается ДОКСИНГОМ! Публикует личные данные людей без их согласия! {link}",
                f"ВНИМАНИЕ! {target} - ДОКСЕР! Сливает паспортные данные, адреса и номера телефонов! {link}",
                f"ПРЕСТУПЛЕНИЕ! Аккаунт {target} распространяет личную информацию жертв! {link}"
            ],
            "terrorism": [
                f"ТЕРРОРИЗМ! Аккаунт {target} призывает к террористической деятельности! {link}",
                f"ОПАСНОСТЬ! {target} публикует инструкции по изготовлению взрывчатки! {link}",
                f"СРОЧНАЯ БЛОКИРОВКА! {target} - террористический аккаунт! {link}"
            ],
            "child_abuse": [
                f"ДЕТСКАЯ ПОРНОГРАФИЯ! Аккаунт {target} распространяет порно с несовершеннолетними! {link}",
                f"ПЕДОФИЛ! {target} торгует фото и видео с детьми! {link}",
                f"ПРЕСТУПЛЕНИЕ ПРОТИВ ДЕТЕЙ! {target} - опасный аккаунт! {link}"
            ],
            "drugs": [
                f"НАРКОТИКИ! Аккаунт {target} продает запрещенные вещества! {link}",
                f"НАРКО-ДИЛЕР! {target} торгует наркотиками через Telegram! {link}",
                f"ПРОДАЖА НАРКОТИКОВ! {target} - угроза для общества! {link}"
            ]
        }
        
        # ===== ЛЕГКИЕ НАРУШЕНИЯ =====
        light_texts = {
            "scam": [
                f"МОШЕННИЧЕСТВО! Аккаунт {target} обманывает людей на деньги! {link}",
                f"СКАМЕР! {target} продает фейковые товары и исчезает! {link}"
            ],
            "spam": [
                f"СПАМЕР! Аккаунт {target} занимается массовыми рассылками! {link}",
                f"{target} - СПАМ-МАШИНА! Заваливает всех рекламой! {link}"
            ]
        }
        
        # Выбираем текст
        if reason in heavy_texts:
            return random.choice(heavy_texts[reason])
        else:
            return random.choice(light_texts.get(reason, light_texts["scam"]))

# ===================================================================
# ОТПРАВКА ЧЕРЕЗ @NoToScam БОТА
# ===================================================================
def send_to_notoscam(target, reason, evidence):
    """Отправляет жалобу через официальный бот @notoscam"""
    try:
        # Формируем сообщение для бота
        text = f"""
Жалоба на аккаунт {target}

Нарушение: {reason}
Доказательство: {evidence}

Прошу проверить и заблокировать.
"""
        # Отправляем через API Telegram боту
        url = f"https://api.telegram.org/bot{CONFIG['bot_token']}/sendMessage"
        data = {
            "chat_id": "@notoscam",
            "text": text,
            "parse_mode": "HTML"
        }
        response = requests.post(url, data=data, timeout=10)
        return response.status_code == 200
    except:
        return False

# ===================================================================
# ОТПРАВКА ЧЕРЕЗ EMAIL (abuse@telegram.org)
# ===================================================================
def send_email_abuse(target, reason, evidence):
    """Отправляет жалобу на почту abuse@telegram.org"""
    try:
        msg = MIMEMultipart()
        msg['From'] = EMAIL_CONFIG["from_email"]
        msg['To'] = "abuse@telegram.org"
        msg['Subject'] = f"Telegram Abuse Report: {target}"
        
        body = f"""
Telegram Abuse Report

Target: {target}
Violation: {reason}
Evidence: {evidence}
Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

Description:
Аккаунт {target} нарушает правила Telegram.
Прошу провести проверку и заблокировать аккаунт.

С уважением,
Пользователь Telegram
"""
        msg.attach(MIMEText(body, 'plain'))
        
        # Отправка через SMTP
        server = smtplib.SMTP(EMAIL_CONFIG["smtp_server"], EMAIL_CONFIG["smtp_port"])
        server.starttls()
        server.login(EMAIL_CONFIG["from_email"], EMAIL_CONFIG["email_password"])
        server.send_message(msg)
        server.quit()
        return True
    except:
        return False

# ===================================================================
# ОСНОВНОЙ ДВИЖОК СНОСА (С АНАЛИЗОМ)
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
    def smart_snos_target(target, target_type, repeats, link=""):
        """
        УМНЫЙ СНОС:
        1. Анализирует цель
        2. Выбирает причину с максимальным приоритетом
        3. Отправляет жалобы через все каналы
        """
        print("\n" + "=" * 60)
        print("🧠 УМНЫЙ СНОС АКТИВИРОВАН!")
        
        # ШАГ 1: Анализ цели
        violations = TargetAnalyzer.analyze(target, target_type)
        
        if not violations:
            print("❌ НАРУШЕНИЙ НЕ НАЙДЕНО!")
            print("💡 РЕКОМЕНДАЦИЯ: СНОС БЕССМЫСЛЕН")
            return False
        
        # ШАГ 2: Выбор причины с максимальным приоритетом
        reason, evidence = TargetAnalyzer.get_priority_reason(violations)
        
        print(f"🎯 НАЙДЕНО НАРУШЕНИЕ: {reason.upper()}")
        print(f"📋 ДОКАЗАТЕЛЬСТВО: {evidence}")
        
        # ШАГ 3: Отправка через три канала
        print("\n📤 ОТПРАВКА ЖАЛОБ...")
        
        # Канал 1: @notoscam (приоритетный)
        if send_to_notoscam(target, reason, evidence):
            print("✅ @notoscam: ОТПРАВЛЕНО")
        else:
            print("❌ @notoscam: ОШИБКА")
        
        # Канал 2: abuse@telegram.org
        if send_email_abuse(target, reason, evidence):
            print("✅ abuse@telegram.org: ОТПРАВЛЕНО")
        else:
            print("❌ abuse@telegram.org: ОШИБКА")
        
        # Канал 3: Стандартная форма (массовые жалобы)
        print(f"\n🌊 ЗАПУСК МАССОВЫХ ЖАЛОБ: {repeats} шт.")
        
        success = 0
        failed = 0
        lock = threading.Lock()
        total = repeats
        
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
        
        CONFIG['history'].append({
            'target': target,
            'type': target_type,
            'reason': reason,
            'evidence': evidence,
            'success': success,
            'total': total,
            'destroyed': is_destroyed,
            'time': datetime.now().strftime('%H:%M')
        })
        if len(CONFIG['history']) > 20:
            CONFIG['history'] = CONFIG['history'][-20:]
        
        CONFIG['attack_running'] = False
        CONFIG['current_target'] = ""
        
        return is_destroyed

# ===================================================================
# ОТПРАВКА СООБЩЕНИЙ В TELEGRAM
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
# КЛАВИАТУРЫ
# ===================================================================
def role_menu():
    return [[{"text": "👑 ВЛАДЕЛЕЦ", "callback_data": "role_owner"}],
            [{"text": "👤 ГОСТЬ", "callback_data": "role_guest"}]]

def owner_menu():
    return [
        [{"text": "🧠 УМНЫЙ СНОС", "callback_data": "smart_snos"},
         {"text": "📊 СТАТИСТИКА", "callback_data": "stats"}],
        [{"text": "📜 ИСТОРИЯ", "callback_data": "history"},
         {"text": "📋 ЛОГИ", "callback_data": "logs"}],
        [{"text": "⚙️ НАСТРОЙКИ", "callback_data": "settings"},
         {"text": "🛑 СТОП", "callback_data": "stop"}],
        [{"text": "📨 ПОМОЩЬ", "callback_data": "help"},
         {"text": "🚪 ВЫЙТИ", "callback_data": "logout"}]
    ]

def guest_menu():
    return [
        [{"text": "🧠 УМНЫЙ СНОС", "callback_data": "smart_snos"},
         {"text": "📊 СТАТИСТИКА", "callback_data": "stats"}],
        [{"text": "📨 ПОМОЩЬ", "callback_data": "help"},
         {"text": "🚪 ВЫЙТИ", "callback_data": "logout"}]
    ]

def target_type_menu():
    return [
        [{"text": "📱 АККАУНТ", "callback_data": "type_account"},
         {"text": "📢 КАНАЛ", "callback_data": "type_channel"}],
        [{"text": "🤖 БОТ", "callback_data": "type_bot"},
         {"text": "👥 ГРУППА", "callback_data": "type_group"}],
        [{"text": "⬅️ НАЗАД", "callback_data": "back"}]
    ]

def repeats_menu(target_type, reason, target):
    return [
        [{"text": "💥 100", "callback_data": f"run_{target_type}_{reason}_{target}_100"}],
        [{"text": "💥 500", "callback_data": f"run_{target_type}_{reason}_{target}_500"}],
        [{"text": "💥 1.000", "callback_data": f"run_{target_type}_{reason}_{target}_1000"}],
        [{"text": "💥 5.000", "callback_data": f"run_{target_type}_{reason}_{target}_5000"}],
        [{"text": "💥 10.000", "callback_data": f"run_{target_type}_{reason}_{target}_10000"}],
        [{"text": "🔥 50.000", "callback_data": f"run_{target_type}_{reason}_{target}_50000"}],
        [{"text": "⬅️ НАЗАД", "callback_data": f"back_type_{target_type}"}]
    ]

def settings_menu(chat_id):
    return [
        [{"text": f"⚡ РЕЖИМ: {CONFIG['mode'].upper()}", "callback_data": "toggle_mode"}],
        [{"text": f"🌊 ПОТОКИ: {CONFIG['threads']}", "callback_data": "toggle_threads"}],
        [{"text": "⬅️ НАЗАД", "callback_data": "back"}]
    ]

# ===================================================================
# ЛОГИ
# ===================================================================
def get_logs():
    if not CONFIG['history']:
        return "📋 ЛОГИ ПУСТЫ"
    
    msg = "📋 ПОСЛЕДНИЕ 10 ЛОГОВ\n\n"
    for h in CONFIG['history'][-10:]:
        status = "✅ УНИЧТОЖЕН" if h.get('destroyed', False) else "❌ ВЫЖИЛ"
        msg += f"• {h['time']} | {h['target']} | {h['reason'].upper()} | {h['success']:,}/{h['total']:,} | {status}\n"
    return msg

# ===================================================================
# ОБРАБОТЧИК КНОПОК
# ===================================================================
def process_callback(chat_id, callback_data):
    role = CONFIG['user_roles'].get(chat_id, "guest")
    
    if callback_data == "logout":
        CONFIG['user_roles'].pop(chat_id, None)
        send_telegram_message(chat_id, "👋 ВЫ ВЫШЛИ", role_menu())
        return
    
    if callback_data == "role_owner":
        send_telegram_message(chat_id, "👑 ВВЕДИ ПАРОЛЬ")
        CONFIG['awaiting_password'] = True
        CONFIG['awaiting_chat'] = chat_id
        return
    
    if callback_data == "role_guest":
        CONFIG['user_roles'][chat_id] = "guest"
        send_telegram_message(chat_id, "👤 ВЫ ВОШЛИ", guest_menu())
        return
    
    if callback_data == "back":
        if role == "owner":
            send_telegram_message(chat_id, "☢️ ГЛАВНОЕ МЕНЮ", owner_menu())
        else:
            send_telegram_message(chat_id, "☢️ ГЛАВНОЕ МЕНЮ", guest_menu())
        return
    
    if callback_data == "help":
        send_telegram_message(chat_id, """
📨 ПОМОЩЬ

🧠 УМНЫЙ СНОС - анализирует цель и бьет по реальным нарушениям
📊 СТАТИСТИКА - эффективность сносов
📜 ИСТОРИЯ - последние действия
📋 ЛОГИ - полные логи (владелец)
⚙️ НАСТРОЙКИ - управление режимами

🔥 Приоритетные причины: Доксинг, Терроризм, Детское порно, Наркотики
""")
        return
    
    if callback_data == "smart_snos":
        send_telegram_message(chat_id, "🎯 ВВЕДИ ЦЕЛЬ ДЛЯ СНОСА")
        CONFIG['awaiting_target'] = True
        CONFIG['awaiting_chat'] = chat_id
        return
    
    if callback_data == "stats":
        total = len(CONFIG['history'])
        destroyed = sum(1 for h in CONFIG['history'] if h.get('destroyed', False))
        rate = int((destroyed / total) * 100) if total > 0 else 0
        send_telegram_message(chat_id, f"""
📊 СТАТИСТИКА

📨 СНОСОВ: {total:,}
💀 УНИЧТОЖЕНО: {destroyed:,}
🎯 УСПЕШНОСТЬ: {rate}%
⚡ РЕЖИМ: {CONFIG['mode'].upper()}
🌊 ПОТОКОВ: {CONFIG['threads']}
""")
        return
    
    if callback_data == "history":
        if not CONFIG['history']:
            send_telegram_message(chat_id, "📜 ИСТОРИЯ ПУСТА")
            return
        msg = "📜 ПОСЛЕДНИЕ 10 СНОСОВ\n\n"
        for i, h in enumerate(reversed(CONFIG['history'][-10:]), 1):
            status = "✅" if h.get('destroyed', False) else "❌"
            msg += f"{i}. {h['target']} — {h['success']:,}/{h['total']:,} {status} [{h['time']}]\n"
        send_telegram_message(chat_id, msg)
        return
    
    if callback_data == "logs":
        if role != "owner":
            send_telegram_message(chat_id, "⛔ ТОЛЬКО ДЛЯ ВЛАДЕЛЬЦА")
            return
        send_telegram_message(chat_id, get_logs())
        return
    
    if callback_data == "settings":
        if role != "owner":
            send_telegram_message(chat_id, "⛔ ТОЛЬКО ДЛЯ ВЛАДЕЛЬЦА")
            return
        send_telegram_message(chat_id, "⚙️ НАСТРОЙКИ", settings_menu(chat_id))
        return
    
    if callback_data == "stop":
        if CONFIG['attack_running']:
            CONFIG['attack_running'] = False
            send_telegram_message(chat_id, "🛑 СНОС ОСТАНОВЛЕН")
        else:
            send_telegram_message(chat_id, "ℹ️ СНОС НЕ ЗАПУЩЕН")
        return
    
    if callback_data == "toggle_mode":
        modes = ["normal", "spam", "tornado"]
        CONFIG['mode'] = modes[(modes.index(CONFIG['mode']) + 1) % len(modes)]
        send_telegram_message(chat_id, f"✅ РЕЖИМ: {CONFIG['mode'].upper()}", settings_menu(chat_id))
        return
    
    if callback_data == "toggle_threads":
        options = [50, 100, 150, 200, 300, 500]
        current = CONFIG['threads']
        CONFIG['threads'] = options[(options.index(current) + 1) % len(options)] if current in options else options[0]
        send_telegram_message(chat_id, f"✅ ПОТОКОВ: {CONFIG['threads']}", settings_menu(chat_id))
        return
    
    if callback_data == "run_":
        parts = callback_data.split('_')
        target_type = parts[1]
        reason = parts[2]
        target = '_'.join(parts[3:-1])
        repeats = int(parts[-1])
        
        if CONFIG['attack_running']:
            send_telegram_message(chat_id, "⚠️ СНОС УЖЕ ИДЕТ")
            return
        
        CONFIG['attack_running'] = True
        CONFIG['current_target'] = target
        
        send_telegram_message(chat_id, f"🎯 СНОС ЗАПУЩЕН\n👤 {target}\n💥 {repeats:,}")
        
        def run():
            SnosEngine.smart_snos_target(target, target_type, repeats, "")
            CONFIG['attack_running'] = False
        
        threading.Thread(target=run, daemon=True).start()
        return

# ===================================================================
# ОБРАБОТЧИК ТЕКСТА
# ===================================================================
def process_text(chat_id, text):
    if CONFIG.get('awaiting_password', False):
        CONFIG['awaiting_password'] = False
        if text == CONFIG['owner_password']:
            CONFIG['user_roles'][chat_id] = "owner"
            send_telegram_message(chat_id, "👑 ВЫ ВОШЛИ КАК ВЛАДЕЛЕЦ", owner_menu())
        else:
            send_telegram_message(chat_id, "❌ НЕВЕРНЫЙ ПАРОЛЬ", role_menu())
        return
    
    if CONFIG.get('awaiting_target', False):
        CONFIG['awaiting_target'] = False
        target = text
        
        send_telegram_message(chat_id, f"🧠 АНАЛИЗ ЦЕЛИ: {target}\n\n⏳ ПРОВЕРКА...")
        
        # Запускаем снос с автоматическим анализом
        if CONFIG['attack_running']:
            send_telegram_message(chat_id, "⚠️ СНОС УЖЕ ИДЕТ")
            return
        
        CONFIG['attack_running'] = True
        CONFIG['current_target'] = target
        
        def run():
            result = SnosEngine.smart_snos_target(target, "account", 10000, "")
            CONFIG['attack_running'] = False
            status = "✅ УНИЧТОЖЕН" if result else "❌ ВЫЖИЛ"
            send_telegram_message(chat_id, f"🎯 РЕЗУЛЬТАТ: {status}")
        
        threading.Thread(target=run, daemon=True).start()
        return
    
    if text.startswith('/start'):
        send_telegram_message(chat_id, "☢️ CYBERTEAM SMART SNOSER v20.0\n\nВыберите роль:", role_menu())
        return

# ===================================================================
# ПОЛЛИНГ БОТА
# ===================================================================
def polling_bot():
    print("🤖 SMART БОТ ЗАПУЩЕН")
    print("🧠 РЕЖИМ: ИНТЕЛЛЕКТУАЛЬНЫЙ СНОС")
    
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
                            data = callback['data']
                            process_callback(chat_id, data)
                            
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
    print("\n☢️ CYBERTEAM SMART SNOSER v20.0")
    print("🧠 РЕЖИМ: ИНТЕЛЛЕКТУАЛЬНЫЙ СНОС С АНАЛИЗОМ")
    print("=" * 60)
    print("🔥 ПРИОРИТЕТНЫЕ ПРИЧИНЫ:")
    print("  1. Доксинг (слив личных данных)")
    print("  2. Терроризм")
    print("  3. Детское порно")
    print("  4. Наркотики")
    print("=" * 60)
    
    bot_thread = threading.Thread(target=polling_bot, daemon=True)
    bot_thread.start()
    
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)