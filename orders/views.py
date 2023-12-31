from django.urls import reverse
from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse
from django.views.decorators.http import require_http_methods, require_GET

from orders.utils.factory import create_new_order


@require_http_methods(("GET", "POST"))
def new_order_view(request: HttpRequest) -> HttpResponse:
    """View for submitting a new order via HTML form"""
    if request.method == "GET":
        return render(request, template_name="orders/order.html")

    if request.method == "POST":
        try:
            create_new_order(request)
        except ValueError:
            return redirect(reverse("failed_order_view"))
        else:
            return redirect(reverse("successful_order_view"))


@require_GET
def successful_order_view(request: HttpRequest) -> HttpResponse:
    """Displayed when order is successfully submitted"""
    return render(request, template_name="orders/success.html")


@require_GET
def failed_order_view(request: HttpRequest) -> HttpResponse:
    """Displayed when order is failed. e.g. some form fields are empty"""
    return render(request, template_name="orders/fail.html")
