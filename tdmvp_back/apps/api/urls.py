from django.urls import include, path

urlpatterns = [
    path('feedback/', include('tdmvp_back.apps.api.feedbacks.urls')),
    path('catalog/', include('tdmvp_back.apps.api.catalog.urls')),
    path('news/', include('tdmvp_back.apps.api.news.urls')),
    path('main/', include('tdmvp_back.apps.api.main.urls')),
]