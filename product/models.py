from datetime import datetime
from django.utils.text import slugify 
from django.db import models

# Create your models here.
class Product(models.Model):
  name = models.CharField(max_length = 255)
  description = models.TextField()
  slug = models.SlugField (unique=True)
  photo = models.CharField(max_length = 255, blank=True) #ImageField
  price_in_dollars = models.DecimalField(max_digits=6, decimal_places=2)
  seller = models.CharField(max_length=255, blank=True)


  def save(self, *args, **kwargs):
    self.slug= slugify(self.name)
    super(Product, self).save(*args, **kwargs) 

  def __str__(self):
    return self.name


class ShoppingCart(models.Model):
  quantity = models.IntegerField()
  user = models.ForeignKey('authenticate.User', related_name = 'user_cart', on_delete = models.CASCADE)
  product = models.ForeignKey(Product, related_name = 'user_cart_products', on_delete = models.CASCADE)


