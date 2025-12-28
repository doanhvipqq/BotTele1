import logging

logger = logging.getLogger(__name__)

def register_help(bot):
    """Register help command with beautiful new UI"""
    
    # Welcome message với ASCII art style mới
    WELCOME_MSG = """
╔═══════════════════════════════╗
║   🌟 𝐁Ó𝐍𝐆𝐗 𝐁𝐎𝐓 🌟   ║
║   ━━━━━━━━━━━━━━━━━━━   ║
║    ✨ 𝒟𝒶 𝒸𝒽𝓊𝒸 𝓃𝒶𝓃𝑔 ✨    ║
╚═══════════════════════════════╝

𝗖𝗵𝗮̀𝗼 𝗺𝘂̛̀𝗻𝗴 𝗯𝗮̣𝗻 𝗱𝗲̂́𝗻 𝘃𝗼̛́𝗶 𝗕𝗼𝘁! 👋

▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰

𝙎𝙚𝙡𝙚𝙘𝙩 𝙖 𝙘𝙖𝙩𝙚𝙜𝙤𝙧𝙮 𝙗𝙚𝙡𝙤𝙬:
"""

    # Tools commands với style mới
    TOOLS_COMMANDS = """
🛠️ 「 𝗖𝗢̂𝗡𝗚 𝗖𝗨̣ & 𝗧𝗜𝗘̣̂𝗡 𝗜́𝗖𝗛 」

┏━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ 📦 /𝗽𝗿𝗼𝘅𝘆
┃ ➥ Lấy proxy miễn phí
┃
┃ 🐙 /𝗴𝗶𝘁𝗵𝘂𝗯 <username>
┃ ➥ Thông tin GitHub profile
┃
┃ 🎧 /𝘀𝗰𝗹 <url>
┃ ➥ Tải nhạc SoundCloud
┃
┃ 🌐 /𝘀𝗼𝘂𝗿𝗰𝗲𝘄𝗲𝗯 <url>
┃ ➥ Tải source website
┃
┃ 🎬 /𝘀𝗲𝗻𝗱 <url>
┃ ➥ Tải video đa nền tảng
┃
┃ 🖼️ /𝘁𝗵𝘂𝗺𝗯
┃ ➥ Thêm thumbnail cho file
┃
┃ 🔐 /𝗲𝗻𝗰𝗼𝗱𝗲
┃ ➥ Encode file Python
┃
┃ 👤 /𝗶𝗻𝟰
┃ ➥ Info user Telegram
┃
┃ ⏰ /𝘁𝗶𝗺𝗲
┃ ➥ Thời gian bot hoạt động
┃
┃ 🏓 /𝗽𝗶𝗻𝗴
┃ ➥ Kiểm tra tốc độ bot
┗━━━━━━━━━━━━━━━━━━━━━━━━━┛
"""

    MEDIA_COMMANDS = """
📱 「 𝗠𝗔̣𝗡𝗚 𝗫𝗔̃ 𝗛𝗢̣̂𝗜 」

┏━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ 🎵 /𝘁𝗶𝗸𝘁𝗼𝗸 <link>
┃ ➥ Thông tin TikTok video
┃
┃ 🖼️ /𝗶𝗺𝗮𝗴𝗲𝘀 <url>
┃ ➥ Lấy URL ảnh từ website
┃
┃ 📤 /𝘀𝗵𝗮𝗿𝗲 <link>
┃ ➥ Share bài Facebook
┃
┃ 🔍 /𝘀𝗲𝗮𝗿𝗰𝗵 <query>
┃ ➥ Tìm kiếm trên web
┃
┃ 🔗 /𝗹𝗶𝗻𝗸𝟰𝘀𝘂𝗯 <link>
┃ ➥ Xử lý link Facebook
┃
┃ 🔗 /𝗹𝗶𝗻𝗸𝟰𝗺 <link>
┃ ➥ Bypass link 4M
┗━━━━━━━━━━━━━━━━━━━━━━━━━┛
"""

    FUN_COMMANDS = """
🎮 「 𝗚𝗜𝗔̉𝗜 𝗧𝗥𝗜́ 」

┏━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ 😂 /𝗺𝗲𝗺𝗲
┃ ➥ Meme ngẫu nhiên cười vui
┃
┃ 🎲 /𝗿𝗮𝗻𝗱𝗼𝗺
┃ ➥ Nội dung ngẫu nhiên
┃
┃ 🇯🇵 /𝗮𝗻𝗶𝗺𝗲
┃ ➥ Video anime random
┃
┃ 👧 /𝗴𝗶𝗿𝗹
┃ ➥ Video girl random
┃
┃ 🎨 /𝗶𝗺𝗴𝗮𝗻𝗶𝗺𝗲
┃ ➥ Ảnh anime ngẫu nhiên
┃
┃ 🤗 /𝘀𝗾𝘂𝗲𝗲𝘇𝗲
┃ ➥ Reaction GIF squeeze
┗━━━━━━━━━━━━━━━━━━━━━━━━━┛
"""

    ADMIN_COMMANDS = """
👑 「 𝗤𝗨𝗔̉𝗡 𝗧𝗥𝗜̣ & 𝗩𝗜𝗣 」

┏━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ 💬 /𝘀𝗺𝘀 <sđt> <vòng>
┃ ➥ SMS spam server 1
┃
┃ 💎 /𝘀𝗺𝘀𝘃𝗶𝗽 <sđt> <vòng>
┃ ➥ SMS spam VIP server 2
┃
┃ ➕ /𝗮𝗱𝗱 <user_id>
┃ ➥ Thêm user vào VIP
┃
┃ 🎮 /𝗿𝗲𝗴 [số lượng]
┃ ➥ Random acc Garena (1-5)
┗━━━━━━━━━━━━━━━━━━━━━━━━━┛
"""

    BOT_INFO = """
ℹ️ 「 𝗧𝗛𝗢̂𝗡𝗚 𝗧𝗜𝗡 𝗕𝗢𝗧 」

┏━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ 🤖 𝐍𝐚𝐦𝐞: BóngX Bot
┃ 📌 𝐕𝐞𝐫𝐬𝐢𝐨𝐧: 2.0.0
┃ 👤 𝐀𝐮𝐭𝐡𝐨𝐫: @doanhvipqq
┃ ⚡ 𝐒𝐭𝐚𝐭𝐮𝐬: Online
┗━━━━━━━━━━━━━━━━━━━━━━━━━┛

━━━━━━━━━━━━━━━━━━━━━━━━━

💡 𝙏𝙞𝙥: Dùng /𝗽𝗶𝗻𝗴 để check tốc độ!
"""

    HELP_MENU = """
📚 「 𝗧𝗔̂́𝗧 𝗖𝗔̉ 𝗟𝗘̣̂𝗡𝗛 𝗕𝗢𝗧 」

━━━━━━━━━━━━━━━━━━━━━━━━━

🛠️ 𝗖𝗢̂𝗡𝗚 𝗖𝗨̣
/proxy • /github • /scl • /time
/ping • /in4 • /encode • /thumb

━━━━━━━━━━━━━━━━━━━━━━━━━

📱 𝗠𝗔̣𝗡𝗚 𝗫𝗔̃ 𝗛𝗢̣̂𝗜
/tiktok • /images • /share
/search • /link4sub • /link4m

━━━━━━━━━━━━━━━━━━━━━━━━━

🎮 𝗚𝗜𝗔̉𝗜 𝗧𝗥𝗜́
/meme • /anime • /girl
/imganime • /squeeze

━━━━━━━━━━━━━━━━━━━━━━━━━

👑 𝗩𝗜𝗣 & 𝗤𝗨𝗔̉𝗡 𝗧𝗥𝗜̣
/sms • /smsvip • /add • /reg

━━━━━━━━━━━━━━━━━━━━━━━━━

✨ 𝙋𝙤𝙬𝙚𝙧𝙚𝙙 𝙗𝙮 𝐁𝐨́𝐧𝐠𝐗 𝐓𝐞𝐚𝐦
"""

    @bot.message_handler(commands=['help', 'start'])
    def send_help(message):
        """Send help menu with inline keyboard"""
        logger.info(f"User {message.from_user.id} requested help menu")
        
        # Create inline keyboard
        markup = types.InlineKeyboardMarkup(row_width=2)
        
        buttons = [
            types.InlineKeyboardButton("🛠️ 𝗖𝗼̂𝗻𝗴 𝗰𝘂̣", callback_data="help_tools"),
            types.InlineKeyboardButton("📱 𝗠𝗮̣𝗻𝗴 𝗫𝗮̃", callback_data="help_media"),
            types.InlineKeyboardButton("🎮 𝗚𝗶𝗮̉𝗶 𝗧𝗿𝗶́", callback_data="help_fun"),
            types.InlineKeyboardButton("👑 𝗩𝗜𝗣", callback_data="help_admin"),
            types.InlineKeyboardButton("📚 𝗧𝗮̂́𝘁 𝗖𝗮̉", callback_data="help_all"),
            types.InlineKeyboardButton("ℹ️ 𝗜𝗻𝗳𝗼", callback_data="help_info")
        ]
        
        markup.add(*buttons)
        
        bot.send_message(
            message.chat.id,
            WELCOME_MSG,
            reply_markup=markup
        )

    @bot.callback_query_handler(func=lambda call: call.data.startswith('help_'))
    def handle_help_callback(call):
        """Handle help menu button clicks"""
        category = call.data.replace('help_', '')
        
        # Create back button
        markup = types.InlineKeyboardMarkup()
        back_btn = types.InlineKeyboardButton("« 𝗕𝗮𝗰𝗸 𝘁𝗼 𝗠𝗲𝗻𝘂", callback_data="help_back")
        markup.add(back_btn)
        
        # Select message based on category
        if category == 'tools':
            msg = TOOLS_COMMANDS
        elif category == 'media':
            msg = MEDIA_COMMANDS
        elif category == 'fun':
            msg = FUN_COMMANDS
        elif category == 'admin':
            msg = ADMIN_COMMANDS
        elif category == 'all':
            msg = HELP_MENU
        elif category == 'info':
            msg = BOT_INFO
        elif category == 'back':
            # Return to main menu
            markup = types.InlineKeyboardMarkup(row_width=2)
            buttons = [
                types.InlineKeyboardButton("🛠️ 𝗖𝗼̂𝗻𝗴 𝗰𝘂̣", callback_data="help_tools"),
                types.InlineKeyboardButton("📱 𝗠𝗮̣𝗻𝗴 𝗫𝗮̃", callback_data="help_media"),
                types.InlineKeyboardButton("🎮 𝗚𝗶𝗮̉𝗶 𝗧𝗿𝗶́", callback_data="help_fun"),
                types.InlineKeyboardButton("👑 𝗩𝗜𝗣", callback_data="help_admin"),
                types.InlineKeyboardButton("📚 𝗧𝗮̂́𝘁 𝗖𝗮̉", callback_data="help_all"),
                types.InlineKeyboardButton("ℹ️ 𝗜𝗻𝗳𝗼", callback_data="help_info")
            ]
            markup.add(*buttons)
            msg = WELCOME_MSG
        else:
            msg = "Unknown category"
        
        try:
            bot.edit_message_text(
                msg,
                call.message.chat.id,
                call.message.message_id,
                reply_markup=markup
            )
            bot.answer_callback_query(call.id)
        except Exception as e:
            logger.error(f"Error editing help message: {e}")
            bot.answer_callback_query(call.id, "Error!")
