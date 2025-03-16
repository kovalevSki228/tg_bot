import telebot

# Replace 'YOUR_TOKEN' with your actual bot token
bot = telebot.TeleBot('')

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
    except ValueError:
        bot.send_message(message.chat.id, "Иди нахуй")

# Define a handler for text, document, and audio messages
@bot.message_handler(content_types=['document', 'audio'])
def handle_docs_audio(message):
    # Handle document and audio messages here
    pass

# Start polling
bot.polling(none_stop=True, interval=0)