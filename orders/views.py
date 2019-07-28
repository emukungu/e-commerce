from django.shortcuts import render, redirect
from django.urls import reverse
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.exceptions import APIException
from utils.auth import decode_token

from .serializers import OrdersSerializer
from .models import Orders

# Create your views here.
class OrderAPIView(APIView):
  permission_class = (IsAuthenticated,)

  serializer_class = OrdersSerializer

  def post(self, request, *args, **kwargs):
    slug = kwargs["slug"]
    check_out = request.data.get('check_out', {})
    check_out_details = {
        'product_slug': slug,
        'check_out': check_out['check_out'],
        'ordered_by': request.user.username
        }

    serializer = self.serializer_class(data = check_out_details)
    serializer.is_valid(raise_exception = True)
    serializer.save()
    
    request.session['order_slug'] = slug
    return redirect(reverse('payment:payment_process'))
    # return Response(serializer.data, status=status.HTTP_201_CREATED)


class UserOrdersAPIView(APIView):
  permission_class = (IsAuthenticated,)

  serializer_class = OrdersSerializer

  def get(self, request):
    try:
      queryset = Orders.objects.filter(ordered_by = request.user.id)
    except: 
      raise APIException('No existing orders')
    
    serializer = self.serializer_class(queryset, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)
    # return render(request, 'product/cart.html', {'context': serializer.data })
