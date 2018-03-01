import csv
from django.core.management import BaseCommand
import requests
import json
from saleor.product.models import Category, Collection, Product,ProductVariant,ProductImage
from django.conf import settings
from decimal import Decimal

# USAGE:
# python manage.py csv_product_import path/to/file.csv
# file.csv should contain one column named 'sku', all other columns ignored
# Tested with CSV exported from magento 2.x
# - magentos simple product type only
# - currently only imports sku, name, description, price, and base image, all products get saved in the saleor default category

class Command(BaseCommand):
    help = 'Import products'
    def add_arguments(self, parser):
        parser.add_argument('file', type=str)

    def handle(self, *args, **options):
        input_file = csv.DictReader(open(options['file']))
        for magento_product in input_file:
            check_exists = ProductVariant.objects.filter(sku=magento_product['sku'])
            if magento_product['product_type'] == 'simple' and not magento_product['custom_options']:
                if not check_exists:
                    print ("creating : %s" % (magento_product['sku']))
                    imported_product = Product.objects.create(
                    name=magento_product['name'],
                    description=magento_product['description'],
                    #TODO: fails if value is an integer
                    price = float(magento_product['price']),
                    product_type_id=1,
                    category_id=1)       

                    ProductVariant.objects.create(
                    sku = magento_product['sku'],
                    product = imported_product)
                    if magento_product['base_image']:
                        ProductImage.objects.create(
                        product = imported_product,
                        image=magento_product['base_image']
                        )
                else:
                    print ("updating : %s" % (magento_product['sku'])) 
                    saleor_product = ProductVariant.objects.get(sku=magento_product['sku']) 
                    saleor_product.categories='default'
                    saleor_product.price=magento_product['price']
                    saleor_product.name=magento_product['name']
                    saleor_product.description=magento_product['description']
                    saleor_product.save
            else:
                print ('Ignoring non simple product type or product with options')       
