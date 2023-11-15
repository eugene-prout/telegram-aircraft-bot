import logging
from telegram import Update
from telegram.ext import (
    ContextTypes,
)

from bot.types import LatLong

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logging.getLogger("httpx").setLevel(logging.WARNING)


# Goal: () -> int
def get_chat_id(update: Update):
    return update.effective_chat.id


# Goal: str -> void
def send_message(update: Update, context: ContextTypes.DEFAULT_TYPE, message: str):
    context.bot.send_message(chat_id=update.effective_chat.id, text=message)


# Goal: str x bytes -> void
def send_photo(
    update: Update, context: ContextTypes.DEFAULT_TYPE, message: str, photo: bytes
):
    context.bot.send_photo(
        chat_id=update.effective_chat.id, photo=photo, caption=message
    )


# Goal: () -> LatLong
def get_location(update: Update):
    return LatLong(update.message.location.latitude, update.message.location.longitude)


telegram_deps = {
    "chat_id": get_chat_id,
    "send_message": send_message,
    "send_photo": send_photo,
    "get_location": get_location,
}

# def wrapper_function(fn):

#     def inner_function(update: Update, context: ContextTypes.DEFAULT_TYPE):
#         # Resolve each telegram function into the goal form only resolving those which
#         # are required in the fn function.
#         mapping = {
#             "update": update,
#             "context": context
#         }
#         resolved_telegram_deps = {}
#         for function_name, function in telegram_deps.items():
#             parameters_of_telegram_function = inspect.signature(function).parameters

#             telegram_deps_to_inject = {
#                 parameter_name: mapping[parameter_name]
#                 for parameter_name in mapping.keys()
#                 if parameter_name in parameters_of_telegram_function
#             }

#             resolved_telegram_deps[function_name] = functools.partial(args=telegram_deps_to_inject)

#         params = inspect.signature(fn).parameters
#         deps = {
#             name: function
#             for name, function in resolved_telegram_deps.items()
#             if name in params
#         }

#         fn(**deps)

#     return inner_function


def bootstrap():
    pass


# I think this will work. Need to modify the handlers to verfiy this and also
# expand the telegram deps dictionary to include supporting adding a
# reply_markup argument to the send message. Probably call it
# send_message_with_keyboard or something. Handlers will need to take the
# telegram functions as a dependency and then pass them into the handle_search
# method.
