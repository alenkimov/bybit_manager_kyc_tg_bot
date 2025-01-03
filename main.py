import asyncio
import logging
from bot.start_bot import start_bot

try:
    from conf import API_KEY
except ImportError:
    API_KEY = None

API_KEY = API_KEY or ""


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    try:
        asyncio.run(start_bot(API_KEY))
    except KeyboardInterrupt:
        print("Bot stopped by user (CTRL + C)")
