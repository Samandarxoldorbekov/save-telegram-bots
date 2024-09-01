# from telegram import Update , InlineKeyboardButton ,InlineKeyboardMarkup
# from 

# SPOTIFPY ORQALI


# from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
# from telegram.ext import CallbackContext
# import spotipy
# from spotipy.oauth2 import SpotifyClientCredentials
# from io import BytesIO
# import requests
# # Spotify API credentials
# sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id='fd08e8edd45c4dae8b373285b34f3fc3',
#                                                            client_secret='b28ccb3a487446cea96dbd8a75129ff5'))

# def create_buttons(tracks, offset):
#     buttons = []
#     for idx, track in enumerate(tracks[offset:offset+15]):
#         track_number = idx + 1 + offset
#         track_id = track['id']
#         buttons.append(InlineKeyboardButton(text=f"{track_number}", callback_data=f"track:{track_id}"))

#     # Pagination buttons
#     pagination_buttons = []
#     if offset > 0:
#         pagination_buttons.append(InlineKeyboardButton(text="⬅️ Orqaga", callback_data="prev_page"))
#     if len(tracks) > offset + 15:
#         pagination_buttons.append(InlineKeyboardButton(text="Oldinga ➡️", callback_data="next_page"))
    
#     # Creating inline keyboard markup
#     keyboard = [buttons[i:i+5] for i in range(0, len(buttons), 5)]  # Adjust to 5 buttons per row
#     if pagination_buttons:
#         keyboard.append(pagination_buttons)
    
#     return InlineKeyboardMarkup(keyboard)

# async def music_search(query: str, context: CallbackContext, chat_id: int) -> None:
#     results = sp.search(q=query, type='track', limit=50)
    
#     if results['tracks']['items']:
#         tracks = results['tracks']['items']
#         offset = 0
#         user_data = {'offset': offset, 'query': query}
#         context.chat_data.update(user_data)

#         # Create inline keyboard
#         builder = create_buttons(tracks, offset)
#         track_list = "\n".join([f"{idx + 1}. {track['artists'][0]['name']} - {track['name']}" for idx, track in enumerate(tracks[offset:offset+15])])
#         await context.bot.send_message(chat_id, f"Topilgan qo'shiqlar:\n{track_list}", reply_markup=builder)
#         context.chat_data['tracks'] = tracks
#     else:
#         await context.bot.send_message(chat_id, "Hech narsa topilmadi. Iltimos, yana urinib ko'ring.")

# async def download_song(update: Update, context: CallbackContext) -> None:
#     print("erore")
#     query = update.callback_query
#     # chat_id = update.update_id
#     track_id = query.data.split(':')[1]
    
#     # Fetch track details
#     track_info = sp.track(track_id)
#     track_name = track_info['name']
#     artist_name = track_info['artists'][0]['name']
#     preview_url = track_info.get('preview_url')  # Preview URL (short sample)
 
#     if preview_url:
#         response = requests.get(preview_url)
#         audio_content = BytesIO(response.content)
        
#         await context.bot.send_audio(
#             chat_id=update.effective_chat.id,
#             audio=audio_content,
#             title=track_name,
#             performer=artist_name,
#             caption=f"{track_name} - {artist_name}"
#         )
#     else:
#         await query.message.reply_text("Qo'shiqning previewi mavjud emas.")

# async def handle_pagination(update: Update, context: CallbackContext, direction: int) -> None:
#     chat_id = update.effective_chat.id
#     user_data = context.chat_data
#     tracks = user_data.get('tracks', [])
#     offset = user_data.get('offset', 0) + direction * 15

#     # Ensure the offset is within bounds
#     if offset < 0:
#         offset = 0
#     if offset >= len(tracks):
#         offset = (len(tracks) // 15) * 15

#     user_data['offset'] = offset
#     builder = create_buttons(tracks, offset)
#     track_list = "\n".join([f"{idx + 1}. {track['artists'][0]['name']} - {track['name']}" for idx, track in enumerate(tracks[offset:offset+15])])
    
#     try:
#         await update.callback_query.message.edit_text(f"Topilgan qo'shiqlar:\n{track_list}", reply_markup=builder)
#     except Exception as e:
#         await update.callback_query.message.reply_text(f"Xatolik yuz berdi: {str(e)}")
################################################################################################################################################################################
#  JAMENDO_CLIENT_ID  API ORQALI
# # from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
# # from telegram.ext import CallbackContext
# # import spotipy
# # from spotipy.oauth2 import SpotifyClientCredentials
# # from io import BytesIO
# # import yt_dlp
# # import asyncio
# # import requests
# # JAMENDO_CLIENT_ID = 'your_jamendo_client_id'

# # # Spotify API credentials
# # sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id='fd08e8edd45c4dae8b373285b34f3fc3', client_secret='b28ccb3a487446cea96dbd8a75129ff5'))

# # def create_buttons(tracks, offset):
# #     buttons = []
# #     for idx, track in enumerate(tracks[offset:offset+15]):
# #         track_number = idx + 1 + offset
# #         track_id = track['id']
# #         buttons.append(InlineKeyboardButton(text=f"{track_number}", callback_data=f"track:{track_id}"))

# #     pagination_buttons = []
# #     if offset > 0:
# #         pagination_buttons.append(InlineKeyboardButton(text="⬅️ Orqaga", callback_data="prev_page"))
# #     if len(tracks) > offset + 15:
# #         pagination_buttons.append(InlineKeyboardButton(text="Oldinga ➡️", callback_data="next_page"))

# #     keyboard = [buttons[i:i+5] for i in range(0, len(buttons), 5)]
# #     if pagination_buttons:
# #         keyboard.append(pagination_buttons)

# #     return InlineKeyboardMarkup(keyboard)

# # async def music_search(query: str, context: CallbackContext, chat_id: int) -> None:
# #     results = sp.search(q=query, type='track', limit=50)

# #     if results['tracks']['items']:
# #         tracks = results['tracks']['items']
# #         offset = 0
# #         user_data = {'offset': offset, 'query': query}
# #         context.chat_data.update(user_data)

# #         builder = create_buttons(tracks, offset)
# #         track_list = "\n".join([f"{idx + 1}. {track['artists'][0]['name']} - {track['name']}" for idx, track in enumerate(tracks[offset:offset+15])])
# #         await context.bot.send_message(chat_id, f"Topilgan qo'shiqlar:\n{track_list}", reply_markup=builder)
# #         context.chat_data['tracks'] = tracks
# #     else:
# #         await context.bot.send_message(chat_id, "Hech narsa topilmadi. Iltimos, yana urinib ko'ring.")

# # async def download_song(update: Update, context: CallbackContext) -> None:
# #     query = update.callback_query
# #     track_info = search_jamendo_track(query)

# #     if track_info:
# #         audio_url = track_info['audio_url']
# #         track_name = track_info['name']
# #         artist_name = track_info['artist']

# #         response = requests.get(audio_url)
# #         audio_file = BytesIO(response.content)

# #         await context.bot.send_audio(
# #             chat_id=update.effective_chat.id,
# #             audio=audio_file,
# #             title=track_name,
# #             performer=artist_name,
# #             caption=f"{track_name} - {artist_name}"
# #         )
# #     else:
# #         await query.message.reply_text("Qo'shiq topilmadi.")

# # async def handle_pagination(update: Update, context: CallbackContext, direction: int) -> None:
# #     chat_id = update.effective_chat.id
# #     user_data = context.chat_data
# #     tracks = user_data.get('tracks', [])
# #     offset = user_data.get('offset', 0) + direction * 15

# #     if offset < 0:
# #         offset = 0
# #     if offset >= len(tracks):
# #         offset = (len(tracks) // 15) * 15

# #     user_data['offset'] = offset
# #     builder = create_buttons(tracks, offset)
# #     track_list = "\n".join([f"{idx + 1}. {track['artists'][0]['name']} - {track['name']}" for idx, track in enumerate(tracks[offset:offset+15])])
    
# #     try:
# #         await update.callback_query.message.edit_text(f"Topilgan qo'shiqlar:\n{track_list}", reply_markup=builder)
# #     except Exception as e:
# #         await update.callback_query.message.reply_text(f"Xatolik yuz berdi: {str(e)}")
#########################################################################################################################################################
# PYTUBE KUTUBXONASI ORQALI
# from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
# from telegram.ext import CallbackContext
# from pytube import Search, YouTube
# from io import BytesIO

# def create_buttons(videos, offset):
#     buttons = []
#     for idx, video in enumerate(videos[offset:offset+15]):
#         video_number = idx + 1 + offset
#         video_id = video.video_id
#         buttons.append(InlineKeyboardButton(text=f"{video_number}", callback_data=f"video:{video_id}"))

#     # Pagination buttons
#     pagination_buttons = []
#     if offset > 0:
#         pagination_buttons.append(InlineKeyboardButton(text="⬅️ Orqaga", callback_data="prev_page"))
#     if len(videos) > offset + 15:
#         pagination_buttons.append(InlineKeyboardButton(text="Oldinga ➡️", callback_data="next_page"))
    
#     # Creating inline keyboard markup
#     keyboard = [buttons[i:i+5] for i in range(0, len(buttons), 5)]  # Adjust to 5 buttons per row
#     if pagination_buttons:
#         keyboard.append(pagination_buttons)
    
#     return InlineKeyboardMarkup(keyboard)

# async def music_search(query: str, context: CallbackContext, chat_id: int) -> None:
#     search = Search(query)
#     videos = search.results  # Fetch the first 50 results
    
#     if videos:
#         offset = 0
#         user_data = {'offset': offset, 'query': query}
#         context.chat_data.update(user_data)

#         # Create inline keyboard
#         builder = create_buttons(videos, offset)
#         video_list = "\n".join([f"{idx + 1}. {video.title}" for idx, video in enumerate(videos[offset:offset+15])])
#         await context.bot.send_message(chat_id, f"Topilgan qo'shiqlar:\n{video_list}", reply_markup=builder)
#         context.chat_data['videos'] = videos
#     else:
#         await context.bot.send_message(chat_id, "Hech narsa topilmadi. Iltimos, yana urinib ko'ring.")

# async def download_song(update: Update, context: CallbackContext) -> None:
#     query = update.callback_query
#     video_id = query.data.split(':')[1]

#     try:
#         # Fetch video details
#         video = YouTube(f"https://www.youtube.com/watch?v={video_id}")
#         print (video)
#         audio_stream = video.streams.filter(only_audio=True).first()

#         if not audio_stream:
#             await query.message.reply_text("Audio stream not available for this video.")
#             return

#         # Download the audio stream to a BytesIO object
#         audio_file = BytesIO()
#         audio_stream.stream_to_buffer(audio_file)
#         audio_file.seek(0)  # Reset the buffer position to the beginning

#         # Send the audio file via Telegram
#         await context.bot.send_audio(
#             chat_id=update.effective_chat.id,
#             audio=audio_file,
#             title=video.title,
#             performer=video.author,
#             caption=f"{video.title} - {video.author}"
#         )

#     except Exception as e:
#         await query.message.reply_text(f"Error downloading the audio: {str(e)}")



# async def handle_pagination(update: Update, context: CallbackContext, direction: int) -> None:
#     chat_id = update.effective_chat.id
#     user_data = context.chat_data
#     videos = user_data.get('videos', [])
#     offset = user_data.get('offset', 0) + direction * 15

#     # Ensure the offset is within bounds
#     if offset < 0:
#         offset = 0
#     if offset >= len(videos):
#         offset = (len(videos) // 15) * 15

#     user_data['offset'] = offset
#     builder = create_buttons(videos, offset)
#     video_list = "\n".join([f"{idx + 1}. {video.title}" for idx, video in enumerate(videos[offset:offset+15])])
    
#     try:
#         await update.callback_query.message.edit_text(f"Topilgan qo'shiqlar:\n{video_list}", reply_markup=builder)
#     except Exception as e:
#         await update.callback_query.message.reply_text(f"Xatolik yuz berdi: {str(e)}")
############################################################################################################################################################################
# YT-DLB KUTUBXONASI ORQALI
# from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
# from telegram.ext import CallbackContext
# from yt_dlp import YoutubeDL
# from io import BytesIO

# def create_buttons(videos, offset):
#     buttons = []
#     for idx, video in enumerate(videos[offset:offset+15]):
#         video_number = idx + 1 + offset
#         video_id = video['id']
#         buttons.append(InlineKeyboardButton(text=f"{video_number}", callback_data=f"video:{video_id}"))

#     # Pagination buttons
#     pagination_buttons = []
#     if offset > 0:
#         pagination_buttons.append(InlineKeyboardButton(text="⬅️ Orqaga", callback_data="prev_page"))
#     if len(videos) > offset + 15:
#         pagination_buttons.append(InlineKeyboardButton(text="Oldinga ➡️", callback_data="next_page"))
    
#     # Creating inline keyboard markup
#     keyboard = [buttons[i:i+5] for i in range(0, len(buttons), 5)]  # Adjust to 5 buttons per row
#     if pagination_buttons:
#         keyboard.append(pagination_buttons)
    
#     return InlineKeyboardMarkup(keyboard)

# async def music_search(query: str, context: CallbackContext, chat_id: int) -> None:
#     ydl_opts = {
#         'format': 'bestaudio/best',
#         'noplaylist': True,
#         'quiet': True,
#     }
#     with YoutubeDL(ydl_opts) as ydl:
#         search_result = ydl.extract_info(f"ytsearch15:{query}", download=False)
#         videos = search_result['entries']
    
#     if videos:
#         offset = 0
#         user_data = {'offset': offset, 'query': query, 'videos': videos}
#         context.chat_data.update(user_data)

#         # Create inline keyboard
#         builder = create_buttons(videos, offset)
#         video_list = "\n".join([f"{idx + 1}. {video['title']}" for idx, video in enumerate(videos[offset:offset+15])])
#         await context.bot.send_message(chat_id, f"Topilgan qo'shiqlar:\n{video_list}", reply_markup=builder)
#     else:
#         await context.bot.send_message(chat_id, "Hech narsa topilmadi. Iltimos, yana urinib ko'ring.")

# async def download_song(update: Update, context: CallbackContext) -> None:
#     print("eror")
#     query = update.callback_query
#     video_id = query.data.split(':')[1]
#     video_url = f"https://www.youtube.com/watch?v={video_id}"

#     try:
#         ydl_opts = {
#             'format': 'bestaudio/best',
#             'noplaylist': True,
#             'quiet': True,
#         }
#         with YoutubeDL(ydl_opts) as ydl:
#             info_dict = ydl.extract_info(video_url, download=False)
#             audio_url = info_dict['url']
#             audio_file = BytesIO(ydl.urlopen(audio_url).read())

#         # Send the audio file via Telegram
#         await context.bot.send_audio(
#             chat_id=update.effective_chat.id,
#             audio=audio_file,
#             title=info_dict['title'],
#             performer=info_dict['uploader'],
#             caption=f"{info_dict['title']} - {info_dict['uploader']}"
#         )

#     except Exception as e:
#         await query.message.reply_text(f"Error downloading the audio: {str(e)}")

# async def handle_pagination(update: Update, context: CallbackContext, direction: int) -> None:
#     chat_id = update.effective_chat.id
#     user_data = context.chat_data
#     videos = user_data.get('videos', [])
#     offset = user_data.get('offset', 0) + direction * 15

#     # Ensure the offset is within bounds
#     if offset < 0:
#         offset = 0
#     if offset >= len(videos):
#         offset = (len(videos) // 15) * 15

#     user_data['offset'] = offset
#     builder = create_buttons(videos, offset)
#     video_list = "\n".join([f"{idx + 1}. {video['title']}" for idx, video in enumerate(videos[offset:offset+15])])
    
#     try:
#         await update.callback_query.message.edit_text(f"Topilgan qo'shiqlar:\n{video_list}", reply_markup=builder)
#     except Exception as e:
#         await update.callback_query.message.reply_text(f"Xatolik yuz berdi: {str(e)}")

##############################################################################################################################################


from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, MessageHandler, Filters, CallbackContext
import yt_dlp

# Function to perform the search
def search_yt(query):
    ydl_opts = {
        'format': 'bestaudio/best',
        'noplaylist': True,
        'quiet': True,
        'extract_flat': 'in_playlist',
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        results = ydl.extract_info(f"ytsearch50:{query}", download=False)
    return results['entries']

# Function to format the results and generate inline keyboard buttons
def format_results(results, page=1, per_page=10):
    start = (page - 1) * per_page
    end = start + per_page
    sliced_results = results[start:end]

    buttons = [
        [InlineKeyboardButton(f"{i + 1}. {entry['title']}", callback_data=f"play_{entry['id']}")]
        for i, entry in enumerate(sliced_results)
    ]
    
    navigation_buttons = []
    if page > 1:
        navigation_buttons.append(InlineKeyboardButton("⬅️ Previous", callback_data=f"page_{page - 1}"))
    if end < len(results):
        navigation_buttons.append(InlineKeyboardButton("Next ➡️", callback_data=f"page_{page + 1}"))
    
    buttons.append(navigation_buttons)
    return InlineKeyboardMarkup(buttons)

# Handler for incoming messages
def search(update: Update, context: CallbackContext):
    query = update.message.text
    context.user_data['results'] = search_yt(query)
    context.user_data['page'] = 1
    update.message.reply_text(
        "🔍 Searching...",
        reply_markup=format_results(context.user_data['results'], page=1)
    )

# Handler for pagination
def paginate(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()
    
    if query.data.startswith('page_'):
        page = int(query.data.split('_')[1])
        context.user_data['page'] = page
        query.edit_message_reply_markup(
            reply_markup=format_results(context.user_data['results'], page=page)
        )
    # Add more handling if necessary (e.g., for playing the selected item)

# Main function to start the bot
def main():
    updater = Updater("YOUR TELEGRAM BOT TOKEN", use_context=True)
    dp = updater.dispatcher

    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, search))
    dp.add_handler(CallbackQueryHandler(paginate))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
