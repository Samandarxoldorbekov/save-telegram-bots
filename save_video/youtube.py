# # import io
# # import yt_dlp
# # from telegram.ext import CallbackContext

# # async def download_youtube_video(url: str, context: CallbackContext, chat_id: int) -> None:
# #     buffer = io.BytesIO()
    
# #     ydl_opts = {
# #         'format': '18',  # Use format code for 360p mp4
# #         'noplaylist': True,
# #         'quiet': True,
# #         'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',  # Set a more typical user agent
# #         'extractor-args': 'youtube:player-client=web',  # Force player client to web
# #         'cookiefile': 'cookies.txt'  # Add a path to cookies if available to bypass bot detection
# #     }
    
# #     try:
# #         with yt_dlp.YoutubeDL(ydl_opts) as ydl:
# #             info_dict = ydl.extract_info(url, download=False)
# #             video_url = info_dict['url']
            
# #             response = ydl.urlopen(video_url)
# #             while True:
# #                 chunk = response.read(1024)
# #                 if not chunk:
# #                     break
# #                 buffer.write(chunk)
        
# #         buffer.seek(0)  # Rewind buffer to the beginning

# #         await context.bot.send_video(chat_id=chat_id, video=buffer, supports_streaming=True)
# #     except Exception as e:
# #         await context.bot.send_message(chat_id=chat_id, text=f'Xatolik yuz berdi: {str(e)}')
from cgitb import text
import io
import yt_dlp
import aiohttp
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import CallbackContext ,ContextTypes

async def download_youtube_video(choise_url, context: CallbackContext, chat_id) -> None:
    format_choice, url = choise_url.split('|')
    buffer = io.BytesIO()
    # await context.bot.send_message(chat_id=chat_id, text=f"Failed to download video, status code: {response.status}")
    loading_message = await context.bot.send_animation(chat_id=chat_id, animation=open('giflar/loader.gif', 'rb'))
    
    ydl_opts = {
        'format': 'bestaudio/best' if format_choice == 'audio' else '18',  # Audio or 360p mp4 video
        'noplaylist': True,
        'quiet': True,
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
        'extractor-args': 'youtube:player-client=web',
        'cookiefile': 'cookies.txt'  # Adjust this if you have a valid cookies file
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=False)
            video_url = info_dict['url']
            
            async with aiohttp.ClientSession() as session:
                async with session.get(video_url) as response:
                    if response.status == 200:
                        while True:
                            chunk = await response.content.read(1024)
                            if not chunk:
                                break
                            buffer.write(chunk)
                    else:
                        await context.bot.send_message(chat_id=chat_id, text=f"Failed to download video, status code: {response.status}")
                        return
        
        buffer.seek(0)  # Rewind buffer to the beginning
        
        if format_choice == 'audio_yourtube_':
            await context.bot.send_audio(chat_id=chat_id, audio=buffer)
            await context.bot.send_message(chat_id=chat_id, text="kanalimizga obuna bo'lishni untmang @xoldorbekovsamandar")
            await context.bot.delete_message(chat_id=chat_id, message_id=loading_message.message_id)
        else:
            await context.bot.send_video(chat_id=chat_id, video=buffer, supports_streaming=True)
            await context.bot.delete_message(chat_id=chat_id, message_id=loading_message.message_id)
    except Exception as e:
        await context.bot.send_message(chat_id=chat_id, text="Teleram cheklovlari sababli katta hajimdagi ma'lumotlarda olish imkonsiz 🥲")

async def ask_for_format_choice(url: str, context: CallbackContext, chat_id: int):
    print("format")
    keyboard = [
        [
            InlineKeyboardButton("Video 🎞", callback_data=f"video_youtube_|{url}"),
            InlineKeyboardButton("Audio 🎧", callback_data=f"audio_yourtube_|{url}")
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await context.bot.send_message(chat_id=chat_id, text="Qaysi formatda yuklab olishni xohlaysiz?", reply_markup=reply_markup)

async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print("chois")
    query = update.callback_query
    await query.answer()
    
    format_choice, url = query.data.split('|')
    chat_id = query.message.chat_id
    await download_youtube_video(url, context, chat_id, format_choice)

# Usage example
# await ask_for_format_choice(url='https://www.youtube.com/watch?v=example', context=context, chat_id=123456789)
