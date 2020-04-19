from django.shortcuts import render
from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from .serializer import StoreSerializer
from .models import Store


class StoreListAPIVIew(ListAPIView):
    serializer_class = StoreSerializer

    def get_queryset(self):
        return Store.objects.filter(is_active = True)




