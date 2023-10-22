import re

from flask import jsonify, request

from . import app
from .constants import CUSTOM_ID_REGEX
from .error_handlers import InvalidAPIUsage
from .services import URL


@app.route('/api/id/<id>/', methods=['GET'])
def get_url(id):
    url_object = URL().get_url(id)
    if url_object:
        return jsonify({'url': url_object.original})
    raise InvalidAPIUsage('Указанный id не найден', 404)


@app.route('/api/id/', methods=['POST'])
def add_url():
    data = URL(request.get_json()).get_data()
    if not data:
        raise InvalidAPIUsage('Отсутствует тело запроса')
    if not data.url:
        raise InvalidAPIUsage('\"url\" является обязательным полем!')
    if data.custom_id:
        if not re.fullmatch(
            CUSTOM_ID_REGEX, data.custom_id if data.custom_id else ''
        ):
            raise InvalidAPIUsage(
                'Указано недопустимое имя для короткой ссылки'
            )
        if data.get_url():
            raise InvalidAPIUsage(
                'Предложенный вариант короткой ссылки уже существует.'
            )
    return jsonify({'url': data.url, 'short_link': data.get_short_link()}), 201
