from rest_framework import serializers
from .models import Product, ShoppingCart
from authenticate.models import User

class ProductSerializer(serializers.Serializer):
  name = serializers.CharField(max_length = 255)
  description = serializers.CharField(max_length = 255)
  photo = serializers.CharField(max_length=255) #ImageField
  price_in_dollars = serializers.DecimalField(max_digits=6, decimal_places=2)
  seller = serializers.CharField(max_length=255)

  class Meta:
    model = Product
    fields = '__all__'

  def validate(self, data):
    name = data.get('name')
    description = data.get('description')
    seller = data.get('seller')
    price_in_dollars = data.get('price_in_dollars')

    if not name:
      raise serializers.ValidationError('The name is required')
    if not description:
      raise serializers.ValidationError('The description is required')
    if not seller:
      raise serializers.ValidationError('The seller is required')
    if not price_in_dollars:
      raise serializers.ValidationError('The price_in_dollars is required')
    
    product = {
      'name': name,
      'description': description,
      'price_in_dollars': price_in_dollars,
      'seller': seller
    }
    return product

  def create(self, product):
    return Product.objects.create(name= product['name'], 
                                  description = product['description'], 
                                  price_in_dollars= product['price_in_dollars'], 
                                  seller= product['seller'])


class ShoppingCartSerializer(serializers.Serializer):
  product = serializers.CharField(max_length = 255)
  user = serializers.CharField(max_length = 255)
  quantity = serializers.IntegerField()

  class Meta:
    model = ShoppingCart
    fields = '__all__'

  def validate(self, data):
    quantity = data.get('quantity')
    product = data.get('product')
    user = data.get('user')

    existing_product = Product.objects.get(slug = product)
    existing_user = User.objects.get(username = user)
    if not existing_product:
      raise serializers.ValidationError('Product does not exist')
    if not quantity:
      raise serializers.ValidationError('The quantity is required')

    return {
      'quantity': quantity,
      'user': existing_user.id,
      'product': existing_product.id
    } 
  
  def create(self, validated_data):
    instance = ShoppingCart.objects.create(quantity = validated_data['quantity'],
                                           user_id = validated_data['user'],
                                           product_id = validated_data['product'])
    return instance
            
     