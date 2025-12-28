import os
import sys
import time
import logging
import telebot
import threading
from flask import Flask, jsonify
from dotenv import load_dotenv
from datetime import datetime

# ============================================
# LOGGING CONFIGURATION
# ============================================
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('bot.log', encoding='utf-8')
    ]
)
logger = logging.getLogger(__name__)

# ============================================
# LOAD ENVIRONMENT VARIABLES
# ============================================
load_dotenv()

# Bot metadata
BOT_VERSION = "2.0.0"
BOT_NAME = "BóngX Bot"
START_TIME = datetime.now()

# ============================================
# FLASK WEB SERVER - RENDER KEEP ALIVE
# ============================================
app = Flask(__name__)

@app.route('/')
def home():
    """Home endpoint - confirms bot is running"""
    return """
    <html>
        <head><title>BóngX Bot</title></head>
        <body style="font-family: Arial; text-align: center; padding: 50px;">
            <h1>🤖 BóngX Bot đang hoạt động!</h1>
            <p>Bot version: {version}</p>
            <p>Uptime: {uptime}</p>
            <hr>
            <a href="/health">Health Check</a> | <a href="/status">Status</a>
        </body>
    </html>
    """.format(
        version=BOT_VERSION,
        uptime=str(datetime.now() - START_TIME).split('.')[0]
    )

@app.route('/health')
def health():
    """Health check endpoint for Render"""
    return jsonify({
        'status': 'healthy',
        'bot': 'online',
        'timestamp': datetime.now().isoformat()
    }), 200

@app.route('/status')
def status():
    """Detailed status endpoint"""
    uptime = datetime.now() - START_TIME
    return jsonify({
        'bot_name': BOT_NAME,
        'version': BOT_VERSION,
        'status': 'running',
        'uptime_seconds': int(uptime.total_seconds()),
        'uptime_formatted': str(uptime).split('.')[0],
        'start_time': START_TIME.isoformat(),
        'current_time': datetime.now().isoformat()
    }), 200

def run_web_server():
    """Run Flask server in separate thread"""
    port = int(os.environ.get('PORT', 8080))
    logger.info(f"🌐 Starting Flask server on port {port}")
    app.run(host='0.0.0.0', port=port, debug=False, use_reloader=False)

def keep_alive():
    """Start web server to keep bot alive on Render"""
    t = threading.Thread(target=run_web_server, daemon=True)
    t.start()
    logger.info("✅ Keep-alive web server started")

# ============================================
# BOT INITIALIZATION
# ============================================
TOKEN = os.getenv('TELEGRAM_TOKEN', '8567340377:AAG9LLjKin8NjJDtIWDsS7jXa_vogHY6nMI')

if not TOKEN:
    logger.error("❌ TELEGRAM_TOKEN not found in environment variables!")
    sys.exit(1)

logger.info(f"🤖 Initializing {BOT_NAME} v{BOT_VERSION}...")
bot = telebot.TeleBot(TOKEN, parse_mode="HTML")

# ============================================
# ERROR HANDLING
# ============================================
def error_handler(func):
    """Decorator for error handling"""
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            logger.error(f"Error in {func.__name__}: {str(e)}", exc_info=True)
            return None
    return wrapper

# ============================================
# MODULE REGISTRATION
# ============================================
logger.info("📦 Loading bot modules...")

try:
    from bot.encode import register_encode
    register_encode(bot)
    logger.info("✓ Loaded: encode")
except Exception as e:
    logger.error(f"✗ Failed to load encode: {e}")

try:
    from bot.share import register_share
    register_share(bot)
    logger.info("✓ Loaded: share")
except Exception as e:
    logger.error(f"✗ Failed to load share: {e}")

try:
    from bot.scl import register_scl
    register_scl(bot)
    logger.info("✓ Loaded: scl")
except Exception as e:
    logger.error(f"✗ Failed to load scl: {e}")

try:
    from bot.in4 import register_in4
    register_in4(bot)
    logger.info("✓ Loaded: in4")
except Exception as e:
    logger.error(f"✗ Failed to load in4: {e}")

try:
    from bot.send import register_send
    register_send(bot)
    logger.info("✓ Loaded: send")
except Exception as e:
    logger.error(f"✗ Failed to load send: {e}")

try:
    from bot.time import register_time
    register_time(bot)
    logger.info("✓ Loaded: time")
except Exception as e:
    logger.error(f"✗ Failed to load time: {e}")

try:
    from bot.help import register_help
    register_help(bot)
    logger.info("✓ Loaded: help")
except Exception as e:
    logger.error(f"✗ Failed to load help: {e}")

try:
    from bot.proxy import register_proxy
    register_proxy(bot)
    logger.info("✓ Loaded: proxy")
except Exception as e:
    logger.error(f"✗ Failed to load proxy: {e}")

try:
    from bot.random import register_random
    register_random(bot)
    logger.info("✓ Loaded: random")
except Exception as e:
    logger.error(f"✗ Failed to load random: {e}")

try:
    from bot.tiktok import register_tiktok
    register_tiktok(bot)
    logger.info("✓ Loaded: tiktok")
except Exception as e:
    logger.error(f"✗ Failed to load tiktok: {e}")

try:
    from bot.github import register_github
    register_github(bot)
    logger.info("✓ Loaded: github")
except Exception as e:
    logger.error(f"✗ Failed to load github: {e}")

try:
    from bot.search import register_search
    register_search(bot)
    logger.info("✓ Loaded: search")
except Exception as e:
    logger.error(f"✗ Failed to load search: {e}")

try:
    from bot.meme import register_meme
    register_meme(bot)
    logger.info("✓ Loaded: meme")
except Exception as e:
    logger.error(f"✗ Failed to load meme: {e}")

try:
    from bot.spamsms import register_spamsms
    register_spamsms(bot)
    logger.info("✓ Loaded: spamsms")
except Exception as e:
    logger.error(f"✗ Failed to load spamsms: {e}")

try:
    from bot.sourceweb import register_sourceweb
    register_sourceweb(bot)
    logger.info("✓ Loaded: sourceweb")
except Exception as e:
    logger.error(f"✗ Failed to load sourceweb: {e}")

try:
    from bot.reg import register_handlers
    register_handlers(bot)
    logger.info("✓ Loaded: reg")
except Exception as e:
    logger.error(f"✗ Failed to load reg: {e}")

try:
    from bot.link4sub import register_link4sub
    register_link4sub(bot)
    logger.info("✓ Loaded: link4sub")
except Exception as e:
    logger.error(f"✗ Failed to load link4sub: {e}")

try:
    from bot.link4m import register_link4m
    register_link4m(bot)
    logger.info("✓ Loaded: link4m")
except Exception as e:
    logger.error(f"✗ Failed to load link4m: {e}")

try:
    from bot.ping import register_ping
    register_ping(bot)
    logger.info("✓ Loaded: ping")
except Exception as e:
    logger.error(f"✗ Failed to load ping: {e}")

logger.info("✅ All modules loaded successfully!")

# ============================================
# MAIN FUNCTION WITH AUTO-RESTART
# ============================================
def main():
    """Main bot loop with auto-restart on crash"""
    retry_count = 0
    max_retries = 5
    
    while retry_count < max_retries:
        try:
            logger.info(f"🚀 Starting {BOT_NAME} polling... (Attempt {retry_count + 1})")
            logger.info(f"📊 Bot Info: @{bot.get_me().username}")
            
            # Start polling
            bot.infinity_polling(timeout=60, long_polling_timeout=60)
            
        except KeyboardInterrupt:
            logger.info("⏹️  Bot stopped by user")
            break
            
        except Exception as e:
            retry_count += 1
            logger.error(f"❌ Bot crashed: {str(e)}", exc_info=True)
            
            if retry_count < max_retries:
                wait_time = min(retry_count * 10, 60)
                logger.info(f"🔄 Restarting in {wait_time} seconds... (Retry {retry_count}/{max_retries})")
                time.sleep(wait_time)
            else:
                logger.error("💀 Max retries reached. Bot stopped.")
                break

if __name__ == '__main__':
    # Start keep-alive server
    keep_alive()
    
    # Add separator for better log visibility
    logger.info("=" * 60)
    logger.info(f"🎯 {BOT_NAME} v{BOT_VERSION} - Ready to serve!")
    logger.info("=" * 60)
    
    # Start bot with auto-restart
    main()
