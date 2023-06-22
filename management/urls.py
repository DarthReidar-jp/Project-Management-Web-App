from django.contrib import admin
from django.urls import path, include
from projectManagement.views import welcome_view

urlpatterns = [
    path('', welcome_view, name='welcome'),
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('app/', include('projectManagement.urls')),
]
