"""DishuffleApp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.conf.urls import url
from django.contrib import admin
from django.urls import path
from django.urls import include
from django.views.generic import RedirectView
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.auth import views
from catalog.views import registration_view, logout_view,login_view, account_view, shuffle_view,about_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('catalog/', include('catalog.urls')),
    path('', RedirectView.as_view(url='catalog/', permanent=True)),
    path('register/', registration_view, name='register'),
    path('logout/',logout_view,name='logout'),
    path('login/',login_view,name='login'),
    path('account/', account_view,name='account'),
    path('about/', about_view,name='about'),
    # path('shuffle/', shuffle_view,name='shuffle'),
    url(r'^shuffle/(?P<combined_string>.+?)$', shuffle_view,name='shuffle'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
