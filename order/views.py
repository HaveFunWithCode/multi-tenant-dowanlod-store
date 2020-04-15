from django.shortcuts import redirect
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from cart.models import Cart
from order.models import Order, OrderItem


class OrderRegisterView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        cart = Cart.objects.get(customer=user.customeruser)

        order = Order.objects.create(customer=user.customeruser,
                                     order_status=Order.PENDING,
                                     total_price=cart.total_price)

        for item in cart.cartitems.all():
            OrderItem.objects.create(
                order=order,
                product=item.product,
                file=item.file,
                price=item.price).save()
            order.total_price+=item.price
            order.save(update_fields=['total_price'])

        # empty cart
        Cart.objects.get(customer=user.customeruser).cartitems.all().delete()
        cart.total_price = 0
        cart.save(update_fields=['total_price'])
        return redirect('payment', orderid=order.id)