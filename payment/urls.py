from django.urls import path
from  .views import PaymentProcessAPIView, PaymentDoneAPIView, PaymentCancelAPIView

app_name = 'payment'

urlpatterns =(
  path('process', PaymentProcessAPIView.as_view(), name = 'payment_process'),
  path('done', PaymentDoneAPIView.as_view(), name = 'payment_done'),
  path('canceled', PaymentCancelAPIView.as_view(), name = 'payment_canceled')
)