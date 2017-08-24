import urllib
import json
import ConfigParser
import sys

try:
    result = json.load(urllib.urlopen("http://172.16.2.102:25678/garage/status/all"))
except:
    print "Error while accessing API"
    sys.exit(2)
else:
    exit_code = 0
    all_statuses = {s['status'] for s in result}
    if 'OPEN' in all_statuses:
        exit_code = 2
    
    ret_message = ""
    for one_garage in result:
        ret_message += "{0}-{1}...".format(one_garage['garage_name'], one_garage['status'])

    print(ret_message)
    sys.exit(exit_code)

