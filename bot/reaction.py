import random
import logging
from telebot import types

logger = logging.getLogger(__name__)

# Emoji list for reactions
EMOJI_LIST = [
    '👍', '👎', '❤️', '🔥', '🥰', '👏', '😁', '🤔', '🤯', '😱', '🤬', '😢', '🎉', '🤩', '🤮', '💩',
    '🙏', '👌', '🕊️', '🤡', '🥱', '🥴', '😍', '🐳', '❤️‍🔥', '🌚', '🌭', '💯', '🤣', '⚡',
    '🍌', '🏆', '💔', '🤨', '😐', '🍓', '🍾', '💋', '🖕', '😈', '😴', '😭', '🤓', '👻', '👨‍💻',
    '👀', '🎃', '🙈', '😇', '😨', '🤝', '✍️', '🤗', '🫡', '🎅', '🎄', '☃️', '💅', '🤪', '🗿',
    '🆒', '💘', '🙉', '🦄', '😘', '💊', '🙊', '😎', '👾', '🤷‍♂️', '🤷', '🤷‍♀️', '😡'
]

def register_reaction(bot):
    """Register auto reaction handler for all messages"""
    
    @bot.message_handler(
        func=lambda message: not (message.text or "").startswith('/'),
        content_types=['text', 'video', 'sticker', 'audio', 'voice']
    )
    def handle_all_messages(message):
        """Add random emoji reaction to messages"""
        # Skip if not in allowed groups (optional filter)
        # if message.chat.id not in GROUP_ID:
        #     return

        emoji = random.choice(EMOJI_LIST)
        try:
            bot.set_message_reaction(
                message.chat.id,
                message.message_id,
                reaction=[types.ReactionTypeEmoji(emoji)]
            )
            logger.debug(f"Added reaction {emoji} to message {message.message_id}")
        except Exception as e:
            logger.debug(f"Failed to add reaction: {e}")
            pass
