from django.contrib import admin
from .models import User
from .models import Product
from .models import Order
# Register your models here.

class UserAdmin(admin.ModelAdmin):
    list_display = ('email', )

admin.site.register(User, UserAdmin)

class ProductAdmin(admin.ModelAdmin):
    list_display = ('product_name', 'price',)

admin.site.register(Product, ProductAdmin)

class OrderAdmin(admin.ModelAdmin):
    list_display = ('user', 'products', )

admin.site.register(Order, OrderAdmin)