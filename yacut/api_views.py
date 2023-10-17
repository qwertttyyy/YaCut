import re

from flask import jsonify, request

from . import app
from .constants import CUSTOM_ID_REGEX
from .error_handlers import InvalidAPIUsage
from .models import URLMap
from .views import create_url


@app.route('/api/id/<id>/', methods=['GET'])
def get_url(id):
    url_object = URLMap.query.filter_by(short=id).first()
    if url_object:
        return jsonify({'url': url_object.original})
    raise InvalidAPIUsage('Указанный id не найден', 404)


@app.route('/api/id/', methods=['POST'])
def add_url():
    data = request.get_json()
    short = None
    if not data:
        raise InvalidAPIUsage('Отсутствует тело запроса')
    if 'url' not in data:
        raise InvalidAPIUsage('\"url\" является обязательным полем!')
    if 'custom_id' in data:
        custom_id = data['custom_id']
        if not re.fullmatch(CUSTOM_ID_REGEX, custom_id if custom_id else ''):
            raise InvalidAPIUsage(
                'Указано недопустимое имя для короткой ссылки'
            )
        if URLMap.query.filter_by(short=custom_id).first():
            raise InvalidAPIUsage(
                'Предложенный вариант короткой ссылки уже существует.'
            )
        short = custom_id
    short_link = create_url(data['url'], short)
    return jsonify({'url': data['url'], 'short_link': short_link}), 201
