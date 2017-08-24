#!/bin/bash
source {{ telegram_bot_virtual_env_location }}/bin/activate
cd {{ telegram_checkout_location }}
nohup python start_telegram_bot.py >> /dev/null 2>&1&
