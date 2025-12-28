import time
import random
import logging
from datetime import timedelta

logger = logging.getLogger(__name__)

start_time = time.time()
file_url_video = "bot/url/anime.txt"

def get_uptime():
    """Calculate bot uptime in human-readable format"""
    uptime_seconds = int(time.time() - start_time)
    days = uptime_seconds // 86400
    hours = (uptime_seconds % 86400) // 3600
    minutes = (uptime_seconds % 3600) // 60
    seconds = uptime_seconds % 60
    
    parts = []
    if days > 0:
        parts.append(f"{days} ngày")
    if hours > 0:
        parts.append(f"{hours} giờ")
    if minutes > 0:
        parts.append(f"{minutes} phút")
    if seconds > 0 or not parts:
        parts.append(f"{seconds} giây")
    
    return ", ".join(parts)

def get_video():
    """Get random anime video URL from file"""
    try:
        with open(file_url_video, "r", encoding="utf-8") as file:
            video_urls = [line.strip() for line in file if line.strip()]
        
        if not video_urls:
            logger.warning(f"No videos found in {file_url_video}")
            return None

        return random.choice(video_urls)
    except FileNotFoundError:
        logger.error(f"Video file not found: {file_url_video}")
        return None
    except Exception as e:
        logger.error(f"Error loading video: {e}")
        return None

def register_time(bot):
    """Register time command handler"""
    
    @bot.message_handler(commands=['time'])
    def send_time(message):
        """Display bot uptime with anime video"""
        try:
            uptime = get_uptime()
            uptime_seconds = int(time.time() - start_time)
            
            # Beautiful formatted caption
            caption = f"""
<b>⏰ Thời gian hoạt động Bot</b>

<blockquote expandable>
╭─────────────────────╮
│ <b>🕐 Uptime:</b> {uptime}
│ <b>⚡ Total:</b> {uptime_seconds:,} giây
│ <b>🚀 Status:</b> Online
╰─────────────────────╯
</blockquote>

<i>✨ Bot đang chạy ổn định!</i>
"""
            
            video_url = get_video()
            
            if video_url:
                try:
                    bot.send_video(
                        message.chat.id,
                        video_url,
                        caption=caption.strip(),
                        reply_to_message_id=message.message_id
                    )
                    logger.info(f"Sent uptime with video to user {message.from_user.id}")
                except Exception as e:
                    logger.error(f"Failed to send video: {e}")
                    # Fallback to text only
                    bot.reply_to(message, caption.strip())
            else:
                # No video available, send text only
                bot.reply_to(message, caption.strip())
                logger.info(f"Sent uptime (text only) to user {message.from_user.id}")
                
        except Exception as e:
            logger.error(f"Error in time command: {e}", exc_info=True)
            bot.reply_to(
                message,
                "⚠️ Có lỗi xảy ra khi lấy thông tin thời gian. Vui lòng thử lại sau!"
            )
