from django.urls import path
from .views import (
    CategoryListCreateView, 
    ProductListView, 
    ProductDetailView
)

urlpatterns = [    
    # Categories
    path('categories/', CategoryListCreateView.as_view(), name='category-list'),
    
    # Products
    path('products/', ProductListView.as_view(), name='product-list-create'),
    path('products/<int:pk>/', ProductDetailView.as_view(), name='product-detail'),
]