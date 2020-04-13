from rest_framework.routers import DefaultRouter
from .viewsets import ProductViewSet


router = DefaultRouter()
router.register('products', ProductViewSet, basename='products')