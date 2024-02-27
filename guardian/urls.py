"""
URL configuration for guardian project.

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
from django.urls import include, path
from django.views.generic import TemplateView
from django.conf import settings
from django.conf.urls.static import static
from django.views.i18n import set_language
from django.conf.urls.i18n import urlpatterns as i18n_urlpatterns

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('dashboard.urls')),
    path('users/', include('users.urls')),
    path('configuration/', include('geoapp.urls')),
    path('journeylog/', include('journeylog.urls')),
    path('about/', include('about_us_app.urls')),
    path('tables/', include('tables.urls')),
    path('notifications/', include('notices.urls')),
    path('devices/', include('mqtt_client.urls')),
    path('medical_card/', include('animals.urls')),
    path('i18n/setlang/', set_language, name='set_language'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)