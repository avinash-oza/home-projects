#! /bin/bash
cd /usr/lib/nagios/plugins/case_temperature
source /home/telegram-bot/telegram-virtual-env/bin/activate
python get_temperature.py --case
