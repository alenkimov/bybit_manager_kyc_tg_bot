import asyncio
import logging
from bot.start_bot import start_bot


API_KEY = ""


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    try:
        asyncio.run(start_bot(API_KEY))
    except KeyboardInterrupt:
        print("Bot stopped by user (CTRL + C)")
