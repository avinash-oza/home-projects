import urllib
import urllib2
import json
import ConfigParser
import sys

config = ConfigParser.ConfigParser()
config.read('airvpn.config')

API_KEY = config.get('AIRVPN', 'API_KEY')
URL = 'http://localhost:25003/submit_check'

exit_code = "0"
output_text = ""

try:
    result = json.load(urllib.urlopen("https://airvpn.org/api/?service=userinfo&format=json&key={0}".format(API_KEY)))
except:
    output_text= "Error while accessing API"
    exit_code = "2"
else:
    num_sessions = 0
    if 'sessions' in result:
        num_sessions = len(result['sessions'])

    if num_sessions < 2:
        exit_code = "2"
    vpn_ips = '|'.join(','.join([s['vpn_ip'], s['server_location'], s['connected_since_date']]) for s in result['sessions'])
    output_text = "Number of sessions: {0} {1}...{2}".format(num_sessions, "less than 2" if num_sessions < 2 else "", vpn_ips)

passive_check_result = [dict(hostname='monitoring-station',service_description='AirVPN Status', return_code=exit_code,plugin_output=output_text)]

# Create and post request
req = urllib2.Request(URL)
req.add_header('Content-Type', 'application/json')

response = urllib2.urlopen(req, json.dumps(passive_check_result))

