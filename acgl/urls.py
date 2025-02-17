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

urlpatterns = [
    path("", views.index,name='home'),
    path("about",views.about,name='about'),
    path("login",views.login,name='login'),
    path("account",views.account,name='account'),
    path("rfq",views.rfq,name='rfq'),
    path("rfq2",views.rfq2,name='rfq2'),
    path("otp",views.otp,name='otp'),
    path("company",views.company,name='company'),
    path("service",views.service,name='service'),
    path("contact",views.contact,name='contact'),
    path("account2",views.account2,name='account2'),
    path('save_vendor_details/',views.save_vendor_details,name='save_vendor_details'),
    path('upload_documents/',views.upload_documents,name='upload_documents'),
    path('login_details/',views.login_details,name='login_details'),
    path('dashboard',views.dashboard,name='dashboard'),
    path('check-username/', views.check_username, name='check-username'),
    path('user', views.user, name='user')
]
