from rest_framework import serializers

from tdmvp_back.apps.news.models import News, NewsTag


class NewsTagsSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewsTag
        fields = ['id', 'name']


class NewsListSerializer(serializers.ModelSerializer):
    tags = serializers.StringRelatedField(many=True, read_only=True)

    class Meta:
        model = News
        fields = ['title', 'slug', 'image', 'short_description', 'tags']


class NewsDetailSerializer(serializers.ModelSerializer):
    tags = serializers.StringRelatedField(many=True, read_only=True)
    related_news = NewsListSerializer(many=True, read_only=True)

    class Meta:
        model = News
        fields = ['title', 'slug', 'image', 'description', 'tags', 'date', 'related_news']

    def to_representation(self, obj):
        request = self.context.get('request')
        ret = super().to_representation(obj)
        queryset = News.objects.filter(is_active=True).exclude(id=obj.id)[:3]
        serializer = NewsListSerializer(queryset, many=True, context={'request': request})
        ret['related_news'] = serializer.data
        return ret
