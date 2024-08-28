import io
import instaloader
import requests
from telegram.ext import CallbackContext
import time
import random

async def download_instagram_video(url: str, context: CallbackContext, chat_id: int, proxy: str = None, session_file: str = 'session') -> None:
    buffer = io.BytesIO()
    
    # Initialize Instaloader with proxy if provided
    L = instaloader.Instaloader()
    if proxy:
        L.context.proxy = proxy
    
    # Load session from file (log in if not available)
    try:
        L.load_session_from_file(username=None, filename=session_file)
    except FileNotFoundError:
        await context.bot.send_message(chat_id=chat_id, text="Please provide a valid session file for authentication.")
        return

    try:
        # Validate and extract the shortcode from the URL
        shortcode = url.split('/')[-2]
        if not shortcode:
            raise ValueError("Invalid Instagram URL")
        
        # Fetch post metadata
        post = instaloader.Post.from_shortcode(L.context, shortcode)
        
        # Ensure the post has a video
        if not post.is_video:
            await context.bot.send_message(chat_id=chat_id, text="The provided post does not contain a video.")
            return

        video_url = post.video_url

        # Use requests to download the video
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
        response = requests.get(video_url, stream=True, headers=headers, proxies={'http': proxy, 'https': proxy} if proxy else None)
        
        for chunk in response.iter_content(chunk_size=1024):
            if chunk:
                buffer.write(chunk)
        
        buffer.seek(0)  # Rewind buffer to the beginning

        # Send the video to the user via Telegram bot
        await context.bot.send_video(chat_id=chat_id, video=buffer, supports_streaming=True)
    
    except instaloader.exceptions.ConnectionException as e:
        # Handle rate limits by retrying after a delay
        await context.bot.send_message(chat_id=chat_id, text="Instagram is rate limiting us. Retrying in a few minutes...")
        time.sleep(random.uniform(60, 180))  # Wait between 1 to 3 minutes before retrying
        await download_instagram_video(url, context, chat_id, proxy, session_file)

    except instaloader.exceptions.BadResponseException as e:
        # Handle cases where metadata fetching fails
        await context.bot.send_message(chat_id=chat_id, text="Failed to fetch post metadata. The post may be private, deleted, or the URL is incorrect.")
    
    except Exception as e:
        # Send an error message if something else goes wrong
        await context.bot.send_message(chat_id=chat_id, text=f'Xatolik yuz berdi: {str(e)}')

# Example usage with a proxy:
# await download_instagram_video("https://www.instagram.com/p/VIDEO_SHORTCODE/", context, chat_id, proxy="http://proxyserver:port", session_file="my_instagram_session")
