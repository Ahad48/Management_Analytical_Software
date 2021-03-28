from django.urls import path
from . import views


urlpatterns = [
    path("sentiment/", views.get_company, name="sentiment"),
]