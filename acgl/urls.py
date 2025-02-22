from django.contrib import admin
from django.urls import path
from acgl import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("", views.login, name='home'),
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
    path('vendor', views.vendor, name='vendor'),  # Unified vendor view for all roles
    path('annexure', views.annexure, name='annexure'),
    path('po', views.po, name='po'),
    path('rfq3', views.rfq3, name='rfq3'),
    path('download/<str:file_field>/<int:vendor_id>/', views.download_file, name='download_file'),
    path('submit_requirement/', views.submit_requirement, name='submit_requirement'),
    path('cfo_dashboard/', views.cfo_dashboard, name='cfo_dashboard'),
    path('ceo_dashboard/', views.ceo_dashboard, name='ceo_dashboard'),
    path('hod_dashboard/', views.hod_dashboard, name='hod_dashboard'),
    path('design_head_dashboard/', views.design_head_dashboard, name='design_head_dashboard'),
    path('quality_head_dashboard/', views.quality_head_dashboard, name='quality_head_dashboard'),
    path('finance_head_dashboard/', views.finance_head_dashboard, name='finance_head_dashboard'),
    path('cfo_review/', views.cfo_review_list, name='cfo_review_list'),
    path('ceo_review/', views.ceo_review_list, name='ceo_review_list'),
    path('cfo_review/<int:requirement_id>/', views.cfo_review, name='cfo_review'),
    path('ceo_review/<int:requirement_id>/', views.ceo_review, name='ceo_review'),
    path('logout/', views.logout, name='logout'),  # Add this line for logout
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),  # Ensure this line is present
    path('generate_pdf/<int:requirement_id>/', views.generate_pdf, name='generate_pdf'),
    path("update_delivery_address/<int:requirement_id>/", views.update_delivery_address, name="update_delivery_address"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)