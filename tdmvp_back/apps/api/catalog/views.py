from django_filters.rest_framework import FilterSet, filters, DjangoFilterBackend
from django_filters.widgets import CSVWidget
from rest_framework import mixins, viewsets, permissions, generics
from rest_framework.response import Response

from tdmvp_back.apps.api.mixins import MultiSerializerViewSetMixin
from tdmvp_back.apps.api.pagination import PageNumberPagination
from tdmvp_back.apps.catalog.models import Category, Product
from .serializers import CategoryListSerializer, ProductListSerializer, ProductDetailSerializer, ProductTagSerializer


class CategoryViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Category.objects.all()
    serializer_class = CategoryListSerializer
    lookup_field = 'slug'
    permission_classes = [permissions.AllowAny]

    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


class ProductViewSet(
    MultiSerializerViewSetMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Product.objects.filter(is_active=True)
    serializer_classes = {
        'retrieve': ProductDetailSerializer,
        'list': ProductListSerializer,
    }
    pagination_class = PageNumberPagination
    permission_classes = [permissions.AllowAny]
    lookup_field = 'slug'

    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        self.get_serializer(request)
        return super().retrieve(request, *args, **kwargs)


class ProductFilter(FilterSet):
    tags = filters.BaseCSVFilter(
        distinct=True, widget=CSVWidget(), method='filter_tags'
    )

    class Meta:
        model = Product
        fields = ['tags']

    @staticmethod
    def filter_tags(queryset, field_name, value):
        qs = queryset
        for i in value:
            qs = qs.filter(tags=i)
        return qs


# TODO: fix неправильный слаг
class CatalogProductAPIView(generics.ListAPIView):
    serializer_class = ProductListSerializer
    pagination_class = PageNumberPagination
    permission_classes = [permissions.AllowAny]

    filter_backends = [DjangoFilterBackend]
    filterset_class = ProductFilter

    def get(self, request, *args, **kwargs):
        product_response = self.list(request, *args, **kwargs)

        category = Category.objects.get(slug=self.kwargs['slug'])
        category_tags_serializer = ProductTagSerializer(category.tags.all(), many=True)

        return Response({
            "category_tags": category_tags_serializer.data,
            "products": product_response.data,
        })

    def get_queryset(self):
        slug = self.kwargs['slug']
        return Product.objects.filter(category__slug=slug).filter(is_active=True)
