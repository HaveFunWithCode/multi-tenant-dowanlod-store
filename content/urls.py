from django.urls import path
from rest_framework.routers import DefaultRouter
from .viewsets import ProductViewSet, ProductAddViewSet, CategoryListAPIView, FileUploadViewSet

# from .viewsets import ProductAddAPIView, CategoryListAPIView

router = DefaultRouter()
router.register('products', ProductViewSet, basename='products')
router.register('addproduct', ProductAddViewSet, basename='addproduct')
router.register('upload', FileUploadViewSet, basename='upload')


urlpatterns = [
    path('listcategory/',CategoryListAPIView.as_view(), name="categories"),
]
urlpatterns += router.urls
