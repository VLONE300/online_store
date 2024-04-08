from rest_framework import serializers
from catalog.models import Category, Product, ProductImage, Seller, Discount, Order, OrderProducts, Promocode, CashBack
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


class OrderProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderProducts
        fields = ('product', 'count')


class PromocodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Promocode
        fields = ('id',)


class OrderSerializer(serializers.ModelSerializer):
    products = OrderProductSerializer(many=True, write_only=True)
    use_cashback = serializers.BooleanField(write_only=True)
    promocode = serializers.CharField(max_length=50, write_only=True)

    class Meta:
        model = Order
        fields = (
            'created_at', 'delivery_address',
            'delivery_method', 'payment_method',
            'payment_status', 'status',
            'total_sum', 'delivery_notification_before',
            'products', 'promocode', 'use_cashback',
        )
        read_only_fields = ('created_at', 'payment_status', 'status', 'total_sum')

    def create(self, validated_data):
        products = validated_data.pop('products')
        use_cashback = validated_data.pop('use_cashback')
        promocode_name = validated_data.pop('promocode')
        promocode = Promocode.objects.filter(name=promocode_name).first()
        if promocode:
            delta_promocode = date.today() - promocode.date_end
            if delta_promocode.days > 0:
                promocode.percent = 0

        total_sum = 0

        for record in products:
            product = record.get('product')
            count = record.get('count')

            if product.discount:
                discount_date_end = product.discount.date_end
                date_today = date.today()
                delta = date_today - discount_date_end
                if delta.days <= 0:
                    discount_percent = product.discount.percent
                    total_sum += (product.price * (100 - discount_percent) / 100) * count
                else:
                    total_sum += product.price * count
            else:
                total_sum += product.price * count
        if promocode and promocode.is_cumulative:
            total_sum += total_sum * (100 - promocode.percent) / 100

        user = self.context['request'].user

        cash_back = CashBack.objects.all().first()
        if use_cashback:
            allow_to_pay_by_points = total_sum * (100 - cash_back.percent) / 100
            if allow_to_pay_by_points >= allow_to_pay_by_points:
                total_sum -= allow_to_pay_by_points
                user.cashback_points -= allow_to_pay_by_points
            else:
                total_sum -= user.cashback_points
                user.cashback_points = 0
        user.save()
        print(validated_data)
        order = Order.objects.create(total_sum=total_sum, user=user, **validated_data)

        for product in products:
            OrderProducts.objects.create(order=order, **product)

        return order
