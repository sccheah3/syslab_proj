from django.contrib import admin

# Register your models here.
from linpack_bench_app.models import Linpack
from .models import System, DIMM

class LinpackInline(admin.TabularInline):
	model = Linpack

class DIMMInline(admin.TabularInline):
	model = DIMM

class SystemAdmin(admin.ModelAdmin):
	inlines = [DIMMInline, LinpackInline]


admin.site.register(System, SystemAdmin)