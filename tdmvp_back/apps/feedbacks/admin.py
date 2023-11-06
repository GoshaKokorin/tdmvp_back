from django.contrib import admin
from django.contrib.auth.models import Group, User

from .models import FeedbackCall, FeedbackQuestion


@admin.register(FeedbackCall)
class FeedbackCallAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'created_at', 'is_processed', 'is_spam']
    list_editable = ['is_processed', 'is_spam']
    fields = ['name', 'number', 'created_at', 'is_processed', 'is_spam']
    readonly_fields = ['name', 'number', 'created_at']

    def has_add_permission(self, request, obj=None):
        return False


@admin.register(FeedbackQuestion)
class FeedbackQuestionAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'created_at', 'is_processed', 'is_spam']
    list_editable = ['is_processed', 'is_spam']
    fields = ['name', 'number', 'text', 'created_at', 'is_processed', 'is_spam']
    readonly_fields = ['name', 'number', 'text', 'created_at']

    def has_add_permission(self, request, obj=None):
        return False


admin.site.unregister(Group)
admin.site.unregister(User)
