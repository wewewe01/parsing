#!/bin/bash


# Открыть фейковый порт, чтобы Render "успокоился"
python3 -m http.server 8080 &

# Запуск Telegram-бота
Xvfb :99 -screen 0 1024x768x16 &
export DISPLAY=:99
python bot.py
