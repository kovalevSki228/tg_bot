import os
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
]
bot.set_my_commands(commands)

REPO_PLAYERS = [
    "@i_bojenka",
    "@crownvagen",
    "@kosoy06",
    "@fursten1",
    "@AquaDarida",
]

def get_admins_list(chat_id):
    admins = bot.get_chat_administrators(chat_id)
    return [f"@{admin.user.username}" for admin in admins]

@bot.message_handler(commands=["repo"])
def handle_repo(message):
    bot.send_message(
        message.chat.id,
        f"{' '.join(REPO_PLAYERS)} в репу"
    )

@bot.message_handler(commands=["all"])
def get_admins(message):
    admin_list = get_admins_list(message.chat.id)
    bot.send_message(message.chat.id, f"{' '.join(admin_list)}")

@bot.message_handler(content_types=['document', 'audio'])
def handle_docs_audio(message):
    pass

bot.polling(none_stop=True, interval=0)
