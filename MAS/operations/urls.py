from django.urls import path
from . import views


urlpatterns = [
    path("show_gantt_chart/", views.show_gantt_chart, name='show_gantt_chart'),
]
