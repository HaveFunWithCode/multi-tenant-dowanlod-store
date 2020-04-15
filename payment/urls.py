from django.urls import path
from payment.views import PaymentSubscribeView, PaymentView

urlpatterns = [
    path('subscribe/<int:subscribe_id>/', PaymentSubscribeView.as_view(), name='subscribepayment'),
    path('<int:orderid>', PaymentView.as_view(), name='payment'),

]
