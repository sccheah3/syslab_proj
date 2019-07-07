from django.contrib import admin
from django.urls import path, include
from django.views.generic.base import TemplateView

from . import views

app_name = "linpack"

urlpatterns = [
    path('', views.index, name='index'),
	path('upload_zipfile/', views.upload_zipfile, name='upload_zipfile'),
	path('linpack_db/', views.linpack_db, name='linpack_db'),
	path('linpack_db/<int:system_id>/', views.detail, name='detail'),
]
