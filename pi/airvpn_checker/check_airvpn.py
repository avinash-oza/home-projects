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
    if(len(result['sessions']) < 2):
        print "Number of sessions {0} less than 2".format(len(result['sessions']))
        exit_code = "2"
    output_text = "Number of sessions: {0}".format(len(result['sessions']))

passive_check_result = [dict(hostname='monitoring-station',service_description='AirVPN Status', return_code=exit_code,plugin_output=output_text)]

# Create and post request
req = urllib2.Request(URL)
req.add_header('Content-Type', 'application/json')

response = urllib2.urlopen(req, json.dumps(passive_check_result))

