from django.shortcuts import render
from django.urls import path

from order.views import OrderRegisterView

urlpatterns = [
    path('',OrderRegisterView.as_view(),name='registerorder'),
]
