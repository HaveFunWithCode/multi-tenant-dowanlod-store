from rest_framework import viewsets, permissions, status
from rest_framework.decorators import permission_classes
from rest_framework.response import Response

from .models import Product
from .serializers import ProductSerializer
from stores.utils import store_from_request


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get_queryset(self):
        store = store_from_request(self.request)
        return super().get_queryset().filter(store=store)


