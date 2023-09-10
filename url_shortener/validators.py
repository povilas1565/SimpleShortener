import re

from django.core.exceptions import ValidationError


def url_validator(value):
    """Url validator that skips url schema validation (http://, https:// and etc.)."""

    regex = re.compile(
        r"(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|"  # domain
        r"localhost|"  # localhost
        r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})"  # ip
        r"(?::\d+)?"  # optional port
        r"(?:/?|[/?]\S+)$", re.IGNORECASE)

    url_matches = re.match(regex, value)
    if not url_matches:
        raise ValidationError(f"Url {value} is invalid.")
    return value
