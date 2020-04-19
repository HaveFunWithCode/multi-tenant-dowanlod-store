from django.shortcuts import render
from django.urls import path

from .views import StoreListAPIVIew

urlpatterns = [
    path('',StoreListAPIVIew.as_view(),name='storelist'),
]
