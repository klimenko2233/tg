import requests
from telebot import TeleBot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton

TOKEN = "7888012304:AAFnjC9Mez4qkPhas9j2-wHJA0viG9YLmLQ"
CRYPTO_NAME_TO_TICKER = {
"Bitcoin": "BTCUSDT",
"Ethereum": "ETHUSDT",
"Doge": "DOGEUSDT"
}

bot = TeleBot(TOKEN)

@bot.message_handler(commands=["start"])
def send_welcome(message):
    markup = ReplyKeyboardMarkup(row_width = 3)
    for crypto_name in CRYPTO_NAME_TO_TICKER.keys():
        item_button = KeyboardButton(crypto_name)
        markup.add(item_button)
    bot.send_message(message.chat.id, "Выбери монету)", reply_markup=markup)

@bot.message_handler(func=lambda message: message.text in CRYPTO_NAME_TO_TICKER.keys())
def send_price(message):
    crypto_name = message.text
    ticker = CRYPTO_NAME_TO_TICKER[crypto_name]
    price = get_price_by_ticker(ticker=ticker)
    bot.send_message(message.chat.id, f"Ценник на  {crypto_name}-{price} usdt")


def get_price_by_ticker(*, ticker: str):
    endpoint = "https://api.binance.com/api/v3/ticker/price"
    params = {
        'symbol': ticker,
    }
    response = requests.get(endpoint, params=params)
    data = response.json()
    price = round(float(data["price"]), 4)
    return price


bot.infinity_polling()