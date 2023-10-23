import re
from random import choice
from string import ascii_letters, digits

from flask import url_for

from yacut.constants import (
    GENERATED_SHORT_LINK_LENGTH,
    SHORT_LINK_VALIDATION_REGEX,
)
from .models import URLMap
from . import db
from .exceptions import (
    EmptyDataError,
    NoRequiredParameterError,
    ValidationError,
)


class URL:
    def __init__(self, data=None, url=None, custom_id=None):
        self.data = data
        if self.data:
            self.url = self.data.get('url')
            self.custom_id = self.data.get('custom_id')
        else:
            self.url = url
            self.custom_id = custom_id

    def get_url(self, short_id=None):
        return URLMap.query.filter_by(
            short=short_id if short_id else self.custom_id
        ).first()

    def get_short_link(self):
        if not self.data and not self.url and not self.custom_id:
            raise EmptyDataError()
        if not self.url:
            raise NoRequiredParameterError()
        if self.custom_id:
            if not re.fullmatch(
                SHORT_LINK_VALIDATION_REGEX,
                self.custom_id if self.custom_id else '',
            ):
                raise ValidationError()
        else:
            self.custom_id = self.get_unique_short_id()
            while self.get_url():
                self.custom_id = self.get_unique_short_id()
        new_url_object = URLMap(original=self.url, short=self.custom_id)
        db.session.add(new_url_object)
        db.session.commit()
        return url_for('redirect_view', id=self.custom_id, _external=True)

    @staticmethod
    def get_unique_short_id():
        chars = ascii_letters + digits
        id = ''.join(choice(chars) for _ in range(GENERATED_SHORT_LINK_LENGTH))
        return id
