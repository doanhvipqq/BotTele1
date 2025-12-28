import logging
import time

logger = logging.getLogger(__name__)

def register_ping(bot):
    """Register ping/speed command handler"""
    
    @bot.message_handler(commands=['ping', 'speed'])
    def ping_handler(message):
        """Check bot response speed"""
        try:
            logger.info(f"User {message.from_user.id} requested ping check")
            
            # Record start time
            start_time = time.time()
            
            # Send initial message
            sent_msg = bot.reply_to(message, "🏓 Pinging...")
            
            # Calculate response time
            end_time = time.time()
            response_time_ms = round((end_time - start_time) * 1000, 2)
            
            # Determine speed status
            if response_time_ms < 100:
                status = "⚡ Cực nhanh"
                emoji = "🚀"
            elif response_time_ms < 300:
                status = "✅ Tốt"
                emoji = "👍"
            elif response_time_ms < 500:
                status = "⚠️ Trung bình"
                emoji = "🐌"
            else:
                status = "🐢 Chậm"
                emoji = "😴"
            
            # Beautiful formatted response
            caption = f"""
<b>🏓 Ping Test - Kết quả</b>

<blockquote expandable>
╭─────────────────────────╮
│ {emoji} <b>Tốc độ:</b> {status}
├─────────────────────────┤
│ ⚡ <b>Response time:</b>
│ {response_time_ms} ms
├─────────────────────────┤
│ 🤖 <b>Bot status:</b> Online
│ 📡 <b>Connection:</b> Stable
╰─────────────────────────╯
</blockquote>

<i>✨ Bot đang hoạt động tốt!</i>
"""
            
            # Edit message with result
            bot.edit_message_text(
                caption.strip(),
                message.chat.id,
                sent_msg.message_id
            )
            
            logger.info(f"Ping check completed: {response_time_ms}ms for user {message.from_user.id}")
            
        except Exception as e:
            logger.error(f"Error in ping command: {e}", exc_info=True)
            try:
                bot.reply_to(
                    message,
                    "❌ Có lỗi xảy ra khi kiểm tra ping. Vui lòng thử lại!"
                )
            except:
                pass
