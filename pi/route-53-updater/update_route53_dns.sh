#!/bin/bash
cd /usr/lib/nagios/plugins/route-53-updater
source /home/asterisk/.virtualenvs/python-aws/bin/activate
python dyndns_route53.py
exit $?

