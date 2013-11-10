import urllib2
import simplejson

XIGNITE_TOKEN = "01982C1733DF487A9F5127F1AE36C412"
XIGNITE_ENDPOINT = "http://www.xignite.com/xEarningsCalendar.json/GetAnnouncement?Identifier=%s&IdentifierType=Symbol&_Token=%s"

def get_xignite_events(symbol):
	endpoint = XIGNITE_ENDPOINT % (symbol, XIGNITE_TOKEN)

	request = urllib2.urlopen(endpoint)

	return simplejson.loads(request.read())
