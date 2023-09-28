from django.urls import path

from robots.views import *


urlpatterns = [
    path('new/', new_robot_view, name="new_robot_view"),
    path('last-week-stats/', last_week_stats_view, name="last_week_stats_view"),
]
