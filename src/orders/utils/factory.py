from django.http import HttpRequest

from orders.models import Order
from robots.models import Robot
from customers.models import Customer


def _validate_new_order_request(request: HttpRequest) -> dict[str, str] | None:
    """Return valid data for creating a new order from POST request as `dict`.
    If something is wrong, raise `ValueError` with corresponding message.
    """

    # Verify that `serial` and `email` params exist and valid
    #
    # 'noinspection' is used to supress 'Parameter `self` is unfilled' warning
    # `request.POST` is a 'QueryDict' that uses parent (`MultiValueDict`) `.get()` method
    #
    # Warning pops up, even though everything works as expected. Maybe some Django/PyCharm bug.

    # noinspection PyArgumentList
    if (serial := request.POST.get(key="serial")) is None:
        raise ValueError("serial is missing")

    # noinspection PyArgumentList
    if (email := request.POST.get(key="email")) is None:
        raise ValueError("email is missing")

    if not Robot.serial_is_valid(serial):
        raise ValueError("serial is invalid")

    if not Customer.email_is_valid(email):
        raise ValueError("email is invalid")

    # Normalization. Make `serial` uppercase before return.
    return {"serial": serial.upper(), "email": email}


def create_new_order(request: HttpRequest) -> None:
    """Create new Order using data validated with `_validate_new_order_request`"""
    data = _validate_new_order_request(request)
    new_customer = Customer.objects.create(email=data["email"])
    Order.objects.create(customer=new_customer, robot_serial=data["serial"])
