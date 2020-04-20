from django.utils.decorators import method_decorator
from rest_framework import viewsets, status
from rest_framework.parsers import (MultiPartParser,
                                    FormParser)
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from .models import (Product,
                     Category,
                     File)
from .permissions import IsOwnerOfStore
from .serializers import (ProductSerializer,
                          CategorySerializer,
                          ProductAddSerializer,
                          FileUploadSerializer)
from stores.utils import store_from_request


from django.conf import settings
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from .decorators import cache_per_store

CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    http_method_names = ['get', ]

    def get_queryset(self):
        store = store_from_request(self.request)
        return super().get_queryset().filter(store=store)

    @method_decorator(cache_per_store(timeout=CACHE_TTL))
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


class ProductAddViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductAddSerializer
    permission_classes = [IsOwnerOfStore, ]

    def get_queryset(self):
        store = store_from_request(self.request)
        return super().get_queryset().filter(store=store)

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"product_id": serializer.instance.id}, status=status.HTTP_201_CREATED)


class CategoryViewSet(ModelViewSet):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
    permission_classes = [IsOwnerOfStore, ]


class FileUploadViewSet(ModelViewSet):
    queryset = File.objects.all()
    serializer_class = FileUploadSerializer
    parser_classes = (MultiPartParser, FormParser,)
    permission_classes = [IsOwnerOfStore, ]

    def get_queryset(self):
        product_id = self.request.query_params['product_id']
        return self.queryset.filter(product_id=int(product_id))

    def perform_create(self, serializer):
        product_id = self.request.query_params['product_id']
        serializer.save(product=Product.objects.get(id=int(product_id)),
                        file_path=self.request.data.get('file_path'))

    def post(self, request, *args, **kwargs):

        file_serializer = FileUploadSerializer(data=request.data)

        if file_serializer.is_valid():
            file_serializer.save()
            return Response(file_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
