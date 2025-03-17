import { CONFIG } from './config';

const BOT_TOKEN = process.env.TELEGRAM_BOT_TOKEN; 

if (!BOT_TOKEN) throw new Error('Invalid BOT_TOKEN')

let chatId = "";
let lastKnownMessageId = null;

const REPO_PLAYERS = [
    "@i_bojenka",
    "@crownvagen",
    "@kosoy06",
    "@fursten1",
    "@AquaDarida",
    "@danilamankevich"
]

const commands = [
    { command: 'all', description: 'Тегнуть всех' },
    { command: 'repo', description: 'Тегнуть в репу'}
]

function processCommand(command) {
    if (command === "/all") {
        getChatAdministrators()
        .then(admins => {
            if (!admins) return;
            const userNames = admins
                .filter(a => !a.user.is_bot)
                .map(a => `@${a.user.username}`);

            sendMessage(userNames.join(' '));
        });
         
    } else if (command === "/repo") {
        sendMessage(`${REPO_PLAYERS.join(' ')} в репу`);
    } else {
        sendMessage("Неизвестная команда.");
    }
}

function sendMessage(text) {
    const url = `https://api.telegram.org/bot${BOT_TOKEN}/sendMessage`;
    const data = {
        chat_id: chatId,
        text: text
    };

    fetch(url, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(result => {
        if (!result.ok) throw new Error(data.description)
    })
    .catch(error => {
        console.error("Ошибка Отправки сообщения:", error);
    });
}

// Функция ожидания запросов из Telegram
function listenForUpdates() {
    const url = `https://api.telegram.org/bot${BOT_TOKEN}/getUpdates`;

    fetch(url)
    .then(response => response.json())
    .then(data => {
        if (!data.ok) throw new Error(data.description)
        if (data.result.length > 0) {
            const botMessages = data.result.filter(r => 
                r.message?.entities &&
                r.message?.entities.length === 1 &&
                r.message?.entities[0].type === 'bot_command'
            );
            
            const lastMessage = botMessages[botMessages.length - 1]?.message;
            if (lastMessage && lastMessage.text) {
                if (!chatId) chatId = lastMessage.chat.id
                if (!lastKnownMessageId) lastKnownMessageId = lastMessage.message_id;
                else {
                    if (lastKnownMessageId === lastMessage.message_id) return;
                    else lastKnownMessageId = lastMessage.message_id
                }
                
                processCommand(lastMessage.text.split('@')[0]);
            }
        }
    })
    .catch(error => console.error("Ошибка получения данных:", error));

    setTimeout(listenForUpdates, 5000);
}

function setCommands() {
    const url = `https://api.telegram.org/bot${BOT_TOKEN}/setMyCommands`;

    const data = {
        commands: commands
    };

    fetch(url, {
        method: 'POST',
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(data => {
        if (!data.ok) throw new Error(data.description)
    })
    .catch(error => console.error("Ошибка назначения команд:", error));
}

function getChatAdministrators() {
    const url = `https://api.telegram.org/bot${BOT_TOKEN}/getChatAdministrators`;

    const data = {
        chat_id: chatId
    };

    return fetch(url, {
        method: 'POST',
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(data => {
        if (!data.ok) throw new Error(data.description)
        return data.result;
    })
    .catch(error => console.error("Ошибка получения администаторов:", error));
}

setCommands()
listenForUpdates();