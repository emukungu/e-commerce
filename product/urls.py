from django.urls import path
from  .views import ProductAPIView, ShoppingCartAPIView, UserCartAPIView, ProductRetrieveAPIView
# ProductRetrieveAPIView

app_name = 'product'

urlpatterns =(
  path('', ProductAPIView.as_view(), name = 'add_new_product'),
  path('user/cart', UserCartAPIView.as_view(), name = "user_cart"),
  path('<slug>', ProductRetrieveAPIView.as_view(), name = 'single_product'),
  path('<slug>/cart', ShoppingCartAPIView.as_view(), name = 'cart'),
)