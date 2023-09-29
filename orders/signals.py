from django.dispatch import receiver
from django.core.mail import send_mail
from django.db.models.signals import post_save

from orders.models import Order
from robots.models import Robot


@receiver(post_save, sender=Robot)
def notify_customers_robot_available(sender, instance, **kwargs) -> None:
    try:
        orders = Order.objects.filter(robot_serial=instance.serial)
    except Order.DoesNotExist:
        pass
    else:
        email_subject = "Робот доступен к покупке!"
        email_message = (
            "Здравствуйте!\n\n"
            f"Недавно Вы интересовались нашим роботом модели {instance.model}, версии {instance.version}.\n\n"
            "Этот робот теперь в наличии. Если Вам подходит этот вариант — пожалуйста, свяжитесь с нами."
        )
        for order in orders:
            send_mail(email_subject, email_message, "info@robocomplex.com", (order.customer.email,))
            order.delete()
