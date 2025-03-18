import os
import random
import telebot
import requests
from telebot.types import BotCommand

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
if not TOKEN:
    raise ValueError("Ошибка: TELEGRAM_BOT_TOKEN не задан!")

bot = telebot.TeleBot(TOKEN)

commands = [
    BotCommand("russian_roulette", "Русская рулетка"),
    BotCommand("insult", "Оскорбление случайного пользователя"),
    BotCommand("insult_me", "Оскорбление тебя"),
    BotCommand("praise", "Комплимент случайному пользователю"),
    BotCommand("fact", "Случайный интересный факт"),
    BotCommand("joke", "Случайная шутка"),
    BotCommand("meme", "Случайный мем"),
    BotCommand("all", "Тегнуть всех"),
    BotCommand("repo", "Тегнуть в репу"),
    BotCommand("gosha_gay", "Гоша гей"),
]
bot.set_my_commands(commands)
REPO_PLAYERS = [
    "@i_bojenka",
    "@crownvagen",
    "@kosoy06",
    "@fursten1",
    "@AquaDarida",
    "@danilamankevich",
]

# 📌 Функции для запросов к API
def get_insult():
    try:
        response = requests.get("https://evilinsult.com/generate_insult.php?lang=en&type=json").json()
        return response.get("insult", "Ты лошара, даже API не смогло оскорбить тебя! 🤡")
    except:
        return "Ты неудачник даже для API! 😂"

def get_praise():
    try:
        response = requests.get("https://complimentr.com/api").json()
        return response.get("compliment", "Ты лучший человек в этом чате! 😊")
    except:
        return "Ты великолепен! Даже сервер завис от твоей крутости! 😎"

def get_fact():
    try:
        response = requests.get("https://uselessfacts.jsph.pl/random.json?language=en").json()
        return response.get("text", "Факты закончились, но ты все равно молодец!")
    except:
        return "Сегодня без фактов, но ты и так умный!"

def get_joke():
    try:
        response = requests.get("https://official-joke-api.appspot.com/random_joke").json()
        return f"{response.get('setup', '')} - {response.get('punchline', '')}"
    except:
        return "Я забыл шутку... но ты все равно смешной! 😆"

def get_meme():
    try:
        response = requests.get("https://meme-api.com/gimme").json()
        return response.get("url", "https://i.redd.it/7n7lbtrkslm51.jpg")
    except:
        return "Что-то пошло не так с мемами, но представь смешной мем"

# 🔥 **Команды**
@bot.message_handler(commands=["russian_roulette"])
def russian_roulette(message):
    if random.randint(1, 6) == 1:
        bot.send_message(message.chat.id, f"💥 {message.from_user.first_name} выстрелил... и проиграл! R.I.P ☠️")
    else:
        bot.send_message(message.chat.id, f"😎 {message.from_user.first_name} выстрелил... но остался в живых!")

@bot.message_handler(commands=["insult"])
def insult_user(message):
    chat_members = bot.get_chat_administrators(message.chat.id)
    if not chat_members:
        bot.send_message(message.chat.id, "В чате нет админов, но все равно кто-то из вас идиот!")
        return
    chosen_one = random.choice(chat_members).user.username
    bot.send_message(message.chat.id, f"🔥 @{chosen_one}, {get_insult()}")

@bot.message_handler(commands=["insult_me"])
def insult_me(message):
    bot.send_message(message.chat.id, f"{message.from_user.first_name}, {get_insult()}")

@bot.message_handler(commands=["praise"])
def praise_user(message):
    chat_members = bot.get_chat_administrators(message.chat.id)
    if not chat_members:
        bot.send_message(message.chat.id, "Ты прекрасен! 😊")
        return
    chosen_one = random.choice(chat_members).user.username
    bot.send_message(message.chat.id, f"✨ @{chosen_one}, {get_praise()}")

@bot.message_handler(commands=["fact"])
def fact(message):
    bot.send_message(message.chat.id, get_fact())

@bot.message_handler(commands=["joke"])
def joke(message):
    bot.send_message(message.chat.id, get_joke())

@bot.message_handler(commands=["gosha_gay"])
def joke(message):
    bot.send_message(message.chat.id, "Илья гей! 🤡")

@bot.message_handler(commands=["meme"])
def meme(message):
    bot.send_photo(message.chat.id, get_meme())
@bot.message_handler(commands=["repo"])
def handle_repo(message):
    bot.send_message(
        message.chat.id,
        f"{' '.join(REPO_PLAYERS)} в репу"
    )

@bot.message_handler(commands=["all"])
def get_admins(message):
    admin_list = bot.get_chat_administrators(message.chat.id)
    if admin_list:
        bot.send_message(message.chat.id, f"{' '.join(admin_list)}")
    else:
        bot.send_message(message.chat.id, "Нет доступных администраторов.")

bot.polling(none_stop=True, interval=0)
