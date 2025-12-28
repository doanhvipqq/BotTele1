import logging
import requests
import time
import threading

logger = logging.getLogger(__name__)

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    'Referer': 'https://link4m.co/',
    'Accept': 'application/json, text/plain, */*',
}

def bypass_process(bot, message, url, message_id):
    """Background process to bypass link4m"""
    try:
        # Step 1: Get task ID
        api_step1 = "https://api-v1-amber.vercel.app/api/v3/link4m"
        
        req1 = requests.get(api_step1, params={"link": url}, headers=HEADERS, timeout=15)
        data1 = req1.json()
        
        # Find task ID
        task_id = data1.get("task_id")
        if not task_id and "data" in data1:
            task_id = data1["data"].get("task_id")
        
        if not task_id:
            bot.edit_message_text(
                "❌ <b>Không lấy được Task ID</b>",
                message.chat.id,
                message_id
            )
            return
        
        # Step 2: Get result
        api_step2 = "https://api-v1-amber.vercel.app/api/v2/getresult"
        
        for i in range(60):  # Max 2 minutes
            try:
                req2 = requests.get(api_step2, params={"task_id": task_id}, headers=HEADERS, timeout=10)
                data2 = req2.json()
                
                final_url = data2.get("url")
                if not final_url and "data" in data2:
                    final_url = data2["data"].get("url")
                
                if final_url:
                    caption = f"""
<b>✅ Link 4M - Thành công!</b>

<blockquote expandable>
╭─────────────────────────╮
│ <b>🔗 Link gốc:</b>
│ {url[:50] + '...' if len(url) > 50 else url}
├─────────────────────────┤
│ <b>✨ Link 4M:</b>
│ {final_url}
╰─────────────────────────╯
</blockquote>

<i>📝 Copy link để sử dụng</i>
"""
                    bot.edit_message_text(caption.strip(), message.chat.id, message_id)
                    logger.info(f"Successfully processed link4m")
                    return
                
                # Wait if not ready
                if data2.get("success") is False:
                    time.sleep(2)
                    continue
                    
            except:
                time.sleep(2)
        
        # Timeout
        bot.edit_message_text(
            "❌ <b>Hết thời gian chờ (2 phút)</b>",
            message.chat.id,
            message_id
        )
        
    except Exception as e:
        logger.error(f"Error in bypass_process: {e}", exc_info=True)
        bot.edit_message_text(
            "❌ <b>Lỗi hệ thống</b>",
            message.chat.id,
            message_id
        )

def register_link4m(bot):
    """Register link4m command handler"""
    
    @bot.message_handler(commands=['link4m', 'l4m'])
    def link4m_handler(message):
        """Process link for 4M service"""
        try:
            args = message.text.split()
            if len(args) < 2:
                bot.reply_to(
                    message,
                    "🚫 <b>Vui lòng cung cấp link!</b>\n\n"
                    "<i>Ví dụ:</i> <code>/link4m https://example.com/...</code>"
                )
                return
            
            url = args[1].strip()
            logger.info(f"User {message.from_user.id} requested link4m for: {url}")
            
            status_msg = bot.reply_to(message, f"⏳ <b>Đang xử lý...</b>\n\n<i>Có thể mất tới 2 phút</i>")
            
            # Run in background thread
            thread = threading.Thread(
                target=bypass_process,
                args=(bot, message, url, status_msg.message_id)
            )
            thread.start()
            
        except Exception as e:
            logger.error(f"Error in link4m: {e}", exc_info=True)
            bot.reply_to(message, "❌ Lỗi xử lý lệnh!")
