from django.urls import path

from cart.views import CartView

urlpatterns = [
    path('', CartView.as_view(), name="cartview"),
    path('add/', CartView.as_view(), name="cartadd"),
    path('remove/', CartView.as_view(), name='cartremove'),
]
