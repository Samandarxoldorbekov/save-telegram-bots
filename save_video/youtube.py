import io
import yt_dlp
from telegram.ext import CallbackContext

async def download_youtube_video(url: str, context: CallbackContext, chat_id: int) -> None:
    buffer = io.BytesIO()
    
    ydl_opts = {
        'format': '18',  # Use format code for 360p mp4
        'noplaylist': True,
        'quiet': True,
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',  # Set a more typical user agent
        'extractor-args': 'youtube:player-client=web',  # Force player client to web
        'cookiefile': '/path/to/your/cookies.txt'  # Add a path to cookies if available to bypass bot detection
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
