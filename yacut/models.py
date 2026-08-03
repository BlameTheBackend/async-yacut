from datetime import datetime, timezone

from sqlalchemy.orm import validates

from . import db
from .contstants import MAX_LENGTH_SHORT_LINK, ALLOWED_CHARS


class URLMap(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(db.String(256), nullable=False)
    short = db.Column(db.String(128), nullable=False, unique=True)
    timestamp = db.Column(
        db.DateTime, index=True, default=datetime.now(timezone.utc)
    )

    @validates('short')
    def validate_short(self, key, value):
        if (
            len(value) > MAX_LENGTH_SHORT_LINK
            or not ALLOWED_CHARS.fullmatch(value)
        ):
            raise ValueError('Указано недопустимое имя для короткой ссылки')
        if (
            URLMap.query.filter_by(short=value).first() is not None
            or value == 'files'
        ):
            raise ValueError(
                'Предложенный вариант короткой ссылки уже существует.')
        return value

    @validates('original')
    def validate_original(self, key, value):
        if not value:
            raise ValueError('\"url\" является обязательным полем!')
        return value
