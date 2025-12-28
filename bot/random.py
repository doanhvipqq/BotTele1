import random
import logging

logger = logging.getLogger(__name__)

MAX_ATTEMPTS = 5

def send_random_media(bot, message, file_path, media_type, command_name):
    """Send random media from file with retry logic"""
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            urls = [line.strip() for line in file if line.strip()]
    except FileNotFoundError:
        logger.error(f"File not found: {file_path}")
        return bot.reply_to(
            message,
            f"❌ File dữ liệu không tồn tại: <code>{file_path}</code>"
        )
    except Exception as e:
        logger.error(f"Error reading file {file_path}: {e}")
        return bot.reply_to(
            message,
            "❌ Không thể đọc dữ liệu. Vui lòng thử lại sau!"
        )

    if not urls:
        logger.warning(f"No URLs found in {file_path}")
        return bot.reply_to(
            message,
            "⚠️ Danh sách chưa có dữ liệu. Vui lòng thử lại sau!"
        )

    # Shuffle for randomness
    random.shuffle(urls)

    # Get appropriate send function
    send_func = {
        "photo": bot.send_photo,
        "video": bot.send_video,
        "animation": bot.send_animation,
    }.get(media_type)

    if not send_func:
        logger.error(f"Invalid media type: {media_type} for command /{command_name}")
        return bot.reply_to(
            message,
            "❌ Lỗi hệ thống. Vui lòng báo admin!"
        )

    # Try sending with retries
    for attempt, url in enumerate(urls[:MAX_ATTEMPTS], 1):
        try:
            # Beautiful captions per type
            captions = {
                "anime": "<b>🇯🇵 Video Anime ngẫu nhiên</b>\n\n<i>✨ Thưởng thức nhé!</i>",
                "girl": "<b>👧 Video Girl</b>\n\n<i>✨ Enjoy!</i>",
                "imganime": "<b>🎨 Ảnh Anime</b>",
                "squeeze": "<b>🤗 Reaction Squeeze</b>",
            }
            caption = captions.get(command_name, f"<b>✨ Random {media_type}</b>")
            
            send_func(
                message.chat.id,
                url,
                caption=caption,
                reply_to_message_id=message.message_id
            )
            logger.info(f"Successfully sent {media_type} for /{command_name} to user {message.from_user.id}")
            return
            
        except Exception as e:
            logger.warning(f"Failed to send {media_type} (attempt {attempt}/{MAX_ATTEMPTS}): {e}")
            continue

    # All attempts failed
    logger.error(f"All {MAX_ATTEMPTS} attempts failed for /{command_name}")
    bot.reply_to(
        message,
        "❌ Không thể gửi nội dung. Vui lòng thử lại sau!"
    )

# Command configurations
COMMANDS = {
    "anime": {
        "path": "bot/url/anime.txt",
        "type": "video"
    },
    "girl": {
        "path": "bot/url/girl.txt",
        "type": "video"
    },
    "imganime": {
        "path": "bot/url/imganime.txt",
        "type": "photo"
    },
    "squeeze": {
        "path": "bot/url/squeeze.txt",
        "type": "animation"
    }
}

def create_handler(bot, cmd_name, path, mtype):
    """Create command handler for specific media type"""
    def handler(message):
        logger.info(f"User {message.from_user.id} used /{cmd_name}")
        send_random_media(bot, message, path, mtype, cmd_name)
    return handler

def register_random(bot):
    """Register all random media command handlers"""
    for cmd, cfg in COMMANDS.items():
        handler = create_handler(bot, cmd, cfg["path"], cfg["type"])
        bot.register_message_handler(handler, commands=[cmd])
        logger.info(f"Registered command: /{cmd}")
