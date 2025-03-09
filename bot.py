import requests
import telebot
from time import sleep


# 🔹 Вставь свой токен Telegram-бота
BOT_TOKEN = "7583013904:AAH001Z6dqlb5NOO2GHbvLd-j-c40rSEf8o"
bot = telebot.TeleBot("7583013904:AAH001Z6dqlb5NOO2GHbvLd-j-c40rSEf8o")

# 🔹 Обработка команды /start
@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, "Привет! 🤖 Я запущен и буду присылать сигналы, когда зафиксирую крупные сделки!")

# 🔹 Запускаем бота
print("✅ Бот запущен и ждёт команду /start")
bot.polling()


# 🔹 Вставь свои API-ключи
ETHERSCAN_API_KEY = "V83MZB9H6I7GF7UY98S4GUP7CFETFXWKI1"
BOT_TOKEN = "7583013904:AAH001Z6dqlb5NOO2GHbvLd-j-c40rSEf8o"
CHAT_ID = "2097077728"  # Узнать можно через @userinfobot

# 🔹 Инициализация Telegram-бота
bot = telebot.TeleBot("7583013904:AAH001Z6dqlb5NOO2GHbvLd-j-c40rSEf8o")

# 🔹 Список кошельков китов
WHALE_ADDRESSES = ["0xEA674fdDe714fd979de3EdF0F56AA9716B898ec8"]

# 🔹 Функция для проверки транзакций
def get_whale_transactions():
    for address in WHALE_ADDRESSES:
        url = f"https://api.etherscan.io/api?module=account&action=txlist&address={address}&apikey={ETHERSCAN_API_KEY}"
        response = requests.get(url).json()

        if response["status"] == "1" and response["result"]:
            latest_tx = response["result"][0]  # Берём последнюю транзакцию
            value = int(latest_tx["value"]) / 10**18  # Переводим в ETH
            to_address = latest_tx["to"]
            tx_hash = latest_tx["hash"]

            # Если сумма больше 100 ETH, отправляем сигнал в Telegram
            if value > 100:
                message = f"🐳 **Крупная сделка кита!**\n" \
                          f"💰 **Сумма:** {value} ETH\n" \
                          f"📍 **Кошелёк:** {address}\n" \
                          f"➡ **Получатель:** {to_address}\n" \
                          f"🔗 [Смотреть в блокчейне](https://etherscan.io/tx/{tx_hash})"

                bot.send_message(CHAT_ID, message, parse_mode="Markdown")

# 🔹 Основной цикл (проверка раз в минуту)
while True:
    get_whale_transactions()
    sleep(60)
