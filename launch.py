from bot.entrypoints.api import APIEntrypoint
from bot.entrypoints.telegram import TelegramEntrypoint
from config import settings

entrypoint = settings.ENTRYPOINT

if entrypoint == "TELEGRAM":
    app = TelegramEntrypoint()
    app.launch()
elif entrypoint == "API":
    app = APIEntrypoint()
    app.launch()
else:
    raise ValueError(
        "ENTRYPOINT env var not set. Please set either 'TELEGRAM' or 'API'."
    )
