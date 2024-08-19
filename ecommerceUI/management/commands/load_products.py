# ecommerceUI/management/commands/load_products.py
import csv
from django.core.management.base import BaseCommand
from ecommerceUI.models import Product

class Command(BaseCommand):
    help = 'Load products from CSV'

    def handle(self, *args, **kwargs):
        with open('products.csv', newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                Product.objects.create(
                    
                    category_1=row['category_1'],
                    category_2=row['category_2'],
                    category_3=row['category_3'],
                    title=row['title'],
                    product_rating=float(row['product_rating']),
                    selling_price=float(row['selling_price(KSH.)']),
                    mrp=float(row['mrp(KSH.)']),
                    seller_name=row['seller_name'],
                    seller_rating=float(row['seller_rating']),
                    price_ratio=float(row['price_ratio']),
                    price_difference=float(row['price_difference']),
                )
        self.stdout.write(self.style.SUCCESS('Successfully loaded products from CSV'))
