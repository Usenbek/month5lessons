from rest_framework import serializers
from .models import Product, Category, Review

class ReviewSerializerforProduct(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = 'text stars'.split()

class ProductDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'title', 'description', 'price', 'category', 'reviews']
        depth = 1


class ProductListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'title', 'description', 'price', 'category']
        depth = 1

class CategorySerializer(serializers.ModelSerializer):
    products_count = serializers.SerializerMethodField()
    class Meta:
        model = Category
        fields = ['id', 'name','products_count']
        
    def get_products_count(self,obj):
        return obj.products.count()  

class CategoryDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']

class ReviewSerializer(serializers.ModelSerializer):
    reviews = ReviewSerializerforProduct(many=True, read_only=True)
    class Meta:
        model = Review
        fields = ['id', 'text', 'product', 'stars']
        depth = 1

class ReviewDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id', 'text', 'product', 'stars']
        depth = 2

class ProductswithReviewsSerializer(serializers.ModelSerializer):
    reviews = ReviewSerializerforProduct(many=True, read_only=True)
    reviews_count = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ['id', 'title', 'description', 'price', 'category', 'reviews', 'reviews_count']
        
    def get_reviews_count(self, obj):
        return sum(obj.reviews.all().values_list("stars", flat=True)) / obj.reviews.count() if obj.reviews.count() > 0 else 0