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
    BotCommand("chief", "Рандомный главный черт дня"),
    BotCommand("random_admin", "Рандомный админ"),
    BotCommand("random", "Рандомный человек из списка"),
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
    bot.send_message(message.chat.id, "Гоша гей! 🤡")

@bot.message_handler(commands=["meme"])
def meme(message):
    bot.send_photo(message.chat.id, get_meme())
@bot.message_handler(commands=["repo"])
def handle_repo(message):
    bot.send_message(
        message.chat.id,
        f"{' '.join(REPO_PLAYERS)} в репу"
    )
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

@bot.message_handler(commands=["all"])
def get_admins(message):
    admin_list = bot.get_chat_administrators(message.chat.id)
    if admin_list:
        bot.send_message(message.chat.id, f"{' '.join(admin_list)}")
    else:
        bot.send_message(message.chat.id, "Нет доступных администраторов.")

bot.polling(none_stop=True, interval=0)
