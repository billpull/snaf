import urllib2
import simplejson

STOCK_TWIT_API = "https://api.stocktwits.com/api/2/streams/symbol/%s.json"

def get_twits(symbol):
	request = urllib2.urlopen(STOCK_TWIT_API % symbol)

	return simplejson.loads(request.read())