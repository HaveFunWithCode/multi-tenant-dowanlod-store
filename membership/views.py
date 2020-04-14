from django.shortcuts import render, redirect
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from .serializers import MemberShipPlansSerializer, MemberShipSubscribeSerializer
from .models import MemberShipPlans

class MemberShipPlanList(ListAPIView):

    serializer_class = MemberShipPlansSerializer
    queryset = MemberShipPlans.objects.all()


class MemberShipSubscribe(APIView):
    serializer_class = MemberShipSubscribeSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = self.serializer_class(data=request.data,
                                           context={'request':request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        subscribe_id = serializer.instance
        return redirect('subscribepayment',subscribe_id=subscribe_id)




