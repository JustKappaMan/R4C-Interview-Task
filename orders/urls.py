from django.urls import path

from orders.views import new_order_view


urlpatterns = [
    path("new/", new_order_view, name="new_order_view"),
]
