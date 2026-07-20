from rest_framework import serializers
from .models import Category, Products

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'  # Kategorideki tüm alanları (id, title, slug) JSON'a çevir

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Products
        fields = '__all__'  # Üründeki tüm alanları JSON'a çevir