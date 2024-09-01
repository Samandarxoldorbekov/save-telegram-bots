import io
import instaloader
import requests
from telegram.ext import CallbackContext
from telegram import InputMediaPhoto, InputMediaVideo
import time
import random

async def download_instagram_media(url: str, context: CallbackContext, chat_id: int, proxy: str = None, session_file: str = 'session') -> None:
    L = instaloader.Instaloader()
    if proxy:
        L.context.proxy = proxy

    try:
        L.load_session_from_file(username=None, filename=session_file)
    except FileNotFoundError:
        await context.bot.send_message(chat_id=chat_id, text="Please provide a valid session file for authentication.")
        return

    try:
        shortcode = url.split('/')[-2]
        if not shortcode:
            raise ValueError("Invalid Instagram URL")

        post = instaloader.Post.from_shortcode(L.context, shortcode)

        media_group = []
        if post.typename == 'GraphSidecar':
            # Handle slideshow posts
            for node in post.get_sidecar_nodes():
                buffer = io.BytesIO()
                if node.is_video:
                    media_url = node.video_url
                    media_type = InputMediaVideo
                else:
                    media_url = node.display_url
                    media_type = InputMediaPhoto

                headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
                response = requests.get(media_url, stream=True, headers=headers, proxies={'http': proxy, 'https': proxy} if proxy else None)

                for chunk in response.iter_content(chunk_size=1024):
                    if chunk:
                        buffer.write(chunk)

                buffer.seek(0)
                media_group.append(media_type(buffer))

        else:
            # Handle single media (image or video) posts
            buffer = io.BytesIO()
            if post.is_video:
                media_url = post.video_url
                media_type = InputMediaVideo
            else:
                media_url = post.url
                media_type = InputMediaPhoto

            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
            response = requests.get(media_url, stream=True, headers=headers, proxies={'http': proxy, 'https': proxy} if proxy else None)

            for chunk in response.iter_content(chunk_size=1024):
                if chunk:
                    buffer.write(chunk)

            buffer.seek(0)
            media_group.append(media_type(buffer))
        texti = "kanalga obuna bo'lishni unutmang 😊 @samandarxoldorbekov"
        # Send the media as a group message
        if media_group:
            await context.bot.send_media_group(chat_id=chat_id, media=media_group,)
            await context.bot.send_message(chat_id=chat_id, text=texti)

    except instaloader.exceptions.ConnectionException:
        await context.bot.send_message(chat_id=chat_id, text="Instagram is rate limiting us. Retrying in a few minutes...")
        time.sleep(random.uniform(60, 180))
        await download_instagram_media(url, context, chat_id, proxy, session_file)

    except instaloader.exceptions.BadResponseException:
        await context.bot.send_message(chat_id=chat_id, text="Failed to fetch post metadata. The post may be private, deleted, or the URL is incorrect.")
    
    except Exception as e:
        await context.bot.send_message(chat_id=chat_id, text=f'An error occurred: {str(e)}')

