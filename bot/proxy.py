import logging
import requests

logger = logging.getLogger(__name__)

# 📦 Proxy sources by type
PROXY_SOURCES = {
    "http": {
        "filename": "http.txt",
        "urls": [
            "https://api.proxyscrape.com/v2/?request=displayproxies&protocol=http&timeout=10000&country=all&ssl=all&anonymity=all",
            "https://raw.githubusercontent.com/BreakingTechFr/Proxy_Free/main/proxies/http.txt",
            "https://raw.githubusercontent.com/ErcinDedeoglu/proxies/main/proxies/http.txt",
            "https://raw.githubusercontent.com/ErcinDedeoglu/proxies/main/proxies/https.txt",
            "https://raw.githubusercontent.com/proxifly/free-proxy-list/main/proxies/protocols/http/data.txt",
            "https://raw.githubusercontent.com/vakhov/fresh-proxy-list/master/http.txt",
            "https://raw.githubusercontent.com/vakhov/fresh-proxy-list/master/https.txt",
            "https://raw.githubusercontent.com/MuRongPIG/Proxy-Master/main/http.txt",
            "https://raw.githubusercontent.com/officialputuid/KangProxy/KangProxy/http/http.txt",
            "https://sunny9577.github.io/proxy-scraper/generated/http_proxies.txt"
        ]
    },
    "socks4": {
        "filename": "socks4.txt",
        "urls": [
            "https://api.proxyscrape.com/v2/?request=displayproxies&protocol=socks4&timeout=10000&country=all&ssl=all&anonymity=all",
            "https://raw.githubusercontent.com/zloi-user/hideip.me/main/socks4.txt",
            "https://raw.githubusercontent.com/ErcinDedeoglu/proxies/main/proxies/socks4.txt",
            "https://raw.githubusercontent.com/proxifly/free-proxy-list/main/proxies/protocols/http/socks4.txt",
            "https://raw.githubusercontent.com/vakhov/fresh-proxy-list/master/socks4.txt",
            "https://raw.githubusercontent.com/MuRongPIG/Proxy-Master/main/socks4.txt",
            "https://raw.githubusercontent.com/officialputuid/KangProxy/KangProxy/socks4/socks4.txt",
            "https://sunny9577.github.io/proxy-scraper/generated/socks4_proxies.txt",
            "https://raw.githubusercontent.com/TheSpeedX/SOCKS-List/master/socks4.txt"
        ]
    },
    "socks5": {
        "filename": "socks5.txt",
        "urls": [
            "https://raw.githubusercontent.com/zloi-user/hideip.me/main/socks5.txt",
            "https://raw.githubusercontent.com/hookzof/socks5_list/master/proxy.txt",
            "https://raw.githubusercontent.com/BreakingTechFr/Proxy_Free/main/proxies/socks5.txt",
            "https://raw.githubusercontent.com/ErcinDedeoglu/proxies/main/proxies/socks5.txt",
            "https://raw.githubusercontent.com/proxifly/free-proxy-list/main/proxies/protocols/http/socks5.txt",
            "https://raw.githubusercontent.com/vakhov/fresh-proxy-list/master/socks5.txt",
            "https://raw.githubusercontent.com/MuRongPIG/Proxy-Master/main/socks5.txt",
            "https://raw.githubusercontent.com/officialputuid/KangProxy/KangProxy/socks5/socks5.txt",
            "https://sunny9577.github.io/proxy-scraper/generated/socks5_proxies.txt",
            "https://raw.githubusercontent.com/TheSpeedX/SOCKS-List/master/socks5.txt"
        ]
    }
}

def fetch_proxies(url):
    """Fetch proxies from a single URL"""
    try:
        r = requests.get(url, timeout=10)
        if r.ok:
            proxies = set(r.text.strip().splitlines())
            logger.info(f"Fetched {len(proxies)} proxies from {url[:50]}...")
            return proxies
    except Exception as e:
        logger.warning(f"Failed to fetch from {url[:50]}...: {e}")
        return set()
    return set()

def update_proxies():
    """Update all proxy lists and return stats"""
    all_proxies = set()
    stats = {"http": 0, "socks4": 0, "socks5": 0}

    for proxy_type, info in PROXY_SOURCES.items():
        proxies = set()
        logger.info(f"Fetching {proxy_type.upper()} proxies from {len(info['urls'])} sources...")
        
        for url in info["urls"]:
            proxies |= fetch_proxies(url)

        # Save to file
        with open(info["filename"], "w") as f:
            f.write("\n".join(sorted(proxies)))

        all_proxies |= proxies
        stats[proxy_type] = len(proxies)
        logger.info(f"Saved {len(proxies)} {proxy_type.upper()} proxies")

    # Save combined file
    with open("PROXY_FREE.txt", "w") as f:
        f.write("\n".join(sorted(all_proxies)))

    logger.info(f"Total proxies collected: {len(all_proxies)}")
    return stats, len(all_proxies)

def register_proxy(bot):
    """Register proxy command handler"""
    
    @bot.message_handler(commands=["proxy"])
    def send_proxy(msg):
        """Fetch and send proxy list"""
        logger.info(f"User {msg.from_user.id} requested proxy list")
        
        status_msg = bot.reply_to(msg, "⏳ <b>Đang thu thập proxies...</b>\n\n<i>Vui lòng đợi khoảng 30s</i>")

        try:
            bot.send_chat_action(msg.chat.id, "upload_document")
            
            # Fetch proxies
            stats, total = update_proxies()

            # Delete status message
            try:
                bot.delete_message(msg.chat.id, status_msg.message_id)
            except:
                pass

            # Beautiful caption with stats
            caption = f"""
<b>📦 Danh sách Proxy miễn phí</b>

<blockquote expandable>
╭─────────────────────╮
│ <b>📊 Thống kê:</b>
│ • HTTP: {stats['http']:,} proxies
│ • SOCKS4: {stats['socks4']:,} proxies
│ • SOCKS5: {stats['socks5']:,} proxies
├─────────────────────┤
│ <b>💯 Tổng cộng:</b> {total:,} proxies
╰─────────────────────╯
</blockquote>

<i>✨ Cập nhật realtime từ nhiều nguồn</i>
"""

            # Send file
            with open("PROXY_FREE.txt", "rb") as f:
                bot.send_document(
                    msg.chat.id,
                    f,
                    caption=caption.strip(),
                    reply_to_message_id=msg.message_id
                )
            
            logger.info(f"Successfully sent {total} proxies to user {msg.from_user.id}")
            
        except Exception as e:
            logger.error(f"Error in proxy command: {e}", exc_info=True)
            try:
                bot.delete_message(msg.chat.id, status_msg.message_id)
            except:
                pass
            bot.reply_to(
                msg,
                "❌ Có lỗi xảy ra khi thu thập proxies.\n\n<i>Vui lòng thử lại sau!</i>"
            )
