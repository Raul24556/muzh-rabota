from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from info import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("info.urls")),
    path('create-admin/', views.create_admin),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
