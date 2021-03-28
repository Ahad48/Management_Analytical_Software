from django.urls import path
from . import views


urlpatterns = [
    path("show_gantt_chart/", views.show_gantt_chart, name='show_gantt_chart'),
    path("add_project/", views.AddProjectDetailsView.as_view(), name="add_project"),
    path("add_job/", views.AddJobDetailsView.as_view(), name="add_job"),
]
