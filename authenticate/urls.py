from django.urls import path
from .views import RegistrationAPIView, LoginAPIView

app_name = 'authenticate'

urlpatterns = [
    path('register', RegistrationAPIView.as_view(), name= 'register_user'),
    path('login', LoginAPIView.as_view(), name= 'login_user'),
    # path('edit/<id>', RetrieveUpdateUserAPIView.as_view(), name= 'update_retrieve_user'),
]