import logging
import requests
from datetime import datetime

logger = logging.getLogger(__name__)

def register_github(bot):
    """Register GitHub profile command handler"""
    
    @bot.message_handler(commands=['github']) 
    def handle_infogithub(message): 
        """Display GitHub user profile information"""
        try:
            # Extract username from command
            args = message.text.split()
            if len(args) < 2:
                bot.reply_to(
                    message,
                    "🚫 <b>Vui lòng cung cấp username GitHub!</b>\n\n"
                    "<i>Ví dụ:</i> <code>/github doanhvipqq</code>"
                )
                return
            
            username = args[1].strip()
            logger.info(f"User {message.from_user.id} requested GitHub info for {username}")
            
            # Send loading message
            status_msg = bot.reply_to(message, f"🔍 Đang tìm kiếm <b>{username}</b> trên GitHub...")
            
            # Fetch GitHub API
            api_url = f"https://api.github.com/users/{username}"
            response = requests.get(api_url, timeout=10)
            
            # Delete loading message
            try:
                bot.delete_message(message.chat.id, status_msg.message_id)
            except:
                pass
            
            if response.status_code == 200:
                data = response.json()
                
                # Parse data
                avatar_url = data.get('avatar_url', '')
                login = data.get('login', 'N/A')
                name = data.get('name') or login  
                bio = data.get('bio') or 'Không có bio'
                user_id = data.get('id', 'N/A')
                public_repos = data.get('public_repos', 0)
                followers = data.get('followers', 0)
                following = data.get('following', 0)
                company = data.get('company') or 'Không có'
                location = data.get('location') or 'Không rõ'
                blog = data.get('blog') or 'Không có'
                twitter = data.get('twitter_username')
                twitter_display = f"@{twitter}" if twitter else 'Không có'
                html_url = data.get('html_url', '')
                
                # Format creation date
                created_at = data.get('created_at', '')
                if created_at:
                    try:
                        dt = datetime.strptime(created_at, '%Y-%m-%dT%H:%M:%SZ')
                        created_at = dt.strftime('%d/%m/%Y')
                    except:
                        created_at = created_at[:10]
                
                # Beautiful formatted caption
                caption = f"""
<b>🐙 Thông Tin GitHub Profile</b>

<blockquote expandable>
╭─────────────────────────╮
│ <b>👤 Username:</b> {login}
│ <b>📝 Tên:</b> {name}
│ <b>🆔 ID:</b> <code>{user_id}</code>
├─────────────────────────┤
│ <b>📋 Bio:</b>
│ {bio if len(bio) <= 80 else bio[:77] + '...'}
├─────────────────────────┤
│ <b>📊 Thống kê:</b>
│ • Repositories: {public_repos:,}
│ • Followers: {followers:,}
│ • Following: {following:,}
├─────────────────────────┤
│ <b>🏢 Company:</b> {company}
│ <b>📍 Location:</b> {location}
│ <b>🌐 Website:</b> {blog if len(blog) <= 30 else blog[:27] + '...'}
│ <b>🐦 Twitter:</b> {twitter_display}
├─────────────────────────┤
│ <b>📅 Tham gia:</b> {created_at}
│ <b>🔗 Profile:</b> <a href="{html_url}">{login}</a>
╰─────────────────────────╯
</blockquote>

<i>✨ Dữ liệu từ GitHub API</i>
"""
                
                # Send with avatar
                if avatar_url:
                    try:
                        bot.send_photo(
                            message.chat.id,
                            avatar_url,
                            caption=caption.strip(),
                            reply_to_message_id=message.message_id
                        )
                        logger.info(f"Successfully sent GitHub info for {username}")
                    except Exception as e:
                        logger.error(f"Failed to send photo: {e}")
                        bot.reply_to(message, caption.strip())
                else:
                    bot.reply_to(message, caption.strip())
                    
            elif response.status_code == 404:
                bot.reply_to(
                    message,
                    f"❌ <b>Không tìm thấy user '{username}'</b>\n\n"
                    "<i>Vui lòng kiểm tra lại username.</i>"
                )
                logger.warning(f"GitHub user not found: {username}")
            else:
                bot.reply_to(
                    message,
                    f"⚠️ Lỗi khi lấy dữ liệu từ GitHub (Status: {response.status_code})\n\n"
                    "<i>Vui lòng thử lại sau!</i>"
                )
                logger.error(f"GitHub API returned status {response.status_code}")
     
        except IndexError: 
            bot.reply_to(
                message,
                "🚫 <b>Vui lòng cung cấp username GitHub!</b>\n\n"
                "<i>Ví dụ:</i> <code>/github doanhvipqq</code>"
            )
        except requests.Timeout:
            logger.error("GitHub API request timed out")
            bot.reply_to(
                message,
                "⏱️ Yêu cầu bị timeout. Vui lòng thử lại!"
            )
        except Exception as e:
            logger.error(f"Error in github command: {e}", exc_info=True)
            bot.reply_to(
                message,
                "❌ Có lỗi xảy ra khi xử lý yêu cầu. Vui lòng thử lại!"
            )
