from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.
class UserRatings(models.Model):
  slug = models.SlugField()
  rated_by = models.ForeignKey('authenticate.User', on_delete=models.CASCADE)
  seller_rating = models.IntegerField()

  def __str__(self):
    return self.seller_rating

class ProductRatings(models.Model):
  slug = models.SlugField()
  rated_by = models.ForeignKey('authenticate.User', on_delete=models.CASCADE)
  product_rating = models.IntegerField(validators=[ MaxValueValidator(5), MinValueValidator(1)])
