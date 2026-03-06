from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Product, Category, Review
from .serializers import Product_detail_Validater, ProductListSerializer, ProductDetailSerializer, CategorySerializer, CategoryDetailSerializer, Review_detail_Validater, ReviewSerializer, ReviewDetailSerializer, ProductswithReviewsSerializer, ProductValidater, ReviewValidater,CategoryValidater
from rest_framework import status
from rest_framework.generics import (ListCreateAPIView, RetrieveUpdateDestroyAPIView)
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from common.permissions import IsOwner, IsAnonymous, IsModerator

# Create your views here. 

class ProductListAPIView(ListCreateAPIView):
    queryset = Product.objects.all()
    permission_classes = [IsOwner | IsAnonymous]

    def get_serializer_class(self):
        if self.request.method == 'POST': 
            return ProductValidater 
        return ProductListSerializer
    

class ProductDetailAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    lookup_field = 'id'
    permission_classes = [IsModerator | IsAnonymous]

    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return Product_detail_Validater
        return ProductDetailSerializer


class CategoryListAPIView(ListCreateAPIView):
    queryset = Category.objects.all()
    permission_classes = [IsOwner | IsAnonymous]

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CategoryValidater
        return CategorySerializer

class CategoryDetailAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    lookup_field = 'id'
    permission_classes = [IsModerator | IsAnonymous]

    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return CategoryValidater
        return CategoryDetailSerializer



class ReviewListAPIView(ListCreateAPIView):
    queryset = Review.objects.all()
    permission_classes = [IsOwner | IsAnonymous]

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return ReviewValidater
        return ReviewSerializer

class ReviewDetailAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    lookup_field = 'id'
    permission_classes = [IsModerator | IsAnonymous]

    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return Review_detail_Validater
        return ReviewDetailSerializer
