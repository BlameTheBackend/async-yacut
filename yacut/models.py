from datetime import datetime, timezone

from . import db


class URLMap(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(db.String(256), nullable=False)
    short = db.Column(db.String(128), nullable=False, unique=True)
    timestamp = db.Column(
        db.DateTime, index=True, default=datetime.now(timezone.utc)
    )
