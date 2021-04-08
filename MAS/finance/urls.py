from django.urls import path
from . import views


urlpatterns = [
    path("foreign_exchange/", views.foreign_exchange, name="foreign_exchange"),
    path("stock_prediction/", views.stock_prediction, name="stock_prediction"),
]