from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import FeedbackCallViewSet, FeedbackQuestionViewSet


router = DefaultRouter()
router.register('call', FeedbackCallViewSet, basename='feedback-call-create')
router.register('question', FeedbackQuestionViewSet, basename='feedback-question-create')

urlpatterns = [
    path('', include(router.urls)),
]
