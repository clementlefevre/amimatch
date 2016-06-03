import pdb
from flask import render_template, abort, request, \
    current_app
from flask.ext.sqlalchemy import get_debug_queries

from . import main
import ipdb as ipdb
from app.main.helper.date_converter import update_article
from app.models import Image, User, Article


@main.after_app_request
def after_request(response):
    for query in get_debug_queries():
        if query.duration >= current_app.config['FLASKY_SLOW_DB_QUERY_TIME']:
            current_app.logger.warning(
                'Slow query: %s\nParameters: %s\nDuration: %fs\nContext: %s\n'
                % (query.statement, query.parameters, query.duration,
                   query.context))
    return response


@main.route('/shutdown')
def server_shutdown():
    if not current_app.testing:
        abort(404)
    shutdown = request.environ.get('werkzeug.server.shutdown')
    if not shutdown:
        abort(500)
    shutdown()
    return 'Shutting down...'


@main.route('/user/<username>')
def user(username):
    user = User.query.filter_by(username=username).first_or_404()

    return render_template('user.html', user=user)


@main.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')


@main.route('/images', methods=['GET', 'POST'])
def all_images():
    # images = Image.query.filter(Image.image_caption.contains('min')).all()
    # pattern = http://www.morgenpost.de/printarchiv/nachrichten-vom-15-1-2014
    articles = Article.query.all()
    for article in articles:
        update_article(article)
    ipdb.set_trace()
    return render_template('images.html', images=articles)
