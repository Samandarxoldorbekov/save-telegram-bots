from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext
from io import BytesIO
import yt_dlp

def create_buttons(tracks, offset):
    buttons = []
    for idx, track in enumerate(tracks[offset:offset+15]):
        track_number = idx + 1
        track_id = track['id']
        buttons.append(InlineKeyboardButton(text=f"{track_number}", callback_data=f"track:{track_id}"))

    # Pagination buttons
    pagination_buttons = []
    if offset > 0:
        pagination_buttons.append(InlineKeyboardButton(text="⬅️ Orqaga", callback_data="prev_page"))
    if len(tracks) > offset + 15:
        pagination_buttons.append(InlineKeyboardButton(text="Oldinga ➡️", callback_data="next_page"))

    # Creating inline keyboard markup
    keyboard = [buttons[i:i+5] for i in range(0, len(buttons), 5)]  # Adjust to 5 buttons per row
    if pagination_buttons:
        keyboard.append(pagination_buttons)

    return InlineKeyboardMarkup(keyboard)

async def music_search(query: str, context: CallbackContext, chat_id: int) -> None:
    print("qidirlmoqda")
    ydl_opts = {
        'format': 'bestaudio/best',
        'noplaylist': True,
        'quiet': True,
        'skip_download': True,
        'cookiefile': 'cookies.txt',  # Path to your cookies file
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
        'extractor-args': 'youtube:player-client=web',
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            search_results = ydl.extract_info(f"ytsearch50:{query}", download=False)['entries']

        tracks = []
        for result in search_results:
            track = {
                'id': result['id'],
                'title': result['title'],
                'artists': [{'name': result['uploader']}],
                'url': result['webpage_url']
            }
            tracks.append(track)

        context.chat_data['tracks'] = tracks
        context.chat_data['offset'] = 0

        # Create buttons for the first 15 tracks
        builder = create_buttons(tracks, 0)
        track_list = "\n".join([f"{idx + 1}. {track['artists'][0]['name']} - {track['title']}" for idx, track in enumerate(tracks[:15])])

        await context.bot.send_message(chat_id=chat_id, text=f"Topilgan qo'shiqlar:\n{track_list}", reply_markup=builder)
    except Exception as e:
        await context.bot.send_message(chat_id=chat_id, text=f"Qo'shiqlarni izlashda xatolik yuz berdi: {str(e)}")

async def download_song(update: Update, context: CallbackContext) -> None:
    print("saqlanmoqda")
    query = update.callback_query

    # Check if 'tracks' exists in chat_data
    if 'tracks' not in context.chat_data:
        await query.answer("Qo'shiq ro'yxati mavjud emas. Iltimos, avval qidiruvdan foydalaning.")
        return

    track_id = query.data.split(':')[1]

    # Find the track URL using the track_id
    track_url = next((track['url'] for track in context.chat_data['tracks'] if track['id'] == track_id), None)
    if not track_url:
        await query.answer("Qo'shiq topilmadi!")
        return

    ydl_opts = {
        'format': 'bestaudio/best',
        'quiet': True,
        'noplaylist': True,
        'outtmpl': '-',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'cookiefile': 'cookies.txt',  # Path to your cookies file
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
        'extractor-args': 'youtube:player-client=web',
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(track_url, download=False)
            audio_data = BytesIO()
            ydl.download([track_url])
            audio_data.seek(0)

        await context.bot.send_audio(chat_id=update.effective_chat.id, audio=audio_data, title=info_dict['title'])
    except Exception as e:
        await update.callback_query.message.reply_text(f"Qo'shiqni yuklashda xatolik yuz berdi: {str(e)}")

async def handle_pagination(update: Update, context: CallbackContext, direction: int) -> None:
    chat_id = update.effective_chat.id
    user_data = context.chat_data
    tracks = user_data.get('tracks', [])
    offset = user_data.get('offset', 0) + direction * 15

    # Ensure the offset is within bounds
    if offset < 0:
        offset = 0
    if offset >= len(tracks):
        offset = (len(tracks) // 15) * 15

    user_data['offset'] = offset
    builder = create_buttons(tracks, offset)
    track_list = "\n".join([f"{idx + 1}. {track['artists'][0]['name']} - {track['name']}" for idx, track in enumerate(tracks[offset:offset+15])])

    try:
        await update.callback_query.message.edit_text(f"Topilgan qo'shiqlar:\n{track_list}", reply_markup=builder)
    except Exception as e:
        await update.callback_query.message.reply_text(f"Xatolik yuz berdi: {str(e)}")
