from django.urls import path

from orders.views import new_order_view, successful_order_view, failed_order_view


urlpatterns = [
    path("new/", new_order_view, name="new_order_view"),
    path("success/", successful_order_view, name="successful_order_view"),
    path("fail/", failed_order_view, name="failed_order_view"),
]
