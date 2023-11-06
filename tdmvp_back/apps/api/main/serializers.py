from rest_framework import serializers

from tdmvp_back.apps.main.models import Main


class MainListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Main
        fields = ['title', 'image', 'description', 'link', 'position']
