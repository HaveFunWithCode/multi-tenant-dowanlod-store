from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from django.db import IntegrityError
from django.utils.translation import ugettext_lazy as _

from .models import Cart, CartItem
from content.models import File, Product
from .serializer import (CartSerializer,
                         CartItemAddSerializer)


class CartView(APIView):
    """ APIView to handle CRUD functionality for Cart Model"""
    permission_classes = [IsAuthenticated]
    serializer_class = CartSerializer

    # show cart content
    def get(self, request):
        cart = Cart.objects.get(customer=request.user.customeruser)
        return Response({'cart': self.serializer_class(cart).data}, status=status.HTTP_200_OK)

    # add to cart file or product based on "type" parameter and their id
    def post(self, request):
        serializer = CartItemAddSerializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        cart = Cart.objects.get(customer=request.user.customeruser)
        cart_item_object = serializer.validated_data
        if type(cart_item_object) is Product:
            try:
                CartItem.objects.create(cart=cart, product=cart_item_object, price=cart_item_object.price)
            except IntegrityError:
                return Response({"cart": self.serializer_class(cart).data,
                                 "message": _("selected file or product already existed in cart")},
                                status=status.HTTP_400_BAD_REQUEST)
        else:
            CartItem.objects.create(cart=cart, file=cart_item_object, price=cart_item_object.price)

        return Response({'cart': self.serializer_class(cart).data}, status=status.HTTP_201_CREATED)

    # remove from cart (parameter id is equal to cartItem id)
    def delete(self, request):
        cart = Cart.objects.get(customer=request.user.customeruser)
        cart_item_id = request.data['id']
        try:
            CartItem.objects.get(id=cart_item_id).delete()
        except CartItem.DoesNotExist:
            return Response({"cart": self.serializer_class(cart).data,
                             "message": _("No such item exist")},
                            status=status.HTTP_400_BAD_REQUEST)
        return Response({"cart": self.serializer_class(cart).data,
                         "message": _("Successfully removed from cart")},
                        status=status.HTTP_200_OK)
