from django.urls import path
from  .views import RatingAPIView, RatingRetrieveAPIView

app_name = 'ratings'

urlpatterns =(
  path('<slug>', RatingAPIView.as_view(), name = 'add_product_rate'),
  path('<slug>/rates', RatingRetrieveAPIView.as_view(), name = 'retrieve_product_rates')
)