import logging
import os

from tab.telegram.telegram import TelegramBotService

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logging.getLogger("httpx").setLevel(logging.WARNING)

token = os.environ["TELEGRAM_TOKEN"]
app = TelegramBotService(token)
app.launch()