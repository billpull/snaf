import urllib2
import simplejson

DOW_JONES_API = "http://betawebapi.dowjones.com/fintech/articles/api/v1/instrument/%s"

def get_articles(symbol):
	request = urllib2.urlopen(DOW_JONES_API % symbol)

	return simplejson.loads(request.read())