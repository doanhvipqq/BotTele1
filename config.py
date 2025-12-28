# ============================================
# BóngX Bot - Configuration
# ============================================

# Admin Configuration
ADMIN_ID = 7509896689
GROUP_ID = [-1002256706038]

# Error Messages
ERROR_MSG = "⚠️ Bạn không có quyền sử dụng lệnh này."
RATE_LIMIT_MSG = "⏰ Vui lòng đợi {seconds}s trước khi sử dụng lệnh này."

# Bot Metadata
BOT_NAME = "BóngX Bot"
BOT_VERSION = "2.0.0"
BOT_AUTHOR = "@doanhvipqq"
BOT_DESCRIPTION = "Bot Telegram đa chức năng với nhiều tính năng hữu ích"

# Logging Configuration
LOG_LEVEL = "INFO"  # DEBUG, INFO, WARNING, ERROR
LOG_TO_FILE = True
LOG_FILE = "bot.log"

# Feature Flags
ENABLE_ANALYTICS = False
ENABLE_RATE_LIMITING = True
ENABLE_AUTO_RESTART = True
MAX_RESTART_ATTEMPTS = 5

# Rate Limiting (seconds)
RATE_LIMITS = {
    'default': 3,
    'sms': 60,
    'smsvip': 120,
    'share': 30
}
