from rest_framework import serializers
from product.models import Product 
from authenticate.models import User
from .models import Orders

class OrdersSerializer(serializers.Serializer):
  ordered_by = serializers.CharField(max_length = 255)
  product_slug = serializers.CharField(max_length = 255)
  check_out = serializers.BooleanField()


  def validate(self, data):
    check_out = data.get('check_out')
    product_slug = data.get('product_slug')
    ordered_by = data.get('ordered_by')

    existing_product = Product.objects.get(slug = product_slug)
    existing_user = User.objects.get(username = ordered_by)
    
    if not existing_product:
      raise serializers.ValidationError('Product does not exist')
    if not check_out:
      raise serializers.ValidationError('The checkout confirmation is required')
    if not ordered_by:
      raise serializers.ValidationError('The user is required')
    existing_order = Orders.objects.get(product_slug_id = existing_product.id, ordered_by_id = existing_user.id )
    if existing_order:
      raise serializers.ValidationError('You already ordered this product')

    return {
      "check_out": check_out,
      "product_slug": existing_product.id,
      "ordered_by": existing_user.id
    }
  
  def create(self, validated_data):
    instance = Orders.objects.create(check_out = validated_data['check_out'],
                                     ordered_by_id = validated_data['ordered_by'],
                                     product_slug_id = validated_data['product_slug'])
    return instance
    