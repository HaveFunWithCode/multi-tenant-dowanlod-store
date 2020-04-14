from django.urls import path, re_path
from rest_framework.authtoken.views import obtain_auth_token
from .views import MemberShipSubscribe, MemberShipPlanList

urlpatterns = [
    path('plans/',MemberShipPlanList.as_view(),name="plans"),
    path('subscribe/',MemberShipSubscribe.as_view(),name="subscribe"),

]
