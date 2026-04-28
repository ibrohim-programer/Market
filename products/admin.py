from django.contrib import admin
from .models import CategoryModel , ProductModel


@admin.register(CategoryModel)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id',"title" , 'slug',]
    
    
@admin.register(ProductModel)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['id','category','user','name','bio','price',]