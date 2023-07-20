import logging
import os
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    filters,
)

from bot.handlers import introduction, location
from config import settings

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logging.getLogger("httpx").setLevel(logging.WARNING)


def bootstrap():
    token = settings.TELEGRAM.TOKEN

    application = ApplicationBuilder().token(token).build()

    start_handler = CommandHandler("start", introduction)
    application.add_handler(start_handler)

    location_handler = MessageHandler(filters.LOCATION, location)
    application.add_handler(location_handler)

    unknown_handler = MessageHandler(filters.ALL, introduction)
    application.add_handler(unknown_handler)
    return application
