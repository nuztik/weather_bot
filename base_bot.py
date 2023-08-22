import requests
import datetime
from config import TOKEN, API_W

from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor

bot = Bot(token=TOKEN)
db = Dispatcher(bot)

@db.message_handler(commands=['start'])
async def start_command(message: types.Message):
    await message.reply("Напиши мне название города, а я пришлю, какая там погода.")

@db.message_handler()
async def get_weather(message: types.Message):

    code_to_smile = {
        "Clear": "Ясно \U00002600",
        "Clouds": "Облачно \U00002601",
        "Rain": "Дождь \U00002614",
        "Drizzle": "Дождь \U00002614",
        "Thunderstorm": "Гроза \U000026C8",
        "Snow": "Снег \U0001F328",
        "Mist": "Туман \U0001F32B"

    }

    try:
        r = requests.get(f"https://api.openweathermap.org/data/2.5/weather?q={message.text}&appid={API_W}&units=metric&lang=ru")
        data = r.json()


        city = data['name']
        temp = data['main']['temp']

        weather_descrition = data['weather'][0]['main']
        if weather_descrition in code_to_smile:
            wd = code_to_smile[weather_descrition]
        else:
            wd = 'Посмотри в окно, я не могу определиться'

        humidity = data['main']['humidity']
        wind = data['wind']['speed']
        sunrise_timestamp = datetime.datetime.fromtimestamp(data['sys']['sunrise'])
        sunset_timestamp = datetime.datetime.fromtimestamp(data['sys']['sunset'])

        await message.reply(f'*** {datetime.datetime.now().strftime("%Y-%m-%d_%H:%M")} ***\n'
              f'Погода сейчас в городе: {city}\n Температура:{temp} С° {wd}\n'
              f'Влажность:{humidity}\n Скорость ветра:{wind} м/с\n'
              f'Восход солнца:{sunrise_timestamp}\n Закат солнца:{sunset_timestamp}\n'
                            f'***Хорошего дня***\n')

    except:
        await message.reply(' \U00002620 Такой город не найден, напишите другой. \U00002620')




if __name__ == '__main__':
    executor.start_polling(db)

