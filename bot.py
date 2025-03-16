import os
import telebot

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
if not TOKEN:
    raise ValueError("Ошибка: TELEGRAM_BOT_TOKEN не задан!")

bot = telebot.TeleBot(TOKEN)


# Define a handler for text messages
@bot.message_handler(content_types=['text'])
def handle_text(message):
    print("Environment Variables:", message.text)
    try:
        if (message_text[0] == '@all'):
            bot.send_message(
                message.chat.id,
                f"@i_bojenka @crownvagen @kosoy06 @fursten1 @AquaDarida @karanik_y @youlvly @danilamankevich @luvrzinc {message_text}"
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