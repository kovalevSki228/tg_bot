import os
import telebot
from telebot.types import BotCommand
print("Environment Variables:", os.environ)
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
if not TOKEN:
    raise ValueError("Ошибка: TELEGRAM_BOT_TOKEN не задан!")

bot = telebot.TeleBot(TOKEN)
# Список команд для бота
commands = [
    BotCommand("all", "Тегнуть всех"),
    BotCommand("repo", "Тегнуть в репу"),
]

# Устанавливаем команды
bot.set_my_commands(commands)

# Define a handler for text messages
@bot.message_handler(content_types=['text'])
def handle_text(message):
    message_text = message.text.split()
    try:
        if (message_text[0] == '@all'):
            bot.send_message(
                message.chat.id,
                f"@i_bojenka @crownvagen @kosoy06 @fursten1 @AquaDarida @karanik_y @youlvly @danilamankevich @luvrzinc {message_text}"
            )
        if (message_text[0] == '@repo'):
            bot.send_message(
                message.chat.id,
                f"@i_bojenka @crownvagen @kosoy06 @fursten1 @AquaDarida @karanik_y в репу"
            )
    except ValueError:
        bot.send_message(message.chat.id, "Иди нахуй")

# Define a handler for text, document, and audio messages
@bot.message_handler(content_types=['document', 'audio'])
def handle_docs_audio(message):
    # Handle document and audio messages here
    pass

# Start polling
bot.polling(none_stop=True, interval=0)