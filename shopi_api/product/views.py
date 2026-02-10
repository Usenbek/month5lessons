from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Product, Category, Review
from .serializers import Product_detail_Validater, ProductListSerializer, ProductDetailSerializer, CategorySerializer, CategoryDetailSerializer, Review_detail_Validater, ReviewSerializer, ReviewDetailSerializer, ProductswithReviewsSerializer, ProductValidater, ReviewValidater,CategoryValidater
from rest_framework import status
# Create your views here.
@api_view(http_method_names=['GET', 'POST'])
def product_list_api_view(request):
    if request.method == 'GET':
        products = Product.objects.all()
        data = ProductListSerializer(products, many=True).data
        # print(data)
        return Response(
            status=status.HTTP_200_OK,
            data=data
        )
    elif request.method == 'POST':
        prodserializer = ProductValidater(data=request.data)
        if not prodserializer.is_valid():
            return Response(data=prodserializer.errors, status=status.HTTP_400_BAD_REQUEST)
        title = prodserializer.validated_data.get('title')
        description = prodserializer.validated_data.get('description')
        price = prodserializer.validated_data.get('price')
        category_id = prodserializer.validated_data.get('category').id
        product = Product.objects.create(title=title, description=description, price=price, category_id=category_id)
        return Response(status=status.HTTP_201_CREATED, data=ProductListSerializer(product).data)

@api_view(http_method_names=['GET','PUT'])
def product_detail_api_view(request, id):
    try:
        product = Product.objects.get(id=id)
    except Product.DoesNotExist:
        return Response(data={"error": "product not found"}, 
                        status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        data = ProductDetailSerializer(product).data
        return Response(data=data)
    elif request.method == 'PUT':
        prodserializer = Product_detail_Validater(data=request.data)
        if not prodserializer.is_valid():
            return Response(data=prodserializer.errors, status=status.HTTP_400_BAD_REQUEST)
        product.title = prodserializer.validated_data.get('title')
        product.description = prodserializer.validated_data.get('description')
        product.price = prodserializer.validated_data.get('price')
        product.category = prodserializer.validated_data.get('category')
        product.save()
        return Response(status=status.HTTP_200_OK, data=ProductDetailSerializer(product).data)


@api_view(http_method_names=['GET', 'POST'])
def category_list_api_view(request):
    if request.method == 'GET':
        categories = Category.objects.all()
        data = CategorySerializer(categories, many=True).data
        return Response(
            status=status.HTTP_200_OK,
            data=data
        )
    elif request.method == 'POST':
        catserializer = CategoryValidater(data=request.data)
        if not catserializer.is_valid():
            return Response(data=catserializer.errors, status=status.HTTP_400_BAD_REQUEST)
        name = catserializer.validated_data.get('name')
        category = Category.objects.create(name=name)

        return Response(status=status.HTTP_200_OK,
                        data=CategorySerializer(category).data)


@api_view(http_method_names=['GET', 'PUT', 'DELETE'])
def category_detail_api_view(request, id):
    try:
        category = Category.objects.get(id=id)
    except Category.DoesNotExist:
        return Response(data={"error": "category not found"}, 
                        status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        data = CategoryDetailSerializer(category).data
        return Response(data=data)
    elif request.method == 'PUT':
        catserializer = CategoryValidater(data=request.data)
        if not catserializer.is_valid():
            return Response(data=catserializer.errors, status=status.HTTP_400_BAD_REQUEST)
        category.name = catserializer.validated_data.get('name')
        category.save()
        return Response(
            status=status.HTTP_200_OK,
            data=CategoryDetailSerializer(category).data)
    elif request.method == 'DELETE':
        category.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(http_method_names=['GET', 'POST'])
def review_list_api_view(request):
    if request.method == 'GET':
        review = Review.objects.all()
        data = ReviewSerializer(review, many=True).data
        return Response(
            status=status.HTTP_200_OK,
            data=data
        )
    elif request.method == 'POST':
        revserializer = ReviewValidater(data=request.data)
        if not revserializer.is_valid():
            return Response(data=revserializer.errors, status=status.HTTP_400_BAD_REQUEST)
        text = revserializer.validated_data.get('text')
        stars = revserializer.validated_data.get('stars')
        product_id = revserializer.validated_data.get('product').id
        review = Review.objects.create(text=text, stars=stars, product_id=product_id)
        return Response(status=status.HTTP_201_CREATED, data=ReviewSerializer(review).data)



@api_view(['GET', 'PUT'])    
def review_detail_api_view(request,id):
    try:
        review = Review.objects.get(id=id)
    except Review.DoesNotExist:
        return Response(data={'error': "review not found"},
                        status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        data = ReviewDetailSerializer(review).data
        return Response(data=data)
    elif request.method == 'PUT':
        revserializer = Review_detail_Validater(data=request.data)
        if not revserializer.is_valid():
            return Response(data=revserializer.errors, status=status.HTTP_400_BAD_REQUEST)
        review.text = revserializer.validated_data.get('text')
        review.stars = revserializer.validated_data.get('stars')
        # review.p = revserializer.validated_data.get('product').id
        review.save()
        return Response(status=status.HTTP_200_OK, data=ReviewDetailSerializer(review).data)

@api_view(['GET'])
def products_with_reviews_api_view(request):
    product = Product.objects.all()
    data = ProductswithReviewsSerializer(product, many=True).data
    return Response(data=data)