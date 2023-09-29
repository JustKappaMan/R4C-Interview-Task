from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView
from django.templatetags.static import static

from home.views import index_view


urlpatterns = [
    path("", index_view),
    path("admin/", admin.site.urls),
    path("robots/", include("robots.urls")),
    path("orders/", include("orders.urls")),
    path("favicon.ico", RedirectView.as_view(url=static("images/icons/favicon.ico"))),
]
