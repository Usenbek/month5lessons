from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Product, Category, Review
from .serializers import ProductListSerializer, ProductDetailSerializer, CategorySerializer, CategoryDetailSerializer, ReviewSerializer, ReviewDetailSerializer, ProductswithReviewsSerializer
from rest_framework import status
# Create your views here.
@api_view(http_method_names=['GET'])
def product_list_api_view(request):
    products = Product.objects.all()
    data = ProductListSerializer(products, many=True).data
    print(data)
    return Response(
        status=status.HTTP_200_OK,
        data=data
    )

@api_view(http_method_names=['GET'])
def product_detail_api_view(request, id):
    try:
        product = Product.objects.get(id=id)
    except Product.DoesNotExist:
        return Response(data={"error": "product not found"}, 
                        status=status.HTTP_404_NOT_FOUND)
    data = ProductDetailSerializer(product).data
    return Response(data=data)


@api_view(http_method_names=['GET'])
def category_list_api_view(request):
    categories = Category.objects.all()
    data = CategorySerializer(categories, many=True).data
    return Response(
        status=status.HTTP_200_OK,
        data=data
    )

@api_view(http_method_names=['GET'])
def category_detail_api_view(request, id):
    try:
        category = Category.objects.get(id=id)
    except Category.DoesNotExist:
        return Response(data={"error": "category not found"}, 
                        status=status.HTTP_404_NOT_FOUND)
    data = CategoryDetailSerializer(category).data
    return Response(data=data)


@api_view(http_method_names=['GET'])
def review_list_api_view(request):
    review = Review.objects.all()
    data = ReviewSerializer(review, many=True).data
    return Response(
        status=status.HTTP_200_OK,
        data=data
    )



@api_view(['GET'])    
def review_detail_api_view(request,id):
    try:
        review = Review.objects.get(id=id)
    except Review.DoesNotExist:
        return Response(data={'error': "review not found"},
                        status=status.HTTP_404_NOT_FOUND)
    data = ReviewDetailSerializer(review).data
    return Response(data=data)

@api_view(['GET'])
def products_with_reviews_api_view(request):
    product = Product.objects.all()
    data = ProductswithReviewsSerializer(product, many=True).data
    return Response(data=data)