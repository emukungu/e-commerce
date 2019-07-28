
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.exceptions import APIException
from utils.auth import decode_token
from paypal.standard.forms import PayPalPaymentsForm
from decimal import Decimal
from django.views.decorators.csrf import csrf_exempt

from orders.models import Orders

class PaymentProcessAPIView(APIView):

  def post(self, request):
    order_slug = request.order.get('order_slug')
    order = get_object_or_404(Orders, product_slug=order_slug)
    # host = request.get_host()

    # What you want the button to do.
    paypal_dict = {
        "business": "esther.namusisi@andela.com",
        "amount": "%.2f" %order.get_total_cost().quantize(Decimal(".01")),
        "item_name": "Order {}".format(order_slug),
        "invoice": str(order.id),
        "currency_code": "USD",
        "notify_url": request.build_absolute_uri(reverse('paypal-ipn')),
        "return": request.build_absolute_uri(reverse('payment:done')),
        "cancel_return": request.build_absolute_uri(reverse('payment:cancel')),
        "custom": "premium_plan",  # Custom command to correlate to some function later (optional)
    }

    # Create the instance.
    form = PayPalPaymentsForm(initial=paypal_dict)
    context = {"form": form}
    return render(request, "payment.html", context)

class PaymentDoneAPIView(APIView):
   @csrf_exempt
   def post(self, request):
     return render(request, "payment/done.html")

class PaymentCancelAPIView(APIView):
  @csrf_exempt
  def post(self, request):
    return render(request, "payment/canceled.html")