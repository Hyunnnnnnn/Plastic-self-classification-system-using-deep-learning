# mysite/urls.py

from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect

urlpatterns = [
    path('admin/', admin.site.urls),
    path('camera/', include('camera.urls')),
    path('', lambda request: redirect('camera/', permanent=True)),  # 기본 경로를 camera로 리디렉션
]
