import urllib
import json
import ConfigParser
import sys

config = ConfigParser.ConfigParser()
config.read('airvpn.config')

API_KEY = config.get('AIRVPN', 'API_KEY')

try:
    result = json.load(urllib.urlopen("https://airvpn.org/api/?service=userinfo&format=json&key={0}".format(API_KEY)))
except:
    print "Error while accessing API"
    sys.exit(2)
else:
    if(len(result['sessions']) < 2):
        print "Number of sessions {0} less than 2".format(len(result['sessions']))
        sys.exit(2)
    print "Number of sessions: {0}".format(len(result['sessions']))
    sys.exit(0)

