import random
import string

from .models import URLMap
from .contstants import LENGTH_SHORT_ID, MAX_ATTEMPTS


def get_unique_short_id(length: int = LENGTH_SHORT_ID) -> str:
    all_chars = string.ascii_letters + string.digits
    attempt = 0
    while True:
        attempt += 1
        short_id = ''.join(random.choices(all_chars, k=length))
        if not URLMap.query.filter_by(short=short_id).first():
            break
        if attempt == MAX_ATTEMPTS:
            raise RuntimeError(
                'Достигнуто максимальное число попыток' +
                ' генерации короткой ссылки')
    return short_id
