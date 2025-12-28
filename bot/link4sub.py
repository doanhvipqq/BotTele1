import logging
import requests

logger = logging.getLogger(__name__)

def register_link4sub(bot):
    """Register link4sub command handler"""
    
    @bot.message_handler(commands=['link4sub'])
    def link4sub_handler(message):
        """Process Facebook link for sub"""
        try:
            # Parse command
            args = message.text.split()
            if len(args) < 2:
                bot.reply_to(
                    message,
                    "🚫 <b>Vui lòng cung cấp link Facebook!</b>\n\n"
                    "<i>Ví dụ:</i> <code>/link4sub https://facebook.com/...</code>"
                )
                return
            
            url = args[1].strip()
            logger.info(f"User {message.from_user.id} requested link4sub for: {url}")
            
            # Send processing message
            status_msg = bot.reply_to(message, "⏳ <b>Đang xử lý...</b>")
            
            try:
                # Call API
                api_url = "https://api-v1-amber.vercel.app/api/v1/link4sub"
                headers = {
                    "User-Agent": "Mozilla/5.0 (Linux; Android 12) AppleWebKit/537.36",
                    "Referer": "https://api-v1-amber.vercel.app/"
                }
                
                response = requests.get(api_url, headers=headers, params={"url": url}, timeout=15)
                data = response.json()
                
                # Process result
                if "data" in data and data["data"]:
                    result_link = data["data"].get("destination_url", "N/A")
                    
                    caption = f"""
<b>✅ Link4Sub - Thành công!</b>

<blockquote expandable>
╭─────────────────────────╮
│ <b>🔗 Link gốc:</b>
│ {url[:50] + '...' if len(url) > 50 else url}
├─────────────────────────┤
│ <b>✨ Link ra:</b>
│ {result_link}
╰─────────────────────────╯
</blockquote>

<i>📝 Copy link để sử dụng</i>
"""
                    
                    bot.edit_message_text(caption.strip(), message.chat.id, status_msg.message_id)
                    logger.info(f"Successfully processed link4sub for user {message.from_user.id}")
                    
                elif "error" in data:
                    bot.edit_message_text(
                        f"❌ <b>Lỗi:</b> {data['error']}\n\n<i>Vui lòng kiểm tra link!</i>",
                        message.chat.id,
                        status_msg.message_id
                    )
                else:
                    bot.edit_message_text(
                        "❌ <b>Lỗi không xác định</b>\n\n<i>Vui lòng thử lại!</i>",
                        message.chat.id,
                        status_msg.message_id
                    )
                    
            except requests.Timeout:
                logger.error("API timeout")
                bot.edit_message_text(
                    "⏱️ <b>Timeout!</b> API không phản hồi.",
                    message.chat.id,
                    status_msg.message_id
                )
            except Exception as e:
                logger.error(f"Error: {e}", exc_info=True)
                bot.edit_message_text(
                    "❌ <b>Có lỗi xảy ra!</b>",
                    message.chat.id,
                    status_msg.message_id
                )
                
        except Exception as e:
            logger.error(f"Error in link4sub: {e}", exc_info=True)
            bot.reply_to(message, "❌ Lỗi xử lý lệnh!")
