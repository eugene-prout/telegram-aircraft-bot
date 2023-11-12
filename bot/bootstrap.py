from dataclasses import dataclass
import logging
import os
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CallbackQueryHandler,
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes
)

from bot.handlers import flight_callback, introduction, location, repeat_callback
from bot.services import FlightObservation
from bot.types import RepeatCallback
from config import settings

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logging.getLogger("httpx").setLevel(logging.WARNING)


def get_chat_id(update: Update):
    return update.effective_chat.id

def send_message(update: Update, context: ContextTypes.DEFAULT_TYPE, message: str):
    context.bot.send_message(
            chat_id=update.effective_chat.id, text=message
    )

def send_photo()

def wrapper_function(fn):



def bootstrap():
    token = settings.TELEGRAM.TOKEN

    application = (
        ApplicationBuilder().token(token).arbitrary_callback_data(True).build()
    )

    start_handler = CommandHandler("start", introduction)
    application.add_handler(start_handler)

    location_handler = MessageHandler(filters.LOCATION, location)
    application.add_handler(location_handler)

    flight_callback_handler = CallbackQueryHandler(
        pattern=FlightObservation, callback=flight_callback
    )
    application.add_handler(flight_callback_handler)

    repeat_callback_handler = CallbackQueryHandler(
        pattern=RepeatCallback, callback=repeat_callback
    )
    application.add_handler(repeat_callback_handler)

    unknown_handler = MessageHandler(filters.ALL, introduction)
    application.add_handler(unknown_handler)

    return application
