cd /home/pi//home-projects/pi/
source /etc/bash_completion.d/virtualenvwrapper
source /home/asterisk/.virtualenvs/telegram-bot/bin/activate
python get_temperature.py
exit $?
