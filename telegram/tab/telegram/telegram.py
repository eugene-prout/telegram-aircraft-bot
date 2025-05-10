from telegram.ext import (ApplicationBuilder, CallbackQueryHandler,
                          CommandHandler, InvalidCallbackData, MessageHandler,
                          filters)

from tab.telegram.handlers import (error_handler, flight_callback, introduction,
                                   invalid_callback, location, repeat_callback)
from tab.telegram.messages import AircraftInformationCallback, RepeatCallback


class TelegramBotService:
    def __init__(self, telegram_token: str):
        application = (
            ApplicationBuilder()
            .token(telegram_token)
            .arbitrary_callback_data(True)
            .build()
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
            
        # application.add_error_handler(error_handler)

        self.app = application

    def launch(self):
        self.app.run_polling()
