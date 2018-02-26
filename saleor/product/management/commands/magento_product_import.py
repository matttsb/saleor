# Magento 2 > Saleor Product Import
# add MAGENTO_REST_URL and MAGENTO_ACCESS_TOKEN to settings.py
# 
# python manage.py import_magento_products
#

from django.core.management import BaseCommand
import requests
import json
from saleor.product.models import Category, Collection, Product,ProductVariant
from django.conf import settings

class Command(BaseCommand):
    help = 'Import products'

    def handle(self, *args, **options):
        
        rest_url = settings.MAGENTO_REST_URL
        access_token = settings.MAGENTO_ACCESS_TOKEN
       
        # print ("Stating Attribute Import")
        # endpoint = "%sV1/products/attributes?searchCriteria=0" % (rest_url)
        # headers = {"Authorization":"Bearer " + access_token}
        # items = requests.get(endpoint, headers=headers).json()
        # for item in items['items']:
        #     try:
        #         print(item['default_frontend_label'])
        #         # Code to create attributes goes here!
        #     except:
        #         print ('**WARNING** Attribute has no default front end label')
        print ("Stating Category Import")
        endpoint = "%sV1/categories/" % (rest_url)
        print (endpoint)
        headers = {"Authorization":"Bearer " + access_token}
        response = requests.get(endpoint, headers=headers).json()
        for key in response['children_data']:
            category_name=key['name']
            magento_category_id=key['id']
            category=Category.objects.get_or_create(name=category_name,slug=category_name)
            print (category)
            endpoint = "%sV1/categories/%s/products" % (rest_url, magento_category_id)
            headers = {"Authorization":"Bearer " + access_token}
            product_skus = requests.get(endpoint, headers=headers).json()      
            print (product_skus)
            for pkey in product_skus:
                print ("sku:"+pkey['sku'])           
        
            #key['children_data']) process second level
          

        print ("Stating Product Import")     
        endpoint = "%sV1/products?searchCriteria=0&fields=items[sku]" % (rest_url)
        headers = {"Authorization":"Bearer " + access_token}
        response = requests.get(endpoint, headers=headers).json()
        items = response['items']

        for item in items:
            endpoint = "%sV1/products/%s" % (rest_url,item['sku'])
            magento_product = requests.get(endpoint, headers=headers).json()
            print(magento_product)

            imported_product = Product.objects.create(
                name=magento_product['name'],
                price=magento_product['price'],
                product_type_id=1,
                category_id=1
                )

            ProductVariant.objects.create(
                sku = magento_product['sku'],
                name = magento_product['name'],
                price_override = magento_product['price'],
                product = imported_product
            )

            #TODO: import images
            #TODO: link products to categories
            #TODO: import options and attributes


# {'id': 2, 'sku': 'test', 'name': 'test', 'attribute_set_id': 4, 'price': 10, 'status': 1, 'visibility': 4, 'type_id': 'simple', 
# 'created_at': '2018-02-19 00:06:40', 'updated_at': '2018-02-19 00:06:40', 'weight': 6, 'extension_attributes': {'website_ids': [1],
#  'category_links': [{'position': 0, 'category_id': '2'}], 'stock_item': {'item_id': 2, 'product_id': 2, 'stock_id': 1, 'qty': 8, 
# 'is_in_stock': True, 'is_qty_decimal': False, 'show_default_notification_message': False, 'use_config_min_qty': True, 'min_qty': 0, 
# 'use_config_min_sale_qty': 1, 'min_sale_qty': 1, 'use_config_max_sale_qty': True, 'max_sale_qty': 10000, 'use_config_backorders': True, 
# 'backorders': 0, 'use_config_notify_stock_qty': True, 'notify_stock_qty': 1, 'use_config_qty_increments': True, 'qty_increments': 0, 
# 'use_config_enable_qty_inc': True, 'enable_qty_increments': False, 'use_config_manage_stock': True, 'manage_stock': True, 
# 'low_stock_date': None, 'is_decimal_divided': False, 'stock_status_changed_auto': 0}}, 'product_links': [], 'options': [],
#  'media_gallery_entries': [], 'tier_prices': [], 'custom_attributes': [{'attribute_code': 'meta_title', 'value': 'test'}, 
# {'attribute_code': 'meta_keyword', 'value': 'test'}, {'attribute_code': 'meta_description', 'value': 'test '},
#  {'attribute_code': 'category_ids', 'value': ['2']}, {'attribute_code': 'options_container', 'value': 'container2'}, 
# {'attribute_code': 'required_options', 'value': '0'}, {'attribute_code': 'has_options', 'value': '0'}, {'attribute_code': 'url_key', 
# 'value': 'test'}, {'attribute_code': 'gift_message_available', 'value': '2'}, {'attribute_code': 'tax_class_id', 'value': '
