from django.db.models import F
from rest_framework.response import Response
from catalog.models import Category, Product, Seller, Discount, Cart
from rest_framework.generics import ListAPIView
from catalog.serializers import CategorySerializer, ProductSerializer, SellerSerializers, DiscountSerializers, \
    AddProductSerializer, CartSerializer, DeleteProductSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView


class CategoryListView(ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (AllowAny,)


class CategoryProductsView(APIView):
    permission_classes = (AllowAny,)

    def get(self, request, category_id):
        queryset = Product.objects.filter(category__id=category_id)
        serializer = ProductSerializer(queryset, many=True)
        return Response(serializer.data)


class SellerListView(ListAPIView):
    queryset = Seller.objects.all()
    serializer_class = SellerSerializers
    permission_classes = (AllowAny,)


class SellerProductsView(APIView):
    permission_classes = (AllowAny,)

    def get(self, request, seller_id):
        queryset = Product.objects.filter(seller__id=seller_id)
        serializer = ProductSerializer(queryset, many=True)
        return Response(serializer.data)


class DiscountListView(ListAPIView):
    queryset = Discount.objects.all()
    serializer_class = DiscountSerializers
    permission_classes = (AllowAny,)


class DiscountProductsView(APIView):
    permission_classes = (AllowAny,)

    def get(self, request, discount_id):
        queryset = Product.objects.filter(discount__id=discount_id)
        serializer = ProductSerializer(queryset, many=True)
        return Response(serializer.data)


class CartView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        input_serializer = AddProductSerializer(data=request.data)
        input_serializer.is_valid(raise_exception=True)
        product = Product.objects.get(id=input_serializer.data['product_id'])
        cart_object, _ = Cart.objects.get_or_create(user=request.user, product=product)

        if cart_object.count:
            cart_object.count += input_serializer.data['count']
        else:
            cart_object.count = input_serializer.data['count']

        if cart_object.count <= 0:
            cart_object.delete()
        else:
            cart_object.save()

        return Response()

    def get(self, request):
        user = request.user
        cart = Product.objects.prefetch_related('cart_set').filter(cart__user=user).values(
            'name', 'price', 'discount', discount_percent=F('discount__percent'),
            count=F("cart__count"), discount_date_end=F('discount__date_end')
        )
        selializer = CartSerializer({'products': cart})
        return Response(selializer.data)

    def delete(self, request):
        input_serializer = DeleteProductSerializer(data=request.data)
        input_serializer.is_valid(raise_exception=True)

        product = Product.objects.get(id=input_serializer.data['product_id'])
        Cart.objects.get(user=request.user, product=product).delete()
        return Response()
