# Telegram Aircraft Bot

[![Python](https://img.shields.io/badge/Python-3.13-blue.svg)](https://www.python.org/)
[![Vue](https://img.shields.io/badge/Vue.js-3.x-brightgreen.svg)](https://vuejs.org/)

Telegram Aircraft Bot is a project that provides a simple visualisation of nearby aircraft.

When given your location, the bot returns a list of nearby aircraft and overlays their positions on a map of your area.

Code structure:

- `api`: Python backend wraps ADS-B services and geenrates flight radar map images.
- `frontend`: Web frontend build with Vue, offering a browser-based interface.
- `telegram`: Telegram bot build with Python, providing the Telegram user interaction.
