#! /bin/bash
cd /usr/local/nagios/libexec/case_temperature
source /etc/bash_completion.d/virtualenvwrapper
source /home/asterisk/.virtualenvs/telegram-bot/bin/activate
python get_temperature.py
