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
        fields = ['id', 'text','stars', 'product']
        depth = 2

class ProductswithReviewsSerializer(serializers.ModelSerializer):
    reviews = ReviewSerializerforProduct(many=True, read_only=True)
    reviews_count = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ['id', 'title', 'description', 'price', 'category', 'reviews', 'reviews_count']
        
    def get_reviews_count(self, obj):
        return sum(obj.reviews.all().values_list("stars", flat=True)) / obj.reviews.count() if obj.reviews.count() > 0 else 0

class ProductValidater(serializers.Serializer):
    title = serializers.CharField(min_length=5, max_length=200)
    description = serializers.CharField(min_length=10, max_length=1000)
    price = serializers.DecimalField(max_digits=10, decimal_places=2, min_value=0.01)
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all())

class CategoryValidater(serializers.Serializer):
    name = serializers.CharField(min_length=3, max_length=100)

class Review_detail_Validater(serializers.Serializer):
    text = serializers.CharField(min_length=1, max_length=1000)
    stars = serializers.FloatField(min_value=1, max_value=5)

class ReviewValidater(serializers.Serializer):
    text = serializers.CharField(min_length=1, max_length=1000)
    stars = serializers.FloatField(min_value=1, max_value=5)
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())

class Product_detail_Validater(serializers.Serializer):
    title = serializers.CharField(min_length=5, max_length=200)
    description = serializers.CharField(min_length=10, max_length=1000)
    price = serializers.DecimalField(max_digits=10, decimal_places=2, min_value=0.01)