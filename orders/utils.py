from django.http import HttpRequest

from robots.models import Robot
from customers.models import Customer


def validate_new_order_request(request: HttpRequest) -> dict[str, str] | None:
    """..."""

    # Verify that `serial` and `email` params exist
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

    return {"serial": serial.upper(), "email": email}
