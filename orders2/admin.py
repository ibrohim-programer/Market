from django.contrib import admin
from .models import *

@admin.register(CartModel)
class CartAdmin(admin.ModelAdmin):
    list_display = ('id','user')


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('id',"cart", 'total_price')


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id' , 'user' , 'product' , 'status',]