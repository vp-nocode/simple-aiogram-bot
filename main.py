import asyncio
import os
from aiogram import Bot, Dispatcher, types, F
from aiogram.types import Message, FSInputFile
from aiogram.filters import CommandStart, Command
from config import TOKEN
from googletrans import Translator
from gtts import gTTS

bot = Bot(token=TOKEN)
dp = Dispatcher()

translator = Translator()

if not os.path.exists('img'):
    os.makedirs('img')

async def main():
    await dp.start_polling(bot)

@dp.message(CommandStart())
async def start(message: Message):
    await message.answer(f"Привет, {message.from_user.first_name} ({message.from_user.full_name}), я бот-переводчик!\n Набери любой текст и я переведу его на английский и озвучу!")

@dp.message(Command('help'))
async def command_help(message: Message):
    # await message.answer("This bot can execute the commands:\n /start\n /help")
    await message.answer("Этот бот может выполнять команды:\n /start\n /help\n а также переводить текст на английский и определять размер фотографий")

@dp.message(F.photo)
async def handle_photo(message: Message):

    photo_file = message.photo[-1]
    file_path = f'img/{photo_file.file_id}.jpg'
    await bot.download(photo_file, destination=file_path)

    file_size = os.path.getsize(file_path)
    await message.reply(f'Photo saved. Size: {file_size / 1024:.2f} KB')

@dp.message()
async def handle_text(message: types.Message):
    # translate to English
    translated = translator.translate(text=message.text, src='ru', dest='en')
    translated_text = translated.text

    # Sending translated text
    await message.reply(f"Translate: {translated_text}")

    # text to speech conversion and sending
    tts = gTTS(translated_text, lang='en')
    audio_file_name = "translated_audio.mp3"
    tts.save(audio_file_name)
    audio_file = FSInputFile(audio_file_name)
    await message.reply_voice(audio_file)
    os.remove(audio_file_name)

if __name__ == "__main__":
    asyncio.run(main())
