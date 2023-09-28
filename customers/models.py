import re

from django.db import models


class Customer(models.Model):
    email = models.CharField(max_length=255,blank=False, null=False)

    @staticmethod
    def email_is_valid(email: str) -> bool:
        """Return `True` if `email` matches `*@*.*` pattern, otherwise `False`"""
        return re.fullmatch(r"[^@]+@[^@]+\.[^@]+", email) is not None
