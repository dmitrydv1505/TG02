import asyncio
import os
import random
from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, FSInputFile
from config import TOKEN, API_KEY
from weather import get_weather_info
from ip_external import get_external_ip
from googletrans import Translator
from gtts import gTTS

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
async def help_command(message: Message):
    await message.answer("Этот бот умеет выполнять команды:\n/start\n/help\n/weather\n/ip\n/photo\n/audio\n/training")

@dp.message(F.text == "что такое ИИ?")
async def aitext(message: Message):
    await message.answer('Искусственный интеллект — это свойство искусственных интеллектуальных систем выполнять творческие функции, которые традиционно считаются прерогативой человека; наука и технология создания интеллектуальных машин, особенно интеллектуальных компьютерных программ')

@dp.message(F.photo)
async def react_photo(message: Message):
    responses = ['Ого, какая фотка!', 'Непонятно, что это такое', 'Не отправляй мне такое больше']
    rand_answ = random.choice(responses)
    await message.answer(rand_answ)
    file_path = os.path.join('tmp', f'{message.photo[-1].file_id}.jpg')
    await bot.download(message.photo[-1], destination=file_path)

@dp.message(Command('photo', prefix='&'))
async def send_photo(message: Message):
    photos = ['https://content.onliner.by/news/original_size/53ddc2f05f38cfdaac5d30d288bd6edd.png',
        'https://i.pinimg.com/736x/8a/92/60/8a926073b4ec3b4b9bc800d12fb35bf0.jpg',
        'https://i.pinimg.com/736x/60/ae/db/60aedbb4fe2c297d0fd305fcebe68623.jpg'
    ]
    rand_photo = random.choice(photos)
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
async def video_command(message: Message):
    await bot.send_chat_action(message.chat.id, 'upload_video')
    video = FSInputFile(os.path.join('tmp', 'video.mp4'))
    await bot.send_video(message.chat.id, video)

@dp.message(Command(commands=['audio']))
async def audio_command(message: Message):
    audio = FSInputFile(os.path.join('tmp', 'sound2.mp3'))
    await bot.send_audio(message.chat.id, audio)

@dp.message(Command(commands=['training']))
async def training_command(message: Message):
    training_list = [
        "Упражнение 1: Кранчи (скручивания): 3 подхода по 15 - 20 повторений.",
        "Упражнение 2: Подъём ног в висе: 3 подхода по 10 - 15 повторений.",
        "Упражнение 3: Планка: 3 подхода.",
        "Упражнение 4: Русский твист: Выполните 3 подхода по 15 - 20 повторений на каждую сторону.",
        "Упражнение 5: Велосипед: Выполните 3 подхода по 15 - 20 повторений на каждую сторону."
    ]
    rand_tr = random.choice(training_list)
    await message.answer(f"Это ваша мини тренировка на сегодня: {rand_tr}")

    tts = gTTS(text=rand_tr, lang='ru')
    audio_path = 'trainingru.mp3'
    tts.save(audio_path)
    audio = FSInputFile(audio_path)
    await bot.send_audio(message.chat.id, audio)
    os.remove(audio_path)

if __name__ == '__main__':
    asyncio.run(main())