import hashlib
from datetime import datetime

from snaf.core import snaf_hash
from snaf.core import db
from snaf import app


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(65), unique=True, nullable=False)
    password = db.Column(db.String(65), nullable=False)
    created_date = db.Column(db.DateTime, nullable=False)

    db.UniqueConstraint(email, name='uix_email')

    def __init__(self, email, password):
        self.email = email
        self.created_date = datetime.utcnow()

        salt = hashlib.md5()
        salt.update(email)
        salt.update(self.created_date.strftime('%Y-%m-%d %H:%M:%S'))
        salt.update(password)

        hash_combo = "%s %s" % (snaf_hash, salt.hexdigest())

        self.password = hashlib.sha224(hash_combo).hexdigest()

    def __repr__(self):
        return '<User %r: %r>' % (self.id, self.email)


class UserAccount(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    name = db.Column(db.String(65), nullable=False)
    yodlee_credentials = db.Column(db.String(255), nullable=False)
    created_date = db.Column(db.DateTime, nullable=False)
    authenticated = db.Column(db.Boolean, nullable=False)

    db.ForeignKeyConstraint(
        ['user_id'],
        ['user.id'],
        use_alter=True,
        name='fk_account_user_id'
    )

    def __init__(self, user_id, name, yodlee_credentials, authenticated):
        self.user_id = user_id
        self.name = name
        self.yodlee_credentials = yodlee_credentials
        self.authenticated = authenticated

        self.created_date = datetime.utcnow()

    def __repr__(self):
        return '<UserAccount %r: User(%r) %r>' % (self.id, self.user_id, self.name)


class UserAccountSymbol(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_account_id = db.Column(db.Integer, nullable=False)
    symbol = db.Column(db.String(65), nullable=False)
    created_date = db.Column(db.DateTime, nullable=False)

    db.ForeignKeyConstraint(
        ['user_account_id'],
        ['user_account.id'],
        use_alter=True,
        name='fk_symbol_account_id'
    )

    db.UniqueConstraint(user_account_id, symbol, name='uix_symbol_user_account')

    def __init__(self, user_account_id, symbol):
        self.user_account_id = user_account_id
        self.symbol = symbol

        self.created_date = datetime.utcnow()

    def __repr__(self):
        return '<UserAccountSymbol %r: UserAccount(%r) %r>' % (self.id, self.user_account_id, self.symbol)


class EventType(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(65), nullable=False)
    description = db.Column(db.String(255), nullable=False)

    def __init__(self, name, description):
        self.name = name
        self.description = description

    def __repr__(self):
        return '<EventType %r: %r>' % (self.id, self.name)


class SymbolEvent(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    event_type_id = db.Column(db.Integer, nullable=False)
    user_account_symbol_id = db.Column(db.Integer, nullable=False)
    title = db.Column(db.String(65), nullable=False)
    content = db.Column(db.String(255), nullable=False)
    sentiment = db.Column(db.Integer)
    created_date = db.Column(db.DateTime, nullable=False)

    db.ForeignKeyConstraint(
        ['event_type_id'],
        ['event_type.id'],
        use_alter=True,
        name='fk_symbol_event_type_id'
    )

    db.ForeignKeyConstraint(
        ['user_account_symbol_id'],
        ['user_account_symbol.id'],
        use_alter=True,
        name='fk_symbol_event_symbol_id'
    )

    def __init__(self, event_type, symbol_id, title, content, sentiment):
        self.event_type_id = event_type
        self.user_account_symbol_id = symbol_id
        self.title = title
        self.content = content
        self.sentiment = sentiment

        self.created_date = datetime.utcnow()

    def __repr__(self):
        return '<SymbolEvent %r: EventType(%r) %r>' % (self.id, self.event_type_id, self.title)


class AlertType(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(65), nullable=False)
    description = db.Column(db.String(255), nullable=False)

    def __init__(self, name, description):
        self.name = name
        self.description = description

    def __repr__(self):
        return '<AlertType %r: %r>' % (self.id, self.name)


class AlertChannel(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(65), nullable=False)

	def __init__(self, name):
		self.name = name

	def __repr__(self):
		return '<AlertChannel %r: %r>' % (self.id, self.name)


class UserAlert(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    alert_type_id = db.Column(db.Integer, nullable=False)
    alert_channel_id = db.Column(db.Integer, nullable=False)
    trigger = db.Column(db.Integer, nullable=False)
    created_date = db.Column(db.DateTime, nullable=False)
    last_updated = db.Column(db.DateTime)

    db.ForeignKeyConstraint(
        ['user_id'],
        ['user.id'],
        use_alter=True,
        name='fk_alert_user_id'
    )

    db.ForeignKeyConstraint(
        ['alert_type_id'],
        ['alert_type.id'],
        use_alter=True,
        name='fk_user_alert_type_id'
    )

    db.ForeignKeyConstraint(
        ['alert_channel_id'],
        ['alert_channel.id'],
        use_alter=True,
        name='fk_user_alert_channel_id'
    )

    def __init__(self, user_id, alert_type_id, trigger):
        self.user_id = user_id
        self.alert_type_id = alert_type_id
        self.trigger = trigger

        self.created_date = datetime.utcnow()

    def __repr__(self):
        return '<UserAlert %r: AlertType(%r) %r>' % (self.id, self.alert_type_id, self.trigger)

# models for which we want to create API endpoints
app.config['API_MODELS'] = {
    'user': User,
    'userAccount': UserAccount,
    'userAccountSymbol': UserAccountSymbol,
    'userAlert': UserAlert,
    'symbolEvent': SymbolEvent,
    'eventType': EventType,
    'alertType': AlertType,
    'alertChannel': AlertChannel
}

# models for which we want to create CRUD-style URL endpoints,
# and pass the routing onto our AngularJS application
app.config['CRUD_URL_MODELS'] = {
    'user': User,
    'userAccount': UserAccount,
    'userAccountSymbol': UserAccountSymbol,
    'userAlert': UserAlert,
    'symbolEvent': SymbolEvent,
    'eventType': EventType,
    'alertType': AlertType,
    'alertChannel': AlertChannel
}
