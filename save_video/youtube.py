import io
import yt_dlp
# from telegram import Bot
from telegram.ext import CallbackContext

async def download_youtube_video(url: str, context: CallbackContext, chat_id: int) -> None:
    buffer = io.BytesIO()
    
    ydl_opts = {
        'format': '18',  # Use format code for 360p mp4
        'noplaylist': True,
        'quiet': True,
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=False)
            video_url = info_dict['url']
            
            response = ydl.urlopen(video_url)
            while True:
                chunk = response.read(1024)
                if not chunk:
                    break
                buffer.write(chunk)
        
        buffer.seek(0)  # Rewind buffer to the beginning

        await context.bot.send_video(chat_id=chat_id, video=buffer, supports_streaming=True)
    except Exception as e:
        await context.bot.send_message(chat_id=chat_id, text=f'Xatolik yuz berdi: {str(e)}')
