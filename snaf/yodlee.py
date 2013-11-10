import urllib2
import urllib
import simplejson

AUTHORIZE_CO_BRAND = "https://rest.developer.yodlee.com/services/srest/restserver/v1.0/authenticate/coblogin"
COB_LOGIN = "sbCobbillpull"
COB_PASSWORD = "fec85d5d-8426-41dd-8774-c4f33de1dcef"


LOGIN = "https://rest.developer.yodlee.com/services/srest/restserver/v1.0/authenticate/login"
USER_LOGIN = "sbMembillpull1"
USER_PASSWORD = "sbMembillpull1#123"

SEARCH = "https://rest.developer.yodlee.com/services/srest/restserver/v1.0/jsonsdk/SiteTraversal/searchSite"

SITE_ACCOUNT = "https://rest.developer.yodlee.com/services/srest/restserver/v1.0/jsonsdk/SiteAccountManagement"


def authenticate_yodlee():
	req = urllib2.Request(AUTHORIZE_CO_BRAND)

	req.add_data(urllib.urlencode({
			'cobrandLogin': COB_LOGIN,
			'cobrandPassword': COB_PASSWORD
		}))


	res = simplejson.loads(urllib2.urlopen(req).read())

	return res['cobrandConversationCredentials']['sessionToken']

def login_user(session_token):
	data = {
		'login': USER_LOGIN,
		'password': USER_PASSWORD,
		'cobSessionToken': session_token
	}

	req = urllib2.Request(LOGIN)

	req.add_data(urllib.urlencode(data))

	res = simplejson.loads(urllib2.urlopen(req).read())

	return res['userContext']['conversationCredentials']['sessionToken']

def search_yodlee(session_token, user_session_token, search_query):
	data = {
		'cobSessionToken': session_token,
		'userSessionToken': user_session_token,
		'siteSearchString': search_query
	}

	req = urllib2.Request(SEARCH)

	req.add_data(urllib.urlencode(data))

	res = simplejson.loads(urllib2.urlopen(req).read())

	return res

def get_site_login(session_token, user_session_token, site_id):
	data = {
		'cobSessionToken': session_token,
		'userSessionToken': user_session_token,
		'siteId': site_id
	}

	req = urllib2.Request(SITE_ACCOUNT)

	req.add_data(urllib.urlencode(data))

	res = simplejson.loads(urllib2.urlopen(req).read())

	return res