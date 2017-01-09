#! /bin/bash
cd /usr/lib/nagios/plugins/case_temperature
source /etc/bash_completion.d/virtualenvwrapper
source /home/asterisk/.virtualenvs/telegram-bot/bin/activate
python get_temperature.py --case
