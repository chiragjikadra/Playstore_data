from django.contrib import admin

# Register your models here.

from .models import *


admin.site.register(Package)
admin.site.register(PackageDetail)