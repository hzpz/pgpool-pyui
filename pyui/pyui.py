"""pgpool-pyui"""
import logging

from flask import Flask, render_template, request, g

from pyui import model

logging.basicConfig(level=logging.INFO)
logging.getLogger('werkzeug').setLevel(logging.WARNING)
LOG = logging.getLogger(__name__)

LOG.info("Initializing Flask app")
APP = Flask(__name__)
APP.config.from_pyfile('../pgpool-pyui.cfg')
model.init_db(APP.config['DATABASE_URL'])


@APP.before_request
def _before_request():
    g.db = model.DATABASE
    g.db.get_conn()  # opens the connection if and only if the connection is not already open


@APP.after_request
def _after_request(response):
    g.db.close()
    return response


@APP.route('/accounts')
def show_accounts():
    """Returns a list of all accounts"""
    accounts = _get_accounts(_get_order(request))
    return render_template('accounts.html', accounts=accounts, build_sort_query=_build_sort_query)


@APP.route('/account/<username>/events')
def acount_events(username):
    """Returns details of the account with the given username"""
    events = _get_events(username)
    return render_template('events.html', username=username, events=events)


def _build_sort_query(_request, order_by):
    if not _request.args.get('order_by') == order_by:
        return 'order_by=' + order_by
    else:
        return 'order_by=' + order_by + '&direction=' + _invert_direction(_request)


def _invert_direction(_request):
    current_direction = _get_direction(_request)
    if current_direction == 'desc':
        return 'asc'
    else:
        return 'desc'


def _get_direction(_request):
    return 'desc' if _request.args.get('direction') == 'desc' else 'asc'


def _get_order(_request):
    order_by = _request.args.get('order_by') or 'username'
    direction = _get_direction(request)
    order_by_field = getattr(model.Account, order_by, None)
    if order_by_field:
        return getattr(order_by_field, direction)()
    else:
        return None


def _get_accounts(order_by=None):
    return model.Account \
        .select() \
        .where(model.Account.level > 0) \
        .order_by(order_by)


def _get_events(username):
    return model.Event \
        .select(model.Event, model.Account) \
        .join(model.Account) \
        .where(model.Account.username == username) \
        .order_by(model.Event.timestamp.desc())


if __name__ == '__main__':
    APP.run(debug=True)
