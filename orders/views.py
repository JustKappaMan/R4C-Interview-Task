from django.shortcuts import render
from django.http import HttpRequest, HttpResponse, HttpResponseNotAllowed, JsonResponse

from orders.models import Order
from customers.models import Customer
from orders.utils import validate_new_order_request


def new_order_view(request: HttpRequest) -> HttpResponse | JsonResponse:
    if request.method == "GET":
        return render(request, template_name="orders/order.html")
    elif request.method == "POST":
        try:
            data = validate_new_order_request(request)
        except ValueError as e:
            return JsonResponse({"status": "error", "message": f"{e}"})
        else:
            new_customer = Customer.objects.create(email=data["email"])
            new_order = Order.objects.create(customer=new_customer, robot_serial=data["serial"])
    else:
        return HttpResponseNotAllowed(permitted_methods=("GET", "POST"))
