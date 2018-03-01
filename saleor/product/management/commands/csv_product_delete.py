import csv
from django.core.management import BaseCommand
import requests
import json
from saleor.product.models import Category, Collection, Product,ProductVariant,ProductImage
from django.conf import settings
from decimal import Decimal
#sku,store_view_code,attribute_set_code,product_type,categories,product_websites,name,description,short_description,weight,product_online,tax_class_name,visibility,price,special_price,special_price_from_date,special_price_to_date,url_key,meta_title,meta_keywords,meta_description,base_image,base_image_label,small_image,small_image_label,thumbnail_image,thumbnail_image_label,swatch_image,swatch_image_label,created_at,updated_at,new_from_date,new_to_date,display_product_options_in,map_price,msrp_price,map_enabled,gift_message_available,custom_design,custom_design_from,custom_design_to,custom_layout_update,page_layout,product_options_container,msrp_display_actual_price_type,country_of_manufacture,additional_attributes,qty,out_of_stock_qty,use_config_min_qty,is_qty_decimal,allow_backorders,use_config_backorders,min_cart_qty,use_config_min_sale_qty,max_cart_qty,use_config_max_sale_qty,is_in_stock,notify_on_stock_below,use_config_notify_stock_qty,manage_stock,use_config_manage_stock,use_config_qty_increments,qty_increments,use_config_enable_qty_inc,enable_qty_increments,is_decimal_divided,website_id,related_skus,related_position,crosssell_skus,crosssell_position,upsell_skus,upsell_position,additional_images,additional_image_labels,hide_from_product_page,custom_options,bundle_price_type,bundle_sku_type,bundle_price_view,bundle_weight_type,bundle_values,bundle_shipment_type,configurable_variations,configurable_variation_labels,associated_skus
#test,,Default,simple,"Default Category",base,test,,,6.0000,1,"Taxable Goods","Catalog, Search",10.0000,,,,test,test,test,"test ",,,,,,,,,"2/19/18, 1:06 AM","2/19/18, 1:06 AM",,,"Block after Info Column",,,,"Use config",,,,,,,,,,8.0000,0.0000,1,0,0,1,1.0000,1,10000.0000,1,1,1.0000,1,1,1,1,1.0000,1,0,0,0,,,,,,,,,,,,,,,,,,,


class Command(BaseCommand):
    help = 'Use to delete all products in a csv file by SKU'
    def handle(self, *args, **options):
        input_file = csv.DictReader(open("saleor/product/management/commands/test_data/csv/products.csv"))
        for magento_product in input_file:
            pv=ProductVariant.objects.filter(sku=magento_product['sku']).first()
            if pv:
                prod=pv.product_id
                print (prod)
                ProductImage.objects.filter(product_id=prod).delete()
                print (ProductImage.objects.filter(product_id=prod).query)
                ProductVariant.objects.filter(product_id=prod).delete()
                Product.objects.filter(pk=prod).delete()