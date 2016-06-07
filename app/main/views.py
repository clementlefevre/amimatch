import json

from flask import render_template, abort, request, \
    current_app
from flask.ext.login import login_required
from flask.ext.sqlalchemy import get_debug_queries

from . import main
from app.main.forms import DateRangeForm
from app.main.service.images_service import find_images, find_images_by_name
from app.models import User


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
@login_required
def index():
    return render_template('index.html')


@main.route('/images/<string:name>', methods=['GET'])
def all_images(name):
    result = json.dumps(find_images_by_name(name))
    return result


@main.route('/search_images', methods=['GET', 'POST'])
@login_required
def search_images():
    form = DateRangeForm(request.form)

    if request.method == 'POST' and form.validate():
        images = find_images(form)
        return render_template('images.html', images=images)

    return render_template('search_images.html', form=form)
