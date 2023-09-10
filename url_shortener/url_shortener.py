import secrets

import hashids


def _create_salt() -> str:
    """Create random salt."""

    salt = secrets.token_hex(8)
    return salt


def generate_id(number: int, salt: str = "") -> str:
    """Generate unique and non-sequential ids (hex) from number with
    minimum length of 3 characters. Use base62 alphabet which
    is shuffled based on :salt:.
    """

    if not salt:
        salt = _create_salt()
    hashids_ = hashids.Hashids(salt=salt, min_length=3)
    return hashids_.encode(number)
