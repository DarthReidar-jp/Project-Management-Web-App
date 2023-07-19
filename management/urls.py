from django.contrib import admin
from django.urls import path, include
from projectManagement.views import welcome_view
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', welcome_view, name='welcome'),
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('app/', include('projectManagement.urls')),
]
if settings.DEBUG:  # only serve media files in development
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
