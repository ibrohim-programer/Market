from rest_framework import serializers
from .models import CategoryModel, ProductModel

class CategorySerializers(serializers.ModelSerializer):
    class Meta:
        model = CategoryModel
        fields = ('id', 'title', 'slug')
        read_only_fields = ('id', 'slug')

class ProductSerializers(serializers.ModelSerializer):
    total_likes = serializers.IntegerField(read_only=True)
    user = serializers.StringRelatedField(read_only=True) 

    class Meta:
        model = ProductModel
        fields = [
            'id', 'category', 'user', 'name', 
            'bio', 'price', 'is_available', 
            'total_likes', 'created_at'
        ]
        read_only_fields = ['id', 'user', 'created_at'] 
        
    def validate_price(self, value):
        if value <= 0:
            raise serializers.ValidationError("Narx 0 dan baland bo'lishi shart.")
        return value