import logging
import requests
import html
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)

def register_search(bot):
    """Register web search command handler"""
    
    @bot.message_handler(commands=['search'])
    def search(message):
        """Search the web using DuckDuckGo"""
        args = message.text.split(maxsplit=1)
        
        if len(args) < 2:
            bot.reply_to(
                message,
                "🚫 <b>Vui lòng nhập từ khóa tìm kiếm!</b>\n\n"
                "<i>Ví dụ:</i> <code>/search cách làm bánh mì</code>"
            )
            return

        query = args[1].strip()
        logger.info(f"User {message.from_user.id} searching for: {query}")
        
        loading = bot.send_message(
            message.chat.id,
            f"🔎 <b>Đang tìm kiếm:</b> {html.escape(query)}\n\n<i>Vui lòng đợi...</i>"
        )

        try:
            results = search_duckduckgo(query)
            
            if not results:
                bot.edit_message_text(
                    f"❌ <b>Không tìm thấy kết quả cho:</b> {html.escape(query)}\n\n"
                    "<i>Thử từ khóa khác hoặc kiểm tra lại chính tả.</i>",
                    message.chat.id,
                    loading.message_id
                )
                logger.warning(f"No search results found for: {query}")
                return
            
            # Format results beautifully
            reply = f"""
<b>🔍 Kết quả tìm kiếm: {html.escape(query)}</b>

<blockquote expandable>
"""
            
            for i, r in enumerate(results, 1):
                title = html.escape(r['title'][:60] + '...' if len(r['title']) > 60 else r['title'])
                url = r['href']
                reply += f"{i}. <b>{title}</b>\n   🔗 {url}\n\n"
            
            reply += "</blockquote>\n\n<i>✨ Powered by DuckDuckGo</i>"

            bot.edit_message_text(
                reply.strip(),
                message.chat.id,
                loading.message_id,
                disable_web_page_preview=True
            )
            
            logger.info(f"Successfully returned {len(results)} search results")

        except Exception as e:
            logger.error(f"Error in search command: {e}", exc_info=True)
            bot.edit_message_text(
                f"❌ <b>Lỗi khi tìm kiếm</b>\n\n"
                f"<i>Chi tiết: {html.escape(str(e)[:100])}</i>",
                message.chat.id,
                loading.message_id
            )

def search_duckduckgo(query, max_results=5):
    """Search DuckDuckGo and return results"""
    try:
        logger.info(f"Searching DuckDuckGo for: {query}")
        
        res = requests.get(
            f"https://html.duckduckgo.com/html/?q={requests.utils.quote(query)}",
            headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'},
            timeout=10
        )
        
        if res.status_code != 200:
            logger.warning(f"DuckDuckGo returned status {res.status_code}")
            return []
        
        soup = BeautifulSoup(res.text, 'html.parser')
        results = []

        for a in soup.find_all("a", class_="result__a"):
            href = a.get("href")
            if not href or href.startswith("/l/?kh="):
                continue  # Skip internal redirects
            
            title = a.get_text(strip=True)
            results.append({'title': title, 'href': href})
            
            if len(results) >= max_results:
                break

        logger.info(f"Found {len(results)} search results")
        return results
        
    except requests.Timeout:
        logger.error("Search request timed out")
        return []
    except Exception as e:
        logger.error(f"Error searching DuckDuckGo: {e}")
        return []
