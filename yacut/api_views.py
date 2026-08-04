from flask import request, jsonify
from http import HTTPStatus

from . import app, db
from .contstants import MAX_LENGTH_SHORT_LINK, ALLOWED_CHARS
from .error_handlers import InvalidAPIUsage
from .models import URLMap
from .url_shrinker import get_unique_short_id


@app.route('/api/id/', methods=['POST'])
def create_short_link():
    data = request.get_json(silent=True)
    if data is None:
        raise InvalidAPIUsage(
            'Отсутствует тело запроса', HTTPStatus.BAD_REQUEST)
    if 'url' not in data:
        raise InvalidAPIUsage(
            '"url" является обязательным полем!', HTTPStatus.BAD_REQUEST)
    custom_id = data.get('custom_id')
    if custom_id:
        if (
            len(custom_id) > MAX_LENGTH_SHORT_LINK
            or not ALLOWED_CHARS.fullmatch(custom_id)
        ):
            raise InvalidAPIUsage(
                'Указано недопустимое имя для короткой ссылки')
        if URLMap.query.filter_by(short=custom_id).first() is not None:
            raise InvalidAPIUsage(
                'Предложенный вариант короткой ссылки уже существует.',
                HTTPStatus.BAD_REQUEST
            )
    else:
        custom_id = get_unique_short_id()
    urlmap = URLMap(
        original=data.get('url'),
        short=custom_id
    )
    db.session.add(urlmap)
    db.session.commit()
    return jsonify({
        'url': urlmap.original,
        'short_link': f'{request.host_url.rstrip("/")}/{custom_id}'
    }), HTTPStatus.CREATED


@app.route('/api/id/<string:short_id>/', methods=['GET'])
def get_original_link(short_id):
    urlmap = URLMap.query.filter_by(short=short_id).first()
    if urlmap is None:
        return jsonify({
            'message': 'Указанный id не найден'
        }), HTTPStatus.NOT_FOUND
    return jsonify({
        'url': urlmap.original
    }), HTTPStatus.OK
