from django.contrib import admin
from django.urls import path, include

from home.views import index_view


urlpatterns = [
    path("admin/", admin.site.urls),
    path("robots/", include("robots.urls")),
    path("orders/", include("orders.urls")),
    path("", index_view),
]
