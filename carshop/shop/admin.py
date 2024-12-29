from django.contrib import admin
from .models import ProductType, Supplier, Product, Manufacturer, Customer, Sale

admin.site.register(ProductType)
admin.site.register(Supplier)
admin.site.register(Product)
admin.site.register(Manufacturer)
admin.site.register(Customer)
admin.site.register(Sale)
