from django.urls import re_path
from django.urls import path
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from pique import views


urlpatterns = [
    re_path(r'^$', views.home, name='home'),
    re_path(r'^register/', views.register, name='register'),
    re_path(r'^login/', views.user_login, name='login'),
    re_path(r'^logout/', views.user_logout, name='logout'),
    re_path(r'^upload/', views.model_form_upload, name='upload'),
    path('get/ajax/update/download_count', views.update_download_count, name='update_download_count')
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
