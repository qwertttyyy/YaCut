from flask import jsonify, request
from sqlalchemy.exc import IntegrityError

from . import app
from .error_handlers import InvalidAPIUsage
from .exceptions import (
    NoRequiredParameterError,
    ValidationError,
)
from .services import URL


@app.route('/api/id/<id>/', methods=['GET'])
def get_url(id):
    url_object = URL().get_url(id)
    if not url_object:
        raise InvalidAPIUsage('Указанный id не найден', 404)
    return jsonify({'url': url_object.original})


@app.route('/api/id/', methods=['POST'])
def add_url():
    data = request.get_json()
    if not data:
        raise InvalidAPIUsage('Отсутствует тело запроса')
    try:
        short_link = URL(
            data.get('url'), data.get('custom_id')
        ).get_short_link()
    except NoRequiredParameterError:
        raise InvalidAPIUsage('\"url\" является обязательным полем!')
    except ValidationError:
        raise InvalidAPIUsage('Указано недопустимое имя для короткой ссылки')
    except IntegrityError:
        raise InvalidAPIUsage(
            'Предложенный вариант короткой ссылки уже существует.'
        )

    return jsonify({'url': data.get('url'), 'short_link': short_link}), 201
