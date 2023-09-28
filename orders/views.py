from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from django.http import HttpRequest, HttpResponse, HttpResponseNotAllowed

from orders.models import Order
from customers.models import Customer
from orders.utils import validate_new_order_request


@require_http_methods(("GET", "POST"))
def new_order_view(request: HttpRequest) -> HttpResponse | HttpResponseNotAllowed:
    if request.method == "GET":
        return render(request, template_name="orders/order.html")

    if request.method == "POST":
        try:
            data = validate_new_order_request(request)
        except ValueError as e:
            raise e
        else:
            new_customer = Customer.objects.create(email=data["email"])
            new_order = Order.objects.create(customer=new_customer, robot_serial=data["serial"])
