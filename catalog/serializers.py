from rest_framework import serializers
from catalog.models import Category, Product, ProductImage, Seller, Discount
from datetime import date


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name', 'description')


class ProductImageSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(use_url=True)

    class Meta:
        model = ProductImage
        fields = ('image',)


class ProductSerializer(serializers.ModelSerializer):
    images = ProductImageSerializer(many=True, source='productimage_set')

    class Meta:
        model = Product
        fields = ('id', 'article', 'name', 'price', 'images')


class SellerSerializers(serializers.ModelSerializer):
    class Meta:
        model = Seller
        fields = ('id', 'name', 'contact')


class DiscountSerializers(serializers.ModelSerializer):
    class Meta:
        model = Discount
        fields = ('id', 'name', 'percent')


class AddProductSerializer(serializers.Serializer):
    product_id = serializers.IntegerField()
    count = serializers.IntegerField()


class ProductInCartSerializer(serializers.Serializer):
    name = serializers.CharField()
    price = serializers.DecimalField(max_digits=10, decimal_places=2)
    count = serializers.IntegerField()
    discount_percent = serializers.IntegerField()


class CartSerializer(serializers.Serializer):
    products = ProductInCartSerializer(many=True)
    result_price = serializers.SerializerMethodField()

    def get_result_price(self, data):
        result_price = 0
        for product in data.get('products'):
            price = product.get('price')
            count = product.get('count')
            if product.get('discount'):
                discount_date_end = product.get('discount_date_end')
                date_today = date.today()
                delta = date_today - discount_date_end
                if delta.days <= 0:
                    discount_percent = product.get('discount_percent')
                    result_price += (price * (100 - discount_percent) / 100) * count
                else:
                    result_price += price * count
            else:
                result_price += price * count
        return result_price


class DeleteProductSerializer(serializers.Serializer):
    product_id = serializers.IntegerField()
