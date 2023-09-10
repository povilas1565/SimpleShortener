from django.urls import path

from url_shortener.views import redirect_to_original_url, short_url_view

urlpatterns = [
    path("shorturl/", view=short_url_view, name="short_url"),
    path(
        "<str:short_url>/",
        view=redirect_to_original_url,
        name="redirect_to_original_url",
    ),
]
