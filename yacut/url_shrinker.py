import random
import string

from .models import URLMap
from .contstants import LENGTH_SHORT_ID


def get_unique_short_id(length: int = LENGTH_SHORT_ID) -> str:
    all_chars = string.ascii_letters + string.digits
    while True:
        short_id = ''.join(random.choices(all_chars, k=length))
        if not URLMap.query.filter_by(short=short_id).first():
            break
    return short_id
