import os

from flask import Flask, request, Response
from flask import render_template, url_for, redirect, send_from_directory
from flask import send_file, make_response, abort
from flask import jsonify

from snaf import app

# routing for API endpoints (generated from the models designated as API_MODELS)
from snaf.core import api_manager
from snaf import stocktwit
from snaf import dowjones
from snaf import xignite
from snaf import yodlee

from snaf.models import *

for model_name in app.config['API_MODELS']:
	model_class = app.config['API_MODELS'][model_name]
	api = api_manager.create_api(model_class, collection_name=model_name, methods=['GET', 'POST'])

session = api_manager.session

# routing for basic pages (pass routing onto the Angular app)
@app.route('/')
@app.route('/events')
@app.route('/topics')
@app.route('/account')
def basic_pages(**kwargs):
	return render_template('index.html')

@app.route('/api/twits/<symbol>')
def twit_controller(symbol, **kwargs):

	return jsonify(stocktwit.get_twits(symbol))

@app.route('/api/broker/<broker>')
def broker_controller(broker, **kwargs):
	yodlee_session = yodlee.authenticate_yodlee()
	yodlee_user_session = yodlee.login_user(yodlee_session)
	yodlee_search_results = yodlee.search_yodlee(yodlee_session, yodlee_user_session, broker)

	data = {
		'searchResults': yodlee_search_results
	}

	return jsonify(data)

@app.route('/api/feed')
def feed_controller(**kwargs):
	"""
		API For Fetching Feed Items
	"""
	feed_items = []
	user_account_ids = [ua.id for ua in session.query(UserAccount)
					.filter(UserAccount.user_id == 1)
					.all()]

	user_symbols = set([us.symbol for us in session.query(UserAccountSymbol)
												.filter(UserAccountSymbol.user_account_id.in_(user_account_ids))
												.all()])

	
	data = {
		'articles': []
	}

	for sym in user_symbols:
		dow_articles = dowjones.get_articles(sym)['Headlines']
		mod_articles = []

		for article in dow_articles:
			article['SnafSymbol'] = sym

			mod_articles.append(article)

		data['articles'] += mod_articles
		

	return jsonify(data)

@app.route('/api/topic')
def topic_controller(**kwargs):
	"""
		API For Fetching Feed Items
	"""
	feed_items = []
	user_account_ids = [ua.id for ua in session.query(UserAccount)
					.filter(UserAccount.user_id == 1)
					.all()]

	user_symbols = set([us.symbol for us in session.query(UserAccountSymbol)
												.filter(UserAccountSymbol.user_account_id.in_(user_account_ids))
												.all()])

	
	topics = {
		'name': 'Trending Topics',
		'children': []
	}

	articles = []
	for sym in user_symbols:
		dow_articles = dowjones.get_articles(sym).setdefault('Headlines',[])

		article = {
			'symbol': sym,
			'articles': dow_articles,
			'size': len(dow_articles)
		}

		articles.append(article)
	
	keywords = {}
	for article in articles:
		sym_keyword = keywords.setdefault(article['symbol'], {
				'keywords': [],
				'size': article['size']
			})

		for headline in article['articles']:
			sym_keyword['keywords'] += headline.setdefault('Keywords', [])
			
		keywords[article['symbol']] = sym_keyword

	for sym in user_symbols:
		kws = keywords[sym]['keywords']
		unique_kws = set(kws)

		sym_topic = {
			'name': sym,
			'children': [],
			'size': keywords[sym]['size']
		}

		for ukw in unique_kws:
			topic = {
				'name': ukw,
				'size': kws.count(ukw)
			}

			sym_topic['children'].append(topic)

		topics['children'].append(sym_topic)

	return jsonify(topics)

@app.route('/api/event')
def event_controller(**kwargs):
	user_account_ids = [ua.id for ua in session.query(UserAccount)
					.filter(UserAccount.user_id == 1)
					.all()]

	user_symbols = set([us.symbol for us in session.query(UserAccountSymbol)
												.filter(UserAccountSymbol.user_account_id.in_(user_account_ids))
												.all()])

	data = {
		'symbol_events': []
	}

	for sym in user_symbols:
		symbol_data = {
			'symbol': sym
		}

		symbol_data['events'] = xignite.get_xignite_events(sym)

		data['symbol_events'].append(symbol_data)

	return jsonify(data)

@app.route('/api/event/<symbol>')
def symbol_event_controller(symbol, **kwargs):

	data = {
		'symbol_events': []
	}

	symbol_event = xignite.get_xignite_events(symbol)

	data['symbol_events'].append({
			'symbol': symbol,
			'events': symbol_event
		})

	return jsonify(data)


# routing for CRUD-style endpoints
# passes routing onto the angular frontend if the requested resource exists
from sqlalchemy.sql import exists

crud_url_models = app.config['CRUD_URL_MODELS']

@app.route('/<model_name>/')
@app.route('/<model_name>/<item_id>')
def rest_pages(model_name, item_id=None):
	if model_name in crud_url_models:
		model_class = crud_url_models[model_name]
		if item_id is None or session.query(exists().where(
			model_class.id == item_id)).scalar():
			return make_response(open(
				'snaf/templates/index.html').read())
	abort(404)

# special file handlers and error handlers
@app.route('/favicon.ico')
def favicon():
	return send_from_directory(os.path.join(app.root_path, 'static'),
							   'img/favicon.ico')

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404



