from django.urls import path
from django.views.generic.base import RedirectView
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView

app_name = 'api-docs'
view_name = 'schema'

urlpatterns = [
    path('schema', SpectacularAPIView.as_view(), name=view_name),
    path('redoc', SpectacularRedocView.as_view(url_name=f'{app_name}:{view_name}'), name='redoc'),
    path('swagger-ui', SpectacularSwaggerView.as_view(url_name=f'{app_name}:{view_name}'), name='swagger-ui'),
    path('', RedirectView.as_view(pattern_name=f'{app_name}:swagger-ui'), name='index'),
]
