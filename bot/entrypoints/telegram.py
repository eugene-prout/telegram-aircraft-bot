from bot.entrypoints.AbstractEntrypoint import AbstractEntrypoint

import logging
from telegram.ext import (
    ApplicationBuilder,
    CallbackQueryHandler,
    CommandHandler,
    MessageHandler,
    filters,
    InvalidCallbackData,
)

from bot.handlers.telegram import (
    flight_callback,
    introduction,
    invalid_callback,
    location,
    repeat_callback,
)
from bot.types import AircraftInformationCallback, RepeatCallback
from config import settings

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logging.getLogger("httpx").setLevel(logging.WARNING)


class TelegramEntrypoint(AbstractEntrypoint):
    def __init__(self):
        token = settings.TELEGRAM.TOKEN

        application = (
            ApplicationBuilder().token(token).arbitrary_callback_data(True).build()
        )

        handlers = [
            CommandHandler("start", introduction),
            MessageHandler(filters.LOCATION, location),
            CallbackQueryHandler(
                pattern=AircraftInformationCallback, callback=flight_callback
            ),
            CallbackQueryHandler(pattern=RepeatCallback, callback=repeat_callback),
            CallbackQueryHandler(
                pattern=InvalidCallbackData, callback=invalid_callback
            ),
            MessageHandler(filters.ALL, introduction),
        ]

        for handler in handlers:
            application.add_handler(handler)

        self.app = application

    def launch(self):
        self.app.run_polling()
