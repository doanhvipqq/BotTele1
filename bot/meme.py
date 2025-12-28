import random
import logging
import requests
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)

def register_meme(bot):
    """Register meme command handler"""
    
    @bot.message_handler(commands=['meme'])
    def handle_meme(message):
        """Send random meme image"""
        try:
            logger.info(f"User {message.from_user.id} requested meme")
            
            # Send loading message
            status_msg = bot.reply_to(message, "🎨 Đang tìm meme vui nhộn...")
            
            # Try to fetch meme
            meme_url = fetch_meme()
            
            # Delete loading message
            try:
                bot.delete_message(message.chat.id, status_msg.message_id)
            except:
                pass
            
            if meme_url:
                try:
                    bot.send_animation(
                        message.chat.id,
                        meme_url,
                        caption="<b>😂 Meme ngẫu nhiên</b>\n\n<i>✨ Chúc bạn cười thật vui!</i>",
                        reply_to_message_id=message.message_id
                    )
                    logger.info(f"Successfully sent meme to user {message.from_user.id}")
                except Exception as e:
                    logger.error(f"Failed to send meme: {e}")
                    bot.reply_to(
                        message,
                        "⚠️ Không thể gửi meme. Vui lòng thử lại!"
                    )
            else:
                bot.reply_to(
                    message,
                    "❌ Không tìm thấy meme.\n\n"
                    "<i>Vui lòng thử lại sau vài giây.</i>"
                )
                
        except Exception as e:
            logger.error(f"Error in meme command: {e}", exc_info=True)
            bot.reply_to(
                message,
                "❌ Có lỗi xảy ra khi tìm meme. Vui lòng thử lại!"
            )

def fetch_meme():
    """Fetch random meme from source"""
    try:
        page = random.randint(1, 50)
        url = f"https://www.aigei.com/s?q=meme&dim=gif-picture_2&page={page}"
        headers = {
            "Referer": url,
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        }

        response = requests.get(url, headers=headers, timeout=15)
        
        if response.status_code != 200:
            logger.warning(f"Meme source returned status {response.status_code}")
            return None
            
        soup = BeautifulSoup(response.text, "html.parser")
        img_tags = soup.find_all("img", src=True)
        img_urls = []

        for tag in img_tags:
            img_url = tag.get("src", "")
            if img_url.startswith("//s1.aigei.com"):
                full_url = "https:" + img_url
                img_urls.append(full_url)

        if not img_urls:
            logger.warning("No meme images found on page")
            return None

        selected_url = random.choice(img_urls)
        logger.info(f"Found {len(img_urls)} memes, selected one")
        return selected_url

    except requests.Timeout:
        logger.error("Meme request timed out")
        return None
    except requests.RequestException as e:
        logger.error(f"Request error while fetching meme: {e}")
        return None
    except Exception as e:
        logger.error(f"Unexpected error fetching meme: {e}")
        return None
