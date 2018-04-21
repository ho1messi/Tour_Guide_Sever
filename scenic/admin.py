from django.contrib import admin
from django.contrib.auth.models import Group
from . import models

admin.site.unregister(Group)

# Register your models here.

admin.site.register(models.ScenicArea)
admin.site.register(models.ScenicSpot)
