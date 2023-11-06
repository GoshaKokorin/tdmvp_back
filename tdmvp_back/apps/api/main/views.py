from rest_framework import mixins, viewsets, permissions
from rest_framework.response import Response

from tdmvp_back.apps.api.catalog.serializers import CategoryListSerializer
from tdmvp_back.apps.api.news.serializers import NewsListSerializer
from tdmvp_back.apps.catalog.models import Category
from tdmvp_back.apps.main.models import Main
from tdmvp_back.apps.news.models import News
from .serializers import MainListSerializer


class MainViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Main.objects.filter(is_active=True)
    permission_classes = [permissions.AllowAny]
    serializer_class = MainListSerializer

    def list(self, request, *args, **kwargs):
        main_response = super().list(request, *args, **kwargs)
        news_serializer = NewsListSerializer(
            News.objects.filter(is_active=True)[:3], many=True, context={'request': request}
        )
        category_serializer = CategoryListSerializer(Category.objects.all(), many=True, context={'request': request})
        return Response({
            "slider": main_response.data,
            "news": news_serializer.data,
            "category": category_serializer.data
        })
