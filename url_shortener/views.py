import typing as t

from django.http import JsonResponse
from django.http.response import Http404
from django.views.generic import RedirectView, View

from url_shortener.exceptions import InvalidUrlError
from url_shortener.json_responses import (
    error_400_json,
    error_404_json,
    generate_success_json,
)
from url_shortener.models import Url


class ShortUrlView(View):
    """View that processes requests for getting shortened urls (GET)
    and return appropriate JsonResponse.
    """

    def get(self, *args, **kwargs) -> t.Union[JsonResponse, t.NoReturn]:
        original_url = self.request.GET.get("originalUrl")
        url = Url(original_url=original_url)

        try:
            url.validate()
        except InvalidUrlError:
            return handler400_json(self.request)

        absolute_url = self.request.build_absolute_uri("/")
        shortened_url = absolute_url + url.get_short_url()
        return JsonResponse(generate_success_json(shortened_url, original_url))


short_url_view = ShortUrlView.as_view()


class RedirectToOriginalUrl(RedirectView):
    """View that processes redirects to original url."""

    def get_redirect_url(
        self, short_url: str, *args, **kwargs
    ) -> t.Union[str, t.NoReturn]:
        matching_url = Url.objects.filter(short_url=short_url).first()
        if matching_url:
            return "http://" + matching_url.original_url
        raise Http404()


redirect_to_original_url = RedirectToOriginalUrl.as_view()


def handler400_json(request, *args, **argv) -> JsonResponse:
    """Custom 400 error handler that returns JsonResponse."""

    json_response = JsonResponse(error_400_json)
    json_response.status_code = 400
    return json_response


def handler404_json(request, *args, **argv) -> JsonResponse:
    """Custom 404 error handler that returns JsonResponse."""

    json_response = JsonResponse(error_404_json)
    json_response.status_code = 404
    return json_response
