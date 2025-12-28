import logging
from datetime import datetime
from telebot.types import Message

logger = logging.getLogger(__name__)

def register_in4(bot):
    """Register user info command handler"""
    
    @bot.message_handler(commands=['in4'])
    def handle_check(message: Message):
        """Display detailed user information"""
        try:
            # Get target user (from reply or self)
            user = message.reply_to_message.from_user if message.reply_to_message else message.from_user
            is_self = (user.id == message.from_user.id)
            
            logger.info(f"User {message.from_user.id} requested info for user {user.id}")
            
            # Send processing message
            status_msg = bot.reply_to(message, "🔍 Đang thu thập thông tin...")
            
            try:
                # Get detailed user information
                user_photos = bot.get_user_profile_photos(user.id, limit=1)
                chat_info = bot.get_chat(user.id)
                bio = chat_info.bio or "Không có"
                
                # User basic info
                user_first_name = user.first_name
                user_last_name = user.last_name or ""
                full_name = f"{user_first_name} {user_last_name}".strip()
                user_username = f"@{user.username}" if user.username else "Không có"
                user_language = user.language_code or "Không xác định"
                has_avatar = user_photos.total_count > 0

                # Default status for private chats
                status = "💬 Cuộc trò chuyện riêng"
                joined_date = "N/A"

                # Get group member status if in group
                if message.chat.type in ['group', 'supergroup']:
                    status_dict = {
                        "creator": "👑 Chủ sở hữu nhóm",
                        "administrator": "🛡️ Quản trị viên",
                        "member": "👤 Thành viên",
                        "restricted": "🚫 Bị hạn chế",
                        "left": "👋 Đã rời nhóm",
                        "kicked": "⛔ Đã bị kick"
                    }
                    try:
                        chat_member = bot.get_chat_member(message.chat.id, user.id)
                        status = status_dict.get(chat_member.status, "❓ Không xác định")
                        
                        # Get join date if available
                        if hasattr(chat_member, 'joined_date') and chat_member.joined_date:
                            joined_date = datetime.fromtimestamp(chat_member.joined_date).strftime('%d/%m/%Y %H:%M')
                        else:
                            joined_date = "Không có dữ liệu"
                    except Exception as e:
                        logger.warning(f"Could not get chat member info: {e}")
                        status = "❓ Không xác định"

                # Beautiful formatted caption
                caption = f"""
<b>👤 Thông Tin {'Của Bạn' if is_self else 'Người Dùng'}</b>

<blockquote expandable>
╭─────────────────────────╮
│ <b>🆔 User ID:</b>
│ <code>{user.id}</code>
├─────────────────────────┤
│ <b>📝 Tên đầy đủ:</b>
│ {full_name}
│
│ <b>🏷️ Username:</b>
│ {user_username}
│
│ <b>🌐 Ngôn ngữ:</b>
│ {user_language.upper()}
├─────────────────────────┤
│ <b>📋 Bio:</b>
│ {bio if len(bio) <= 100 else bio[:97] + '...'}
│
│ <b>🖼️ Avatar:</b>
│ {'✅ Có' if has_avatar else '❌ Không'}
├─────────────────────────┤
│ <b>🏘️ Trạng thái nhóm:</b>
│ {status}
│
│ <b>📅 Ngày tham gia:</b>
│ {joined_date}
╰─────────────────────────╯
</blockquote>

<i>✨ Thông tin được cập nhật realtime</i>
"""

                # Delete processing message
                try:
                    bot.delete_message(message.chat.id, status_msg.message_id)
                except:
                    pass

                # Send with avatar if available
                if has_avatar:
                    avatar_file_id = user_photos.photos[0][-1].file_id
                    bot.send_photo(
                        message.chat.id,
                        avatar_file_id,
                        caption=caption.strip(),
                        reply_to_message_id=message.message_id
                    )
                else:
                    bot.reply_to(message, caption.strip())
                
                logger.info(f"Successfully sent user info for {user.id}")

            except Exception as e:
                logger.error(f"Error fetching user details: {e}", exc_info=True)
                try:
                    bot.delete_message(message.chat.id, status_msg.message_id)
                except:
                    pass
                bot.reply_to(
                    message,
                    "⚠️ Không thể lấy thông tin chi tiết.\n\n"
                    "<i>Người dùng có thể đã chặn bot hoặc ẩn thông tin cá nhân.</i>"
                )

        except Exception as e:
            logger.error(f"Critical error in in4 command: {e}", exc_info=True)
            bot.reply_to(
                message,
                "❌ Có lỗi xảy ra khi xử lý yêu cầu. Vui lòng thử lại sau!"
            )
