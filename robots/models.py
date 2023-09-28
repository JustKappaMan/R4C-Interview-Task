from re import fullmatch
from datetime import datetime

from django.db import models
from django.utils import timezone
from django.db.models import Count


class RobotsManager(models.Manager):
    def models(self) -> tuple[str]:
        """Get unique `Robot.model` values"""
        return tuple(self.values_list("model", flat=True).distinct())

    def last_week_production_summary(self, model: str) -> dict:
        """Extract `Robot.model` production totals for the last week
        e.g. {"R2": ({"version": "D2", "count": "42"}, {"version": "D3", "count": "7"}), ...}
        """
        data = tuple(
            self.filter(model=model, created__gte=timezone.now() - timezone.timedelta(weeks=1))
            .values("version")
            .annotate(count=Count("id"))
        )
        return {model: data} if data else {}

    def is_assembled_at_second(self, timestamp: datetime) -> bool:
        """Return True if there's a robot already assembled at that second, otherwise False"""
        return self.filter(created=timestamp).first() is not None


class Robot(models.Model):
    serial = models.CharField(max_length=5, blank=False, null=False)
    model = models.CharField(max_length=2, blank=False, null=False)
    version = models.CharField(max_length=2, blank=False, null=False)
    created = models.DateTimeField(blank=False, null=False)
    objects = RobotsManager()

    @staticmethod
    def serial_is_valid(serial: str) -> bool:
        """Return `True` if `serial` is something like 'R2-D2', '13-xs' etc., otherwise `False`"""
        return fullmatch("[a-zA-Z0-9]{2}-[a-zA-Z0-9]{2}", serial) is not None
