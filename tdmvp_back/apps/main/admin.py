from django.contrib import admin

from .models import Main


@admin.register(Main)
class NewsTagAdmin(admin.ModelAdmin):
    pass
