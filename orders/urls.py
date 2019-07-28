from django.urls import path
from  .views import OrderAPIView, UserOrdersAPIView

app_name = 'orders'

urlpatterns =(
  path('user', UserOrdersAPIView.as_view(), name = 'retrieve_user_orders'),
  path('<slug>', OrderAPIView.as_view(), name = 'add_new_order'),
)