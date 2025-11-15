"""clinic_backend URL Configuration."""
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('doctors.urls')),
    path('api/patient/auth/', include('users.urls')),
    path('api/auth/', include('auth_user.urls')),
    path('api/scheduling/', include('scheduling.urls')),
]
