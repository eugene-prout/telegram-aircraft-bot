import logging
from telegram import Update
from telegram.ext import (
    ContextTypes,
)
from bot.bearing import convert_bearing_to_cardinal

from bot.flights import create_flight_observations, get_flights_in_box, load_flight_data
from bot.translate import create_box


async def introduction(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="I'm a bot, send me your location to find nearby aircraft!",
    )


async def location(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logging.info("Location message being handled")
    current_pos = (update.message.location.latitude, update.message.location.longitude)

    flights = create_flight_observations(
        load_flight_data(get_flights_in_box(*create_box(current_pos))), current_pos
    )

    logging.info("%d flights nearby" % len(flights))

    if len(flights) == 0:
        await context.bot.send_message(
            chat_id=update.effective_chat.id, text="No aircraft nearby"
        )
    else:
        for i, f in enumerate(flights, 1):
            message = f"{i}: {f.aircraft}\n{f.origin}->{f.destination}\nFlying:{convert_bearing_to_cardinal(f.heading)}\nLook:{convert_bearing_to_cardinal(f.relative_angle)}\nDistance:{round(f.ground_distance)}km"
            if f.photo:
                await context.bot.send_photo(
                    chat_id=update.effective_chat.id, photo=f.photo, caption=message
                )
            else:
                await context.bot.send_message(
                    chat_id=update.effective_chat.id, text=message
                )
    logging.info("Handler completed")