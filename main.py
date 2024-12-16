import telebot
import requests
import json


bot = telebot.TeleBot('7042484062:AAEvIZY1W2HcEevMMzoAz8lwx2kGxNPz_T0')
API = '4843135e9e0ed4b6e423e163843570d6'

@bot.message_handler(commands=['start'])
def main(message):
    bot.send_message(message.chat.id, f'Привет, {message.from_user.first_name}. Напиши название города!' )


@bot.message_handler(content_types=['text'])
def get_weather(message):
    city = message.text.strip().lower()
    res = requests.get(f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API}&units=metric')
    data = json.loads(res.text)
    bot.reply_to(message, f'Сейчас погода: {data["main"]["temp"]}')



bot.polling(non_stop=True)