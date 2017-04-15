#!/bin/bash
source {{ telegram_bot_virtual_env_location }}/bin/activate
cd {{ telegram_checkout_location }}
python start_telegram_bot.py
