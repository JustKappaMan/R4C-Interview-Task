from django.http import HttpRequest
from django.dispatch import receiver
from django.core.mail import send_mail
from django.db.models.signals import post_save

from robots.models import Robot
from orders.models import Order
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

    return {"serial": serial, "email": email}


@receiver(post_save, sender=Robot)
def notify_customer_robot_available(sender, instance, **kwargs):
    try:
        order = Order.objects.get(robot_serial=instance.serial)
    except Order.DoesNotExist:
        pass
    else:
        email_subject = "Робот доступен к покупке!"
        email_message = (
            "Здравствуйте!\n\n"
            f"Недавно Вы интересовались нашим роботом модели {instance.model}, версии {instance.version}.\n\n"
            "Этот робот теперь в наличии. Если Вам подходит этот вариант - пожалуйста, свяжитесь с нами."
        )
        send_mail(email_subject, email_message, "from@example.com", (order.customer.email,))
        print("Email has been sent!")
