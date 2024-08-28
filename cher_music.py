# import logging
# from aiogram import Bot, Dispatcher, types
# from aiogram.filters import Command
# from aiogram.fsm.state import State, StatesGroup
# from aiogram.fsm.context import FSMContext
# from aiogram.fsm.storage.memory import MemoryStorage
# from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
# from aiogram.utils.keyboard import InlineKeyboardBuilder
# from spotipy import Spotify
# from spotipy.oauth2 import SpotifyClientCredentials
# import os

# API_TOKEN = '7452238296:AAFnS1SfDT4P-27sZFa2Xoeua3eI3X5NwRQ'
# SPOTIFY_CLIENT_ID = 'fd08e8edd45c4dae8b373285b34f3fc3'
# SPOTIFY_CLIENT_SECRET = 'b28ccb3a487446cea96dbd8a75129ff5'

# # Bot va dispatcher o'rnatilishi
# logging.basicConfig(level=logging.INFO)
# bot = Bot(token=API_TOKEN)
# dp = Dispatcher(storage=MemoryStorage())

# # Spotify'ga ulanish
# sp = Spotify(auth_manager=SpotifyClientCredentials(client_id=SPOTIFY_CLIENT_ID, client_secret=SPOTIFY_CLIENT_SECRET))

# # State Machine uchun klass
# class SearchState(StatesGroup):
#     waiting_for_song_choice = State()
#     waiting_for_song_page = State()

# # /start komandasi
# @dp.message(Command("start"))
# async def start_command(message: types.Message):
#     await message.answer("Assalomu alaykum! Qaysi qo'shiqni qidiryapsiz? Qo'shiq yoki ijrochi nomini yuboring.")

# # Musiqa yoki ijrochi nomi bo'yicha Spotify'dan qidirish
# @dp.message()
# async def search_song(message: types.Message, state: FSMContext):
#     query = message.text
#     results = sp.search(q=query, type='track', limit=50)
    
#     if results['tracks']['items']:
#         tracks = results['tracks']['items']
#         user_data = {'offset': 0, 'query': query}
#         await state.set_data(user_data)

#         def create_buttons(tracks, offset):
#             builder = InlineKeyboardBuilder()
#             for idx, track in enumerate(tracks[offset:offset+15]):
#                 track_id = track['id']
#                 builder.button(text=f"{idx+1}", callback_data=f"track:{track_id}")
            
#             # Pagination buttons
#             if offset > 0:
#                 builder.button(text="Orqaga", callback_data="prev_page")
#             if len(tracks) > offset + 15:
#                 builder.button(text="Oldinga", callback_data="next_page")
            
#             # Adjust to 5 buttons per row
#             builder.adjust(5)
            
#             return builder

#         # Yangi sahifa yaratish
#         offset = 0
#         builder = create_buttons(tracks, offset)
#         track_list = "\n".join([f"{idx+1}. {track['artists'][0]['name']} - {track['name']} ({track['album']['name']}, {track['album']['release_date']})" for idx, track in enumerate(tracks[offset:offset+15])])
#         await message.answer(f"Topilgan qo'shiqlar:\n{track_list}", reply_markup=builder.as_markup())
#         await state.set_state(SearchState.waiting_for_song_page)
#     else:
#         await message.answer("Hech narsa topilmadi. Iltimos, yana urinib ko'ring.")

# # Foydalanuvchi qo'shiqni tanlaganda yoki sahifa tugmalariga bosilganda
# @dp.callback_query(SearchState.waiting_for_song_page)
# async def handle_song_choice_or_pagination(callback: types.CallbackQuery, state: FSMContext):
#     data = callback.data
#     user_data = await state.get_data()
#     query = user_data.get('query', '')
#     offset = user_data.get('offset', 0)
    
#     results = sp.search(q=query, type='track', limit=50)
#     tracks = results['tracks']['items']

#     if data == "prev_page":
#         offset = max(0, offset - 15)
#     elif data == "next_page":
#         offset = min(len(tracks) - 15, offset + 15)
#     elif data.startswith("track:"):
#         track_id = data.split(":")[1]
#         track = sp.track(track_id)
#         track_name = track['name']
#         artist_name = track['artists'][0]['name']

#         await callback.message.answer(f"'{artist_name} - {track_name}' qo'shig'i tanlandi.")
#         await state.clear()
#         return artist_name , track_name

#     builder = create_buttons(tracks, offset)
#     track_list = "\n".join([f"{idx+1}. {track['artists'][0]['name']} - {track['name']} ({track['album']['name']}, {track['album']['release_date']})" for idx, track in enumerate(tracks[offset:offset+15])])
#     await callback.message.edit_text(f"Topilgan qo'shiqlar:\n{track_list}", reply_markup=builder.as_markup())
#     await state.update_data(offset=offset)
    
    
# def create_buttons(tracks, offset):
#     builder = InlineKeyboardBuilder()
#     for idx, track in enumerate(tracks[offset:offset+15]):
#         track_id = track['id']
#         builder.button(text=f"{idx+1}", callback_data=f"track:{track_id}")
    
#     # Pagination buttons
#     if offset > 0:
#         builder.button(text="Orqaga", callback_data="prev_page")
#     if len(tracks) > offset + 15:
#         builder.button(text="Oldinga", callback_data="next_page")
    
#     # Adjust to 5 buttons per row
#     builder.adjust(5)
    
#     return builder

# # Botni ishga tushirish
# async def main():
#     await dp.start_polling(bot)

# if __name__ == "__main__":
#     import asyncio
#     asyncio.run(main())
