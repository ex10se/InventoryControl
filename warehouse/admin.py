from django.contrib import admin

from . import models


@admin.register(models.Item)
class UserProfileAdmin(admin.ModelAdmin):
    pass
