from django.conf import settings
from django.contrib import admin
from django.urls import path,include
from django.conf.urls.static import static
from ReportSystem import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('ReportSystem.urls')),
]+static(settings.MEDIA_URL,documentsroot=settings.MEDIA_ROOT)
