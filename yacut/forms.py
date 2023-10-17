from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length, Optional, URL, Regexp

from yacut.constants import CUSTOM_ID_REGEX, CUSTOM_ID_LENGTH


class URLForm(FlaskForm):
    original_link = StringField(
        'Длинная ссылка',
        validators=[
            DataRequired(message='Обязательное поле'),
            URL(message='Некорректная ссылка'),
        ],
    )
    custom_id = StringField(
        'Ваш вариант короткой ссылки',
        validators=[
            Length(1, CUSTOM_ID_LENGTH),
            Regexp(CUSTOM_ID_REGEX, message='Некорректная короткая ссылка'),
            Optional(),
        ],
    )
    create = SubmitField('Создать')
