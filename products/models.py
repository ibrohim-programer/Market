from django.db import models
from  django.contrib.auth import get_user_model
from django.utils.text import slugify


User = get_user_model()

class CategoryModel(models.Model):
    title = models.CharField(max_length=500)
    slug = models.SlugField(null=True,blank=True , max_length=500 , unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self , *args , **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args , **kwargs)
            
    def __str__(self):
        return self.title

class ProductModel(models.Model):
    category = models.ForeignKey(CategoryModel, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE , related_name='products')
    name = models.CharField(max_length=950)
    bio = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    is_available = models.BooleanField(default=True)
    likes = models.ManyToManyField(User , related_name='likes_product' , blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def total_likes(self):
        return self.likes.count()
    
    def __str__(self):
        return self.name
