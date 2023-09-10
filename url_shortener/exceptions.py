from core.exceptions import BaseProjectException


class InvalidUrlError(BaseProjectException):
    """Exception raised when invalid url is passed."""

    pass


class MissingPrimaryKeyError(BaseProjectException):
    """Exception raised when primary key is missing."""

    pass
