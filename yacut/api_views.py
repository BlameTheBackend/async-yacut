from flask import request, jsonify

from . import app, db
from .error_handlers import InvalidAPIUsage
from .models import URLMap
from .url_shrinker import get_unique_short_id


@app.route('/api/id/', methods=['POST'])
def create_short_link():
    data = request.get_json(silent=True)
    if data is None:
        raise InvalidAPIUsage('Отсутствует тело запроса', 400)
    custom_id = data.get('custom_id') or get_unique_short_id()
    try:
        urlmap = URLMap(
            original=data.get('url'),
            short=custom_id
        )
        db.session.add(urlmap)
        db.session.commit()
        return jsonify({
            'url': urlmap.original,
            'short_link': f'{request.host_url.rstrip('/')}/{custom_id}'
        }), 201
    except ValueError as e:
        raise InvalidAPIUsage(str(e), 400)


@app.route('/api/id/<string:short_id>/', methods=['GET'])
def get_original_link(short_id):
    try:
        urlmap = URLMap.query.filter_by(short=short_id).first()
        if urlmap is None:
            return jsonify({
                'message': 'Указанный id не найден'
            }), 404
    except ValueError as e:
        return InvalidAPIUsage(str(e), 404)
    return jsonify({
        'url': urlmap.original
    }), 200
