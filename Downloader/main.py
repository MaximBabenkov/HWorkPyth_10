from aiogram import*
from config import*
from pytube import YouTube
import os

bot = Bot(TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands = ['start'])
async def start_message(message: types.Message):
    chat_id = message.chat.id
    await bot.send_message(chat_id, 'Hello! I can download YouTube videos\n'
                            'Please send me your link:')
@dp.message_handler()
async def text_messsage(message: types.Message):
    chat_id = message.chat.id
    url = message.text
    film = YouTube(url)
    if message.text.startswith == 'https://www.youtube.com/' or 'https://youtu.be':
        await bot.send_message(chat_id, f"I'm beginning video upload: {film.title}\n"
                        f'from channel: {film.author} {film.channel_url}', parse_mode = 'HTML')
        await download_youtube_video(url, message, bot)
        await bot.send_message(chat_id, f"I'm beginning audio upload: {film.title}\n"
                        f'from channel: {film.author} {film.channel_url}', parse_mode = 'HTML')
        await download_youtube_audio(url, message, bot)

async def download_youtube_video(url, message, bot):
    film = YouTube(url)
    stream = film.streams.filter(progressive = True, file_extension = 'mp4')
    stream.get_highest_resolution().download(f'{message.chat.id}', f'{message.chat.id}_{film.title}')
    with open (f'{message.chat.id}/{message.chat.id}_{film.title}', 'rb') as video:
        await bot.send_video(message.chat.id, video, caption = 'Your video', parse_mode = 'HTML')
        os.remove(f'{message.chat.id}/{message.chat.id}_{film.title}')

async def download_youtube_audio(url, message, bot):
    film = YouTube(url)    
    film.streams.get_audio_only().download(filename = 'audio.mp3')
    with open ('audio.mp3', 'rb') as audio:
        await bot.send_audio(message.chat.id, audio, caption = 'Your audio', parse_mode = 'HTML')
        os.remove('audio.mp3')

if __name__ == '__main__':
    executor.start_polling(dp)

