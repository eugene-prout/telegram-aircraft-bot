import logging
from telegram import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Update,
)
from telegram.ext import (
    ContextTypes,
)
from bot.types import AircraftInformationCallback, RepeatCallback


from bot.services import (
    GetAircraftInformation,
    GetFlights,
    LatLong,
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
    if not isinstance(data, AircraftInformationCallback):
        raise ValueError("Flight callback data is not of type string")

    summary = GetAircraftInformation(data.name).description

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

    current_pos = LatLong(
        update.message.location.latitude, update.message.location.longitude
    )
    await handle_search(current_pos, context, update)


async def handle_search(
    current_pos: LatLong,
    context: ContextTypes.DEFAULT_TYPE,
    update: Update,
):
    """
    Handler for the core functionality of the bot.
    """
    data = GetFlights(current_pos)
    observations = data.observations
    radar_map = data.radar_map

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
        buttons = [
            InlineKeyboardButton(
                index, callback_data=AircraftInformationCallback(flight.aircraft)
            )
            for index, flight in row
        ]
        keyboard_rows.append(buttons)

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


async def invalid_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.callback_query.answer(
        text="This button has expired. Send me your location to start again.",
        show_alert=True,
    )
