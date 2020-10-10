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
from django.contrib.auth import views as auth_views
from catalog.views import registration_view, logout_view,login_view, account_view, shuffle_view, home,about_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('catalog/', home, name='home'),

    path('register/', registration_view, name='register'),
    path('logout/',logout_view,name='logout'),
    path('login/',login_view,name='login'),
    path('account/', account_view,name='account'),
    path('about/', about_view,name='about'),
    # path('shuffle/', shuffle_view,name='shuffle'),
    url(r'^shuffle/(?P<combined_string>.+?)$', shuffle_view,name='shuffle'),
    path('password_reset',auth_views.PasswordResetView.as_view(),name='password_reset'),
    path('password_reset_done', auth_views.PasswordResetDoneView.as_view(),name='password_reset_done'),
    path('password_reset_confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(),name='password_reset_confirm'),
    path('password_reset_complete', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
