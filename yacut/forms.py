from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length, Optional, URL, Regexp

from .constants import SHORT_LINK_VALIDATION_REGEX, MAX_SHORT_LINK_LENGTH


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
            Length(1, MAX_SHORT_LINK_LENGTH),
            Regexp(
                SHORT_LINK_VALIDATION_REGEX,
                message='Некорректная короткая ссылка',
            ),
            Optional(),
        ],
    )
    create = SubmitField('Создать')
