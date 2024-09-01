from telegram import Update
from telegram.ext import CallbackContext
from save_video import youtube, instagram, tiktok
import music  # Importing the music_search module
import re

# Regular expression to identify a URL
url_pattern = re.compile(r'https?://[^\s]+')

async def start(update: Update, context: CallbackContext) -> None:
    user = update.message.from_user
    user_name = user.first_name
    await update.message.reply_text(f'Salom {user_name}! Link yuboring yoki qo\'shiq so\'rovini kiriting.')

async def check_link(update: Update, context: CallbackContext) -> None:
    text = update.message.text
    chat_id = update.effective_chat.id

    # Check if the message contains a URL
    if url_pattern.match(text):
        if "youtube.com" in text or "youtu.be" in text:
            # await update.message.reply_text('YouTubedan video saqlash amalga oshirilmoqda...')
            await youtube.ask_for_format_choice(text, context, chat_id)
        elif "instagram.com" in text:
            await update.message.reply_text('Instagramdan video saqlash amalga oshirilmoqda...')
            await instagram.download_instagram_media(text, context, chat_id)
        elif "tiktok.com" in text:
            await update.message.reply_text('TikTokdan video saqlash amalga oshirilmoqda...')
            await tiktok.download_tiktok_video(text, context, chat_id)
        else:
            await update.message.reply_text("Yaroqsiz link yubordingiz. Faqat YouTube, Instagram va TikTok linklarini qo‘llab-quvvatlaymiz.")
    else:
        # If the message is not a URL, assume it's a search query for music
        await update.message.reply_text('Qo\'shiq qidirilmoqda...')
        await music.music_search(text, context, chat_id)

async def button_handler(update: Update, context: CallbackContext) -> None:
    chat_id = update.effective_chat.id
    # chat_id = update.message.chat_id
    query = update.callback_query
    data = query.data
    await query.answer()  # Acknowledge the callback query
    
    if data.startswith("track:"):
        # Call download_song function from music.py
        await music.download_song(update, context)
    elif data == "prev_page":
        # Handle previous page
        await music.handle_pagination(update, context, -1)
    elif data == "next_page":
        # Handle next page
        await music.handle_pagination(update, context, 1)
    elif "video_youtube_" in data:
        await youtube.download_youtube_video(data, context, chat_id)
    elif "audio_yourtube_" in data:
        await youtube.download_youtube_video(data, context, chat_id)
