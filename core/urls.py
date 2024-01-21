"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from apps.views import generate_file_app, generate_pdf, download_app
from schema_graph.views import Schema
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
urlpatterns = [
    path('01641501/admin/', admin.site.urls),
    # path('', include('admin_soft.urls')),

    # path('', include('admin_material.urls')),
    path('01641501/', include('dashboard.urls')),
    path("", download_app, name="download_page"),
    path('generate-pdf/<int:order_id>/', generate_pdf, name='generate_pdf'),
    path('generate-app-file/', generate_file_app, name='generate_app'),

    path('schema/', Schema.as_view()),
    path('api/', include('apps.urls')),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/doc/',
         SpectacularSwaggerView.as_view(url_name='schema'), name='api_doc'),
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += staticfiles_urlpatterns()
