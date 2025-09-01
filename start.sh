#!/bin/bash
# Запускаем виртуальный дисплей
Xvfb :99 -screen 0 1024x768x16 &
export DISPLAY=:99

# Запускаем Telegram-бота
python bot.py
