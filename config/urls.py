#config/urls.py

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('pybo/', include('pybo.urls')),  # 'pybo/' 경로를 이미 처리하고 있음
    path('', include('pybo.urls')),      # 빈 경로('/')에 pybo 앱 연결
]
