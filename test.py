import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from config import TOKEN,  API_KEY
from weather import get_weather_info
from ip_external import get_external_ip
from aiogram.types import Message, FSInputFile
#from aiogram.utils import executor
from googletrans import Translator
import random
from gtts import gTTS
import os


# Инициализация бота и диспетчера
bot = Bot(token=TOKEN)
dp = Dispatcher()

# Получаем внешний IP один раз при запуске
ip = get_external_ip()

# Инициализируем переводчик
translator = Translator()

async def main():
    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()




@dp.message(CommandStart())
async def start(message: Message):
    await message.answer(f'Привет от бота, {message.from_user.full_name}')

@dp.message(Command(commands=['help']))
async def help(message: Message):
    await message.answer("Этот бот умеет выполнять команды:\n/start\n/help")

@dp.message(F.text == "что такое ИИ?")
async def aitext(message: Message):
    await message.answer('Искусственный интеллект — это свойство искусственных интеллектуальных систем выполнять творческие функции, которые традиционно считаются прерогативой человека; наука и технология создания интеллектуальных машин, особенно интеллектуальных компьютерных программ')

#Прописываем хендлер и варианты ответов:
@dp.message(F.photo)
async def react_photo(message: Message):
        list = ['Ого, какая фотка!', 'Непонятно, что это такое', 'Не отправляй мне такое больше']
        rand_answ = random.choice(list)
        await message.answer(rand_answ)
        await bot.download(message.photo[-1], destination=f'img/{message.photo[-1].file_id}.jpg')


@dp.message(Command('photo', prefix='&'))
async def photo(message: Message):
        list = ['https://content.onliner.by/news/original_size/53ddc2f05f38cfdaac5d30d288bd6edd.png',
                'https://i.pinimg.com/736x/8a/92/60/8a926073b4ec3b4b9bc800d12fb35bf0.jpg',
                'https://i.pinimg.com/736x/60/ae/db/60aedbb4fe2c297d0fd305fcebe68623.jpg'
        ]
        rand_photo = random.choice(list)
        await message.answer_photo(photo=rand_photo, caption='Это крутая картинка')

@dp.message(Command(commands=['weather']))
async def weather_command(message: Message):
    # Координаты Москвы
    lat = 55.7558
    lon = 37.6176

    # Получаем переводимую информацию о погоде
    weather_info = get_weather_info(API_KEY, lat, lon)

    # Отправляем сообщение пользователю
    await message.answer(weather_info)

@dp.message(Command(commands=['ip']))
async def ip_command(message: Message):
    await message.answer(f'Ваш внешний IP: {ip}')


@dp.message(Command(commands=['video']))
async def video(message: Message):
    await bot.send_chat_action(message.chat.id, 'upload_video')
    video = FSInputFile('tmp\\video.mp4')
    await bot.send_video(message.chat.id, video)


@dp.message(Command('audio'))
async def audio(message: Message):
    audio = FSInputFile('tmp\\sound2.mp3')
    await bot.send_audio(message.chat.id, audio)


@dp.message(Command('training'))
async def training(message: Message):
    training_list = [
        "Упражнение 1:\n 1. Кранчи(скручивания): 3 подхода по 15 - 20 повторений.\n",
        "Упражнение 2:\n 2. Подъём ног в висе: 3 подхода по 10 - 15 повторений.\n",
        "Упражнение 3:\n 3. Планка : 3 подхода.\n"
        "Упражнение 4:\n 4. Русский твист: Выполните 3 подхода по 15 - 20 повторений на каждую сторону.\n",
        "Упражнение 5:\n 5. Велосипед: Выполните 3 подхода по 15 - 20 повторений на каждую сторону.\n"
    ]
    rand_tr = random.choice(training_list)
    await message.answer(f"Это ваша мини тренировка на сегодня {rand_tr}")

    tts = gTTS(text=rand_tr, lang='ru')
    tts.save('trainingru.mp3')
    audio = FSInputFile ('trainingru.mp3')
    await bot.send_audio(message.chat.id, audio)
    os.remove('trainingru.mp3')

    tts = gTTS(text=rand_tr, lang='en')
    tts.save('trainingen.mp3')
    audio = FSInputFile('trainingen.mp3')
    await bot.send_audio(message.chat.id, audio)
    os.remove('trainingen.mp3')

    tts = gTTS(text=rand_tr, lang='it')
    tts.save('trainingit.ogg')
    audio = FSInputFile('trainingit.ogg')
    await bot.send_voice(chat_id=message.chat.id, voice=audio)
    os.remove('trainingit.ogg')
@dp.message()
async def start(message: Message):
    if message.text.lower() == 'test':
        await message.answer('Тестируем')


@dp.message_handler()
async def echo_or_translate(message: types.Message):
    if message.text.startswith('/'):
        # Если это команда, но она не распознана
        await message.reply("Unknown command.")
    else:
        # Переводим текст на английский
        translated_text = translator.translate(message.text, dest='en').text
        await message.reply(translated_text)

@dp.message()
async def start(message: Message):
    await message.send_copy(chat_id=message.chat.id)

if __name__ == "__main__":
    asyncio.run(main())
