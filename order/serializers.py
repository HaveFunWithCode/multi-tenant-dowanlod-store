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