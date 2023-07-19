from bot.bootstrap import bootstrap
from config import settings

app = bootstrap()
method = settings.TELEGRAM_METHOD
if method == "polling":
    app.run_polling()
elif method == "webhook":
    url = settings.WEBHOOK_URL
    secret_token = settings.SECRET_TOKEN
    key = settings.KEY
    cert = settings.CERT

    app.run_webhook(port=8443, secret_token=secret_token, webhook_url=url)
else:
    raise ValueError(
        "TELEGRAM_METHOD env var not set. Please set either 'polling' or 'webhook'."
    )
