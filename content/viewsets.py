from rest_framework import viewsets, permissions, status
from rest_framework.decorators import permission_classes
from rest_framework.parsers import MultiPartParser, FormParser, FileUploadParser
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import ListAPIView, CreateAPIView

from .models import Product, Category, File
from .permissions import IsOwnerOfStore
from .serializers import ProductSerializer, CategorySerializer, ProductAddSerializer, FileSerializer, \
    FileUploadSerializer
from stores.utils import store_from_request


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    http_method_names = ['get', ]

    def get_queryset(self):
        store = store_from_request(self.request)
        return super().get_queryset().filter(store=store)


class ProductAddViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductAddSerializer
    permission_classes = [IsOwnerOfStore, ]

    def get_queryset(self):
        store = store_from_request(self.request)
        return super().get_queryset().filter(store=store)
    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request':request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"product_id":serializer.instance.id},status=status.HTTP_201_CREATED)


class FileUploadView(APIView):

    parser_classes = (MultiPartParser, FormParser,)
    permission_classes = [IsOwnerOfStore, ]


    def post(self, request, *args, **kwargs):

      file_serializer = FileUploadSerializer(data=request.data)

      if file_serializer.is_valid():
          file_serializer.save()
          return Response(file_serializer.data, status=status.HTTP_201_CREATED)
      else:
          return Response(file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CategoryListAPIView(ListAPIView):

    serializer_class = CategorySerializer
    queryset = Category.objects.all()
