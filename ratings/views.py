from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.exceptions import APIException
from utils.auth import decode_token

from .serializers import RatingSerializer
from .models import ProductRatings

# Create your views here.
class RatingAPIView(APIView):
  permission_class = (IsAuthenticated,)

  serializer_class = RatingSerializer

  def post(self, request, *args, **kwargs):
    slug = kwargs["slug"]
    rating = request.data.get('rate', {})
    
    rating_details = {
        'slug': slug,
        'product_rating': rating['rate'],
        'rated_by': request.user.username
        }
    
    serializer = self.serializer_class(data = rating_details)
    serializer.is_valid(raise_exception = True)
    serializer.save()
    return Response(serializer.data, status=status.HTTP_201_CREATED)

class RatingRetrieveAPIView(APIView):
  permission_class = (AllowAny,)

  serializer_class = RatingSerializer

  def get(self, request, *args, **kwargs):
    try:
      queryset = ProductRatings.objects.get(slug = kwargs["slug"])
    except: 
      raise APIException('Product does not exist')
    
    serializer = self.serializer_class(queryset)
    return Response(serializer.data, status=status.HTTP_200_OK)
