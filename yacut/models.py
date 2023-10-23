from datetime import datetime

from . import db
from .constants import MAX_SHORT_LINK_LENGTH


class URLMap(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(db.Text, nullable=False)
    short = db.Column(
        db.String(MAX_SHORT_LINK_LENGTH), unique=True, nullable=False
    )
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
