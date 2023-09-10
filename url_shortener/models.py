import typing as t

from django.conf.global_settings import SECRET_KEY
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models.query import QuerySet

from url_shortener.exceptions import InvalidUrlError, MissingPrimaryKeyError
from url_shortener.url_shortener import generate_id
from url_shortener.validators import url_validator


class Url(models.Model):
    """Model that represents original URL and its shortened url equivalent.

    :original_url: is actual full URL without schema (http://, https:// and etc.). Example: 'google.com'
    :short_url: is shortened relative URL. Example: 'aAb'
    """

    original_url = models.URLField(
        verbose_name="original full url", null=False, unique=True, db_index=True
    )
    short_url = models.URLField(
        verbose_name="shortened relative url", null=True, unique=True
    )

    def __str__(self) -> str:
        cls_name = self.__class__.__name__
        return f"<{cls_name}(original={self.original_url}, short={self.short_url})>"

    def clean(self) -> None:
        """Run custom validators."""

        url_validator(value=self.original_url)

    def validate(self) -> t.Optional[t.NoReturn]:
        """Run custom clean() and handles ValidationError."""

        try:
            self.clean()
        except ValidationError as e:
            raise InvalidUrlError(e)

    @staticmethod
    def _remove_url_schema(url: str) -> str:
        """Remove url schema (http://, https:// and etc.) from given URL."""

        url_schemas = ("https://", "http://")
        for schema in url_schemas:
            url_without_schema = url.removeprefix(schema)
        return url_without_schema

    def _get_existing(self) -> t.Optional["QuerySet[Url]"]:
        """Prepare and check whether self (Url instance) exists at
        the database and returns it in case of success. Otherwise,
        save it to the database and return None.
        """

        url_without_schema = self._remove_url_schema(self.original_url)
        existing_url = Url.objects.filter(original_url=url_without_schema).first()
        if existing_url:
            return existing_url
        self.save()
        return None

    def _create_short_url(self) -> t.Union[str, t.NoReturn]:
        """Create short URL from original one and save it to the database.
        self.pk should exist as it is used for generating string id.
        """

        if self.pk:
            self.short_url = generate_id(number=self.pk, salt=SECRET_KEY)
            self.save()
            return self.short_url
        raise MissingPrimaryKeyError(
            f"Primary key (pk) for {self} is missing because object was not saved."
        )

    def get_short_url(self) -> str:
        """Get and return short URL."""

        existing_url = self._get_existing()
        if existing_url:
            return existing_url.short_url
        return self._create_short_url()
