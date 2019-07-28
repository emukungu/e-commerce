import json
from django.shortcuts import render
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.exceptions import APIException
from django.shortcuts import get_object_or_404
from utils.auth import decode_token

from .serializers import ProductSerializer, ShoppingCartSerializer
from .models import Product, ShoppingCart


# Create your views here.
class ProductAPIView(APIView):
  permission_class = (IsAuthenticated,)

  serializer_class = ProductSerializer

  def post(self, request):
    product = request.data.get('product', {})
    serializer = self.serializer_class(data = product)
    serializer.is_valid(raise_exception = True)
    serializer.save()
    return Response(serializer.data, status=status.HTTP_201_CREATED)

  def get(self, request, *args, **kwargs):
    try:
      queryset = Product.objects.all()
    except: 
      raise APIException('Product does not exist')
    
    serializer = self.serializer_class(queryset, many=True)
    # all_products = serializer.data
    # return Response(all_products, status=status.HTTP_200_OK)
    return render(request, 'product/product_list.html', {'context': serializer.data })


class ProductRetrieveAPIView(APIView):
  permission_class = (AllowAny,)

  serializer_class = ProductSerializer

  def get(self, request, *args, **kwargs):
    try:
      queryset = Product.objects.get(slug = kwargs["slug"])
    except: 
      raise APIException('Product does not exist')
    
    serializer = self.serializer_class(queryset)
    return Response(serializer.data, status=status.HTTP_200_OK)


class ShoppingCartAPIView(APIView):
  permission_class = (IsAuthenticated,)

  serializer_class = ShoppingCartSerializer

  def post(self, request, *args, **kwargs):
    # try:
    slug = kwargs["slug"]
    item = request.data.get('quantity', {})

    cart_item = {
      'product': slug,
      'quantity': item['quantity'],
      'user': request.user.username
      }

    serializer = self.serializer_class(data = cart_item)   
    serializer.is_valid(raise_exception = True)
    serializer.save()
    return Response(serializer.data, status=status.HTTP_201_CREATED)
    # except:
    #   return Response({'error': 'Bad request.'}, status=status.HTTP_400_BAD_REQUEST)


class UserCartAPIView(APIView):
  permission_class = (IsAuthenticated,)

  serializer_class = ShoppingCartSerializer

  def get(self, request):
    # try:
    queryset = ShoppingCart.objects.filter(user = request.user.id)
    # except: 
    #   raise APIException('The shopping cart is empty')
    
    serializer = self.serializer_class(queryset, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)
    # return render(request, 'product/cart.html', {'context': serializer.data })
