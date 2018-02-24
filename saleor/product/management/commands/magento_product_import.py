from django.core.management import BaseCommand
import requests
import json
from saleor.product.models import Category, Collection, Product,ProductVariant
from django.conf import settings

#  /V1/products/attributes
#  /V1/products/types
#  /V1/categories

class Command(BaseCommand):
    help = 'Import products'

    def handle(self, *args, **options):
        
        rest_url = settings.MAGENTO_REST_URL
        access_token = settings.MAGENTO_ACCESS_TOKEN
        
        endpoint = "http://magento2/rest/all/V1/categories/"
        headers = {"Authorization":"Bearer " + access_token}
        response = requests.get(endpoint, headers=headers).json()
        print (response)
   
        endpoint = "%sproducts?searchCriteria=0&fields=items[sku]" % (rest_url)
        headers = {"Authorization":"Bearer " + access_token}
        response = requests.get(endpoint, headers=headers).json()
        items = response['items']

        for item in items:
            endpoint = "%sproducts/%s" % (rest_url,item['sku'])
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
