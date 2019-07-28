from django.db import models

# Create your models here.
class Orders(models.Model):
  product_slug = models.ForeignKey('product.Product', related_name = 'order_products', on_delete = models.CASCADE)
  ordered_by = models.ForeignKey('authenticate.User', related_name = 'order_user', on_delete = models.CASCADE)
  check_out = models.CharField(max_length = 255, default=False)
  paid = models.CharField(max_length = 255, default=False)
  completed_order = models.CharField(max_length = 255, default=False)
