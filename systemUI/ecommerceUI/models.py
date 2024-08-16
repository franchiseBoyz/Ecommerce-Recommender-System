from django.db import models

class Product(models.Model):
    category_1 = models.CharField(max_length=255)
    category_2 = models.CharField(max_length=255)
    category_3 = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    product_rating = models.FloatField()
    selling_price = models.FloatField()
    mrp = models.FloatField()
    seller_name = models.CharField(max_length=255)
    seller_rating = models.FloatField()
    price_ratio = models.FloatField()
    price_difference = models.FloatField()

    def __str__(self):
        return self.title

