import os
import random
import json
import datetime
import telebot
from telebot.types import BotCommand

# Получаем токен
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
if not TOKEN:
    raise ValueError("Ошибка: TELEGRAM_BOT_TOKEN не задан!")

bot = telebot.TeleBot(TOKEN)

commands = [
    BotCommand("all", "Тегнуть всех"),
    BotCommand("repo", "Тегнуть в репу"),
    BotCommand("chief", "Рандомный главный черт дня"),
    BotCommand("random_admin", "Рандомный админ"),
    BotCommand("random", "Рандомный человек из списка"),
]
bot.set_my_commands(commands)

CHIEF_FILE = "chief_of_the_day.json"

def get_admins_list(chat_id):
    admins = bot.get_chat_administrators(chat_id)
    return [f"@{admin.user.username}" for admin in admins if admin.user.username]

def save_chief(chat_id, username):
    data = {
        "chat_id": chat_id,
        "username": username,
        "date": str(datetime.date.today())
    }
    with open(CHIEF_FILE, "w") as f:
        json.dump(data, f)

def load_chief(chat_id):
    if not os.path.exists(CHIEF_FILE):
        return None

    with open(CHIEF_FILE, "r") as f:
        try:
            data = json.load(f)
            if data.get("chat_id") == chat_id and data.get("date") == str(datetime.date.today()):
                return data.get("username")
        except json.JSONDecodeError:
            return None
    return None

@bot.message_handler(commands=["repo"])
def handle_repo(message):
    bot.send_message(message.chat.id, "В репу!")

@bot.message_handler(commands=["all"])
def get_admins(message):
    admin_list = get_admins_list(message.chat.id)
    if admin_list:
        bot.send_message(message.chat.id, f"{' '.join(admin_list)}")
    else:
        bot.send_message(message.chat.id, "Нет доступных администраторов.")

@bot.message_handler(commands=["chief"])
def choose_chief(message):
    current_chief = load_chief(message.chat.id)
    if current_chief:
        bot.send_message(message.chat.id, f"👹 Черт все еще: {current_chief}")
        return

    admins = get_admins_list(message.chat.id)
    if not admins:
        bot.send_message(message.chat.id, "В чате нет администраторов.")
        return

    chosen_one = random.choice(admins)
    save_chief(message.chat.id, chosen_one)
    bot.send_message(message.chat.id, f"🔥 Сегодня главный черт: {chosen_one} 🔥")

@bot.message_handler(commands=["random_admin"])
def random_admin(message):
    admin_list = get_admins_list(message.chat.id)
    if admin_list:
        chosen_admin = random.choice(admin_list)
        bot.send_message(message.chat.id, f"🎲 Случайный админ: {chosen_admin}")
    else:
        bot.send_message(message.chat.id, "В чате нет администраторов.")

@bot.message_handler(commands=["random"])
def random_user(message):
    args = message.text.split()[1:] 
    if args:
        chosen_user = random.choice(args)
        bot.send_message(message.chat.id, f"🎲 Случайный выбор: {chosen_user}")
    else:
        bot.send_message(message.chat.id, "Использование: /random @user1 @user2 @user3")

@bot.message_handler(content_types=['document', 'audio'])
def handle_docs_audio(message):
    pass

bot.polling(none_stop=True, interval=0)
