from django.urls import path
from payment.views import PaymentSubscribeView

urlpatterns = [
    path('subscribe/<int:subscribe_id>/', PaymentSubscribeView.as_view(), name='subscribepayment'),

]
