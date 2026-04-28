from django.db import models
from datetime import datetime
from django.contrib.auth.models import AbstractUser
class CustomUser(AbstractUser):
    
    ROLE_CHOICE = (
        ("Customer" , "Customer"),
        ("Seller" , "Seller"),
    )
    role = models.CharField(choices=ROLE_CHOICE , max_length=9 , default=ROLE_CHOICE[0][0])
    email = models.EmailField(max_length=200 , unique=True )
    username = models.CharField(max_length=200 , unique=True)
    phone = models.CharField(null=True , blank=True , max_length=14)
    name = models.CharField(null=True , blank=True , max_length=200)
    birthday = models.IntegerField(null=True, blank=True)
    bio = models.TextField(null=True, blank=True)
    image = models.ImageField(upload_to='image/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def save(self, *arg , **kwargs ):
        if self.username:
            self.username = self.username.capitalize()
            
        if self.birthday:  
            yil_now = datetime.now().year
            self.birthday = yil_now - int(self.birthday)
        super().save(*arg , **kwargs)

    @property
    def age(self):
        return datetime.now().year - self.birthday
    
    @property
    def is_seller(self):
        return self.role == 'Seller'
    
    @property
    def is_customer(self):
        return self.role == 'Customer'
    
    def __str__(self):
        return self.email
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    