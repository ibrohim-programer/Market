from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView , UpdateAPIView , DestroyAPIView 

from rest_framework.permissions import IsAdminUser, AllowAny, IsAuthenticated
from drf_spectacular.utils import extend_schema
from common.permissions import IsOwner, Seller
from .serialezirs import CategorySerializers, ProductSerializers
from .models import CategoryModel, ProductModel


'''Caregore'''
@extend_schema(tags=['Categories'])
class CategoryListCreateView(ListCreateAPIView):
    queryset = CategoryModel.objects.all()
    serializer_class = CategorySerializers
    
    def get_permissions(self):
        if self.request.method == 'GET':
            return [AllowAny()]
        return [IsAuthenticated(), IsAdminUser()]
    
    
@extend_schema(tags=['Product - Category - Crud'])
class CategoryUpdateView(UpdateAPIView):
    queryset = CategoryModel.objects.all()
    serializer_class = CategorySerializers
    permission_classes = [IsAuthenticated , IsAdminUser]
    
@extend_schema(tags=['Product - Category - Crud'])
class CategoryDeleteView(DestroyAPIView):
    queryset = CategoryModel.objects.all()
    serializer_class = CategorySerializers
    permission_classes = [IsAuthenticated , IsAdminUser]

'''Product'''
@extend_schema(tags=['Products'])
class ProductListView(ListCreateAPIView):
    """
    Mahsulotlarni ko'rish va yaratish (faqat Sellerlar uchun).
    """
    serializer_class = ProductSerializers
    
    def get_queryset(self):
        return ProductModel.objects.select_related('category', 'user').all()

    def get_permissions(self):
        if self.request.method == 'GET':
            return [AllowAny()]
        return [IsAuthenticated(), Seller()]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)    
        
        
@extend_schema(tags=['Products'])
class ProductDetailView(RetrieveUpdateDestroyAPIView):
    serializer_class = ProductSerializers
    permission_classes = [IsAuthenticated, IsOwner]
    http_method_names = ['put' , 'delete']
    def get_queryset(self):
        return ProductModel.objects.filter(user=self.request.user)