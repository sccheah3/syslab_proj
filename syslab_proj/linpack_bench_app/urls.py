from django.contrib import admin
from django.urls import path, include
from django.views.generic.base import TemplateView

from . import views

app_name = "linpack"

urlpatterns = [
    path('', views.index, name='index'),
	path('upload_zipfile/', views.upload_zipfile, name='upload_zipfile'),
	path('linpacks/', views.linpacks, name='linpacks'),
	path('linpack_systems/', views.linpack_systems, name='linpack_systems'),
	path('linpack_systems/<int:system_id>/', views.detail, name='detail'),
	path('linpack_systems/performance_comparison/', views.performance_comparison, name='performance_comparison'),
]
