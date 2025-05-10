from itertools import batched
import logging

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes

from tab.core.models import LatLong
from tab.services.observations import (get_aircraft_information,
                                       get_flights_near_user)
from tab.telegram.messages import AircraftInformationCallback, RepeatCallback


async def introduction(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Handler for default message when user chats with the bot.
    """
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="I'm a bot, send me your location to find nearby aircraft!",
    )


async def flight_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logging.info("Flight callback fired")

    data = update.callback_query.data
    if not isinstance(data, AircraftInformationCallback):
        raise ValueError("Flight callback data is not of type string")

    response = await get_aircraft_information(data.name)

    await context.bot.answer_callback_query(callback_query_id=update.callback_query.id)

    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=response.description
    )


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

    if update.message.location is None:
        raise ValueError("Update has no location")

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
    data = await get_flights_near_user(current_pos)
    observations = data.observations
    radar_map = data.radar_map

    logging.info("%d flights nearby" % len(observations))

    if len(observations) == 0:
        await context.bot.send_message(
            chat_id=update.effective_chat.id, text="No aircraft nearby"
        )
    else:
        await context.bot.send_photo(chat_id=update.effective_chat.id, photo=radar_map)

        for f in sorted(observations, key=lambda o: o.ground_distance):
            buttons = [[InlineKeyboardButton(
                "Info", callback_data=AircraftInformationCallback(f.aircraft)
            )]]
            reply_markup = InlineKeyboardMarkup(buttons)

            message = f"{f.callsign}\n{f.aircraft}\n{f.origin}->{f.destination}\nFlying:{convert_bearing_to_eight_point_cardinal(f.heading)}\nLook:{convert_bearing_to_eight_point_cardinal(f.relative_angle)}\nDistance:{round(f.ground_distance)}km"
            if f.photo:
                await context.bot.send_photo(
                    chat_id=update.effective_chat.id, photo=f.photo, caption=message, reply_markup=reply_markup
                )
            else:
                await context.bot.send_message(
                    chat_id=update.effective_chat.id, text=message, reply_markup=reply_markup
                )

    message = f"{len(observations)} flights nearby. Click a button to view more information about a flight, or repeat the search"

    await context.bot.send_message(
        chat_id=update.effective_chat.id, text=message
    )

    logging.info("Handler completed")


def convert_bearing_to_eight_point_cardinal(bearing: float):
    if bearing < 0:
        bearing += 360

    compass_brackets = ["N", "NE", "E", "SE", "S", "SW", "W", "NW", "N"]

    compass_lookup = round(bearing / 45)
    return compass_brackets[compass_lookup]


async def invalid_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.callback_query.answer(
        text="This button has expired. Send me your location to start again.",
        show_alert=True,
    )

async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="An error occurred. Please try again.")
