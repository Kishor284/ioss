from django.contrib import admin
from django.urls import path
from app.views import index, redirect_view, URLCreateAPIView, URLListAPIView, delete_url

urlpatterns = [
    path('admin/', admin.site.urls),
    # Web UI
    path('', index, name='index'),
    path('<str:code>/', redirect_view, name='redirect'),

    # REST API
    path('api/urls/', URLListAPIView.as_view(), name='url-list'),
    path('api/urls/create/', URLCreateAPIView.as_view(), name='url-create'),
    path('delete/<int:id>/', delete_url, name='delete-url'),
]
