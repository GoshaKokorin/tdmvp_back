from rest_framework import serializers

from tdmvp_back.apps.catalog.models import Category, Product, ProductImage, ProductCharacteristic, ProductTag


class CategoryListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['name', 'slug', 'image']


class ProductTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductTag
        fields = ['id', 'name']


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['name', 'slug']


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['image', 'position']


class ProductCharacteristicSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductCharacteristic
        fields = ['name', 'value', 'position']


class ProductListSerializer(serializers.ModelSerializer):
    tags = serializers.StringRelatedField(many=True, read_only=True)
    product_images = ProductImageSerializer(many=True, read_only=True)
    category = CategorySerializer(read_only=True)

    class Meta:
        model = Product
        fields = ['category', 'slug', 'name', 'short_description', 'product_images', 'tags', 'price']


class ProductDetailSerializer(serializers.ModelSerializer):
    product_images = ProductImageSerializer(many=True, read_only=True)
    category = serializers.StringRelatedField(read_only=True)
    tags = serializers.StringRelatedField(many=True, read_only=True)
    product_characteristics = ProductCharacteristicSerializer(many=True, read_only=True)
    related_products = ProductListSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = [
            'id', 'category', 'tags', 'slug', 'name', 'description', 'price', 'additional_title',
            'additional_description', 'advantages', 'accessories', 'guarantees', 'product_images',
            'product_characteristics', 'related_products',
        ]

    def to_representation(self, obj):
        request = self.context.get('request')
        ret = super().to_representation(obj)
        queryset = Product.objects.filter(is_active=True).exclude(id=obj.id).order_by('?')[:4]
        serializer = ProductListSerializer(queryset, many=True, context={'request': request})
        ret['related_products'] = serializer.data
        return ret
