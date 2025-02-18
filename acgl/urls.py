"""
URL configuration for website project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.urls import path
from acgl import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("", views.index, name='home'),
    path("about", views.about, name='about'),
    path("login", views.login, name='login'),
    path("account/", views.account, name='account'),
    path("rfq", views.rfq, name='rfq'),
    path("rfq2", views.rfq2, name='rfq2'),
    path("otp", views.otp, name='otp'),
    path("company", views.company, name='company'),
    path("service", views.service, name='service'),
    path("contact", views.contact, name='contact'),
    path("account2/", views.account2, name='account2'),
    path("account3/", views.account3, name='account3'),
    path('login_details/', views.login_details, name='login_details'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('check-username/', views.check_username, name='check-username'),
    path('user', views.user, name='user'),
    path('vendor', views.vendor, name='vendor'),
    path('download/<str:file_field>/<int:vendor_id>/', views.download_file, name='download_file'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)