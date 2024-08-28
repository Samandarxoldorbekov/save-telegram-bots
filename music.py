from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from io import BytesIO
import requests

# Spotify API credentials
sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id='fd08e8edd45c4dae8b373285b34f3fc3',
                                                           client_secret='b28ccb3a487446cea96dbd8a75129ff5'))

def create_buttons(tracks, offset):
    buttons = []
    for idx, track in enumerate(tracks[offset:offset+15]):
        track_number = idx + 1 + offset
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
    results = sp.search(q=query, type='track', limit=50)
    
    if results['tracks']['items']:
        tracks = results['tracks']['items']
        offset = 0
        user_data = {'offset': offset, 'query': query}
        context.chat_data.update(user_data)

        # Create inline keyboard
        builder = create_buttons(tracks, offset)
        track_list = "\n".join([f"{idx + 1}. {track['artists'][0]['name']} - {track['name']}" for idx, track in enumerate(tracks[offset:offset+15])])
        await context.bot.send_message(chat_id, f"Topilgan qo'shiqlar:\n{track_list}", reply_markup=builder)
        context.chat_data['tracks'] = tracks
    else:
        await context.bot.send_message(chat_id, "Hech narsa topilmadi. Iltimos, yana urinib ko'ring.")

async def download_song(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    track_id = query.data.split(':')[1]
    
    # Fetch track details
    track_info = sp.track(track_id)
    track_name = track_info['name']
    artist_name = track_info['artists'][0]['name']
    preview_url = track_info.get('preview_url')  # Preview URL (short sample)

    if preview_url:
        response = requests.get(preview_url)
        audio_content = BytesIO(response.content)
        
        await context.bot.send_audio(
            chat_id=update.effective_chat.id,
            audio=audio_content,
            title=track_name,
            performer=artist_name,
            caption=f"{track_name} - {artist_name}"
        )
    else:
        await query.message.reply_text("Qo'shiqning previewi mavjud emas.")

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
