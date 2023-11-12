import logging
import uuid
from telegram import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Message,
    Update,
)
from telegram.ext import (
    ContextTypes,
)
from bot.types import RepeatCallback

import wikipedia

from bot.services import (
    FlightObservation,
    LatLong,
    get_flights_near_user,
    convert_bearing_to_eight_point_cardinal,
)


async def introduction(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Handler for default message when user chats with the bot.
    """
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="I'm a bot, send me your location to find nearby aircraft!",
    )

# Upgrading to Python 3.12 would put this functionality into itertools, but 3.12 breaks python-telegram-bot.
def batch(iterable, n=1):
    l = len(iterable)
    for ndx in range(0, l, n):
        yield iterable[ndx : min(ndx + n, l)]

async def flight_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logging.info("Flight callback fired")

    data = update.callback_query.data
    if not isinstance(data, FlightObservation):
        raise ValueError("Flight callback data is not of type FlightObservation")

    summary = wikipedia.summary(data.aircraft)

    await context.bot.send_message(chat_id=update.effective_chat.id, text=summary)


async def repeat_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Handler for repeat search callback function. Expects callback data to be RepeatCallback.
    """
    data = update.callback_query.data
    current_pos = LatLong(data.latitude, data.longitude)

    await handle_search(current_pos, context, update)


async def location(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Handler for user sending a location to the bot.
    """
    logging.info("Location message being handled")

    if update.message is None:
        raise ValueError("Update has no message")

    current_pos = LatLong(update.message.location.latitude, update.message.location.longitude)
    await handle_search(current_pos, context, update)


async def handle_search(
    current_pos: LatLong,
    context: ContextTypes.DEFAULT_TYPE,
    update: Update,
):
    """
    Handler for the core functionality of the bot. 
    """
    observations, radar_map = get_flights_near_user(current_pos)

    logging.info("%d flights nearby" % len(observations))

    if len(observations) == 0:
        await context.bot.send_message(
            chat_id=update.effective_chat.id, text="No aircraft nearby"
        )
    else:
        # Send radar photo.
        await context.bot.send_photo(chat_id=update.effective_chat.id, photo=radar_map)
        
        # Send flight details and photo, if available.
        for i, f in enumerate(observations, 1):
            message = f"{i}: {f.aircraft}\n{f.origin}->{f.destination}\nFlying:{convert_bearing_to_eight_point_cardinal(f.heading)}\nLook:{convert_bearing_to_eight_point_cardinal(f.relative_angle)}\nDistance:{round(f.ground_distance)}km"
            if f.photo:
                await context.bot.send_photo(
                    chat_id=update.effective_chat.id, photo=f.photo, caption=message
                )
            else:
                await context.bot.send_message(
                    chat_id=update.effective_chat.id, text=message
                )

    # Show the user inline keyboard buttons to send a callback message about the flight.
    # We want to display up to 4 buttons in a row for the flight information.
    # Finally add a row solely for the repeat button.
    flight_rows = batch(list(enumerate(observations, 1)), n=4)
    keyboard_rows = []
    for row in flight_rows:
        keyboard_rows.append(
            [InlineKeyboardButton(index, callback_data=flight) for index, flight in row]
        )

    keyboard_rows.append(
        [
            InlineKeyboardButton(
                "Repeat",
                callback_data=RepeatCallback(
                    current_pos.latitude, current_pos.longitude
                ),
            )
        ]
    )

    reply_markup = InlineKeyboardMarkup(keyboard_rows)

    message = f"{len(observations)} flights nearby. Click a button to view more information about a flight, or repeat the search"

    await context.bot.send_message(
        chat_id=update.effective_chat.id, text=message, reply_markup=reply_markup
    )

    logging.info("Handler completed")
