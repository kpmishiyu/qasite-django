from django.contrib import admin
from django.urls import path, include
from django.conf import settings # 导入 settings
from django.conf.urls.static import static # 导入 static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('', include('core.urls')),
]

# 只在开发模式 (DEBUG=True) 下，才让 Django 的开发服务器处理媒体文件
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)