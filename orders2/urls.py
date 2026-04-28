from django.urls import path
from .views import (
    MyCartListView,
    CartItemView, CartItemDeleteView,
    MyOrderCreateView, MyOrderListView,
    MyOrderDelete, MyOrderStatusUpdateView,
)

urlpatterns = [

    # ── Cart 
    path('my-cart-list/',              MyCartListView.as_view(),      name='cart-list'),
    path('my-cart-item/',              CartItemView.as_view(),         name='cart-item'),
    path('my-cart-delete/<int:pk>/',   CartItemDeleteView.as_view(),   name='cart-delete'),

    # ── Orders 
    path('my-order-create/',           MyOrderCreateView.as_view(),    name='order-create'),
    path('my-order-list/',             MyOrderListView.as_view(),      name='order-list'),
    path('my-order-delete/<int:pk>/',  MyOrderDelete.as_view(),        name='order-delete'),

    # ── Status 
    path('my-order-status/<int:pk>/',  MyOrderStatusUpdateView.as_view(), name='order-status'),
]