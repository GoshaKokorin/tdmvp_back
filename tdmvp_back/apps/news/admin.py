from django.contrib import admin

from .models import News, NewsTag


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ['title', 'date', 'is_active']
    list_editable = ['is_active']
    search_fields = ['title']


@admin.register(NewsTag)
class NewsTagAdmin(admin.ModelAdmin):
    pass
