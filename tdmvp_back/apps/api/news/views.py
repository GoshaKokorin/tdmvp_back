from django_filters.rest_framework import DjangoFilterBackend
from django_filters.rest_framework import FilterSet, filters
from django_filters.widgets import CSVWidget
from rest_framework import mixins, viewsets, permissions
from rest_framework.response import Response

from tdmvp_back.apps.api.mixins import MultiSerializerViewSetMixin
from tdmvp_back.apps.api.pagination import PageNumberPagination
from tdmvp_back.apps.news.models import News, NewsTag
from .serializers import NewsDetailSerializer, NewsListSerializer, NewsTagsSerializer


class NewsFilter(FilterSet):
    tags = filters.BaseCSVFilter(
        distinct=True, widget=CSVWidget(), method='filter_tags'
    )

    class Meta:
        model = News
        fields = ['tags']

    @staticmethod
    def filter_tags(queryset, field_name, value):
        qs = queryset
        for i in value:
            qs = qs.filter(tags=i)
        return qs


class NewsViewSet(
    MultiSerializerViewSetMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet,
):
    queryset = News.objects.filter(is_active=True)
    serializer_classes = {
        'retrieve': NewsDetailSerializer,
        'list': NewsListSerializer,
    }
    pagination_class = PageNumberPagination
    permission_classes = [permissions.AllowAny]
    lookup_field = 'slug'

    filter_backends = [DjangoFilterBackend]
    filterset_class = NewsFilter

    def list(self, request, *args, **kwargs):
        news_response = super().list(request, *args, **kwargs)
        news_tags_serializer = NewsTagsSerializer(NewsTag.objects.all(), many=True)
        return Response({
            "news_tags": news_tags_serializer.data,
            "news": news_response.data
        })

    def retrieve(self, request, *args, **kwargs):
        self.get_serializer(request)
        return super().retrieve(request, *args, **kwargs)
