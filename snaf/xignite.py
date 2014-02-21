import urllib2
import simplejson

XIGNITE_TOKEN = "XIGNITE_API_TOKEN"
XIGNITE_ENDPOINT = "http://www.xignite.com/xEarningsCalendar.json/GetAnnouncement?Identifier=%s&IdentifierType=Symbol&_Token=%s"

def get_xignite_events(symbol):
	endpoint = XIGNITE_ENDPOINT % (symbol, XIGNITE_TOKEN)

	request = urllib2.urlopen(endpoint)

	return simplejson.loads(request.read())
