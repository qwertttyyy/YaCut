from random import choice
from string import ascii_letters, digits

from flask import url_for

from yacut.constants import ID_SIZE
from yacut.forms import URLForm
from yacut.models import URLMap
from . import db


class URL:
    def __init__(self, data=None):
        self.data = data
        self.url = None
        self.custom_id = None

    def get_data(self):
        if not self.data:
            return None
        if isinstance(self.data, URLForm):
            self.url = self.data.original_link.data
            self.custom_id = self.data.custom_id.data
        else:
            self.url = self.data.get('url')
            self.custom_id = self.data.get('custom_id')
        return self

    def get_url(self, short_id=None):
        return URLMap.query.filter_by(
            short=short_id if short_id else self.custom_id
        ).first()

    def get_short_link(self):
        if not self.custom_id:
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
        id = ''.join(choice(chars) for _ in range(ID_SIZE))
        return id
