#!/bin/bash
cd /usr/local/nagios/libexec/route53
source /home/nagios/.virtualenvs/python-aws/bin/activate
python dyndns_route53.py
exit $?

