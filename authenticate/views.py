# Create your views here.
from django.shortcuts import render
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.exceptions import APIException

from .serializers import UserRegisterSerializer, LoginSerializer
from .models import User

class RegistrationAPIView(APIView):
  """ Create and return a new user"""
  permissions_class = (AllowAny,)
  serializer_class = UserRegisterSerializer

  def post(self, request):
    try:
      user = request.data.get('user', {})

      serializer = self.serializer_class(data = user)
      serializer.is_valid(raise_exception = True)
      serializer.save()

      return Response(serializer.data, status=status.HTTP_201_CREATED)
      # return render(request, 'authenticate/signup.html', {'context': serializer.data})
    except:
      return Response({"message": "User already exists"}, status=status.HTTP_400_BAD_REQUEST)

    

class LoginAPIView(APIView):
  """ Login a user and return token"""
  serializer_class = LoginSerializer

  def post(self, request):

    user = request.data.get('user', {})

    serializer = self.serializer_class(data = user)
    serializer.is_valid(raise_exception = True)

    return Response(serializer.data, status=status.HTTP_200_OK)
    


