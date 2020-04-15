from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from django.utils.translation import ugettext_lazy as _
from django.db.models import Sum

from cart.models import Cart, CartItem
from content.models import Product, File


class CartItemAddSerializer(ModelSerializer):
    """ Serializer for checking validation of added item to cart"""
    id = serializers.IntegerField(required=True)
    type = serializers.CharField(required=True)

    def validate(self, data):
        obj_id = data["id"]
        item_type = data['type']

        file = File.objects.get(id=obj_id) if item_type == 'f' else None
        product = Product.objects.get(id=obj_id) if item_type == 'p' else None

        if product is None and file is None:
            raise serializers.ValidationError(_('No such file or product found.'))
        return file or product

    class Meta:
        model = CartItem
        fields = ["id", "type"]


class CartItemSerializer(ModelSerializer):
    """ Serializer for serializing cart item detail """
    class Meta:
        model = CartItem
        fields = "__all__"


class CartSerializer(ModelSerializer):
    """ Serializer for calculate total price and serialize the whole cart"""

    total_price = serializers.SerializerMethodField('get_total_price')
    cart_items = serializers.SerializerMethodField('get_cart_items')

    def get_cart_items(self, obj):
        cart_items = CartItem.objects.filter(cart__id=obj.id)
        return CartItemSerializer(cart_items,
                                  many=True,
                                  read_only=True, context=self.context).data

    def get_total_price(self, obj):
        return CartItem.objects.filter(cart__id=obj.id).aggregate(Sum('price'))['price__sum']

    class Meta:
        model = Cart
        fields = ["total_price", 'cart_items']
