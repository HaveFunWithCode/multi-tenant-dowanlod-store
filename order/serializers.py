from rest_framework import serializers

from cart.models import Cart
from order.models import OrderItem, Order


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ('order',
                  'product',
                  'file',
                  'price',
                  'item_type')


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ( 'id')

    def create(self, validated_data):
        request = self.context.get('request')
        user = request.user
        cart = Cart.objects.get(customer=user.customeruser)

        order = Order.objects.create(customer=user.customeruser,
                                     order_status=Order.PENDING,
                                     total_price=cart.total_price)

        for item in cart.cartitem_set.all():
            OrderItem.objects.create(
                order=order,
                product=item.product,
                file=item.file,
                price=item.price)

        # empty cart
        Cart.objects.get(customer=user.customeruser).cartitem_set.all().delete()
        cart.total_price = 0
        cart.save(update_fields=['total_price'])

        return order
