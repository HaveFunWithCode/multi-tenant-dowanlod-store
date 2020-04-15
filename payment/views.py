from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from membership.models import MemberShipOrder
from order.models import Order


class PaymentSubscribeView(APIView):

    def get(self, request, subscribe_id):
        """
        Payment app skeleton
        payment_result=0 ==> assume payment result is not ok

        payment_result=1 ==>assume payment result is ok
        """

        payment_result = 1
        order = MemberShipOrder.objects.get(id=subscribe_id)

        if payment_result:
            order.order_status = MemberShipOrder.SUCCESSFUL
            order.is_active = True
            order.save(update_fields=['order_status', 'is_active'])
            return Response({'message': 'successful payed'}, status=status.HTTP_200_OK)
        else:
            order.shipping_status = MemberShipOrder.UNSUCCESSFUL
            order.save(update_fields=['order_status'])
            return Response({'message': 'unsuccessful payment'}, status=status.HTTP_400_BAD_REQUEST)


class PaymentView(APIView):

    def get(self, request, orderid):

        """
       Payment app skeleton
       payment_result=0 ==> assume payment result is not ok
       payment_result=1 ==>assume payment result is ok
       """
        payment_result = 1
        order = Order.objects.get(id=orderid)
        if payment_result:
            order.order_status = Order.SUCCESSFUL
            order.save(update_fields=['order_status'])
            return Response({'status': 'successful payed'})
        else:
            order.order_status = Order.UNSUCCESSFUL
            order.save(update_fields=['order_status'])
            return Response({'status': 'successful payed'})
