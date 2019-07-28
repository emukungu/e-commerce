from rest_framework import serializers
from product.models import Product  
from .models import ProductRatings
from authenticate.models import User

class RatingSerializer(serializers.Serializer):
  rated_by = serializers.CharField(max_length = 255)
  product_rating = serializers.IntegerField()
  slug = serializers.CharField(max_length = 255)

  class Meta:
    model = ProductRatings
    fields = '__all__'

  def validate(self, data):
    product_rating = data.get('product_rating')
    slug = data.get('slug')
    rated_by = data.get('rated_by')

    existing_product = Product.objects.get(slug = slug)
    existing_user = User.objects.get(username = rated_by)

    if not existing_product:
      raise serializers.ValidationError('Product does not exist')
    if not product_rating:
      raise serializers.ValidationError('The rate is required')
      
    existing_rate = ProductRatings.objects.filter(slug = slug, rated_by_id = existing_user.id )
    if existing_rate:
      raise serializers.ValidationError('You already rated this product')

    return {
      "slug": slug,
      "product_rating": product_rating,
      "rated_by": existing_user.id,
    }

  def create(self, validated_data):
    instance = ProductRatings.objects.create(product_rating = validated_data['product_rating'],
                                            slug = validated_data['slug'],
                                            rated_by_id = validated_data['rated_by'])
    return instance
            
    