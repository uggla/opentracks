# -*- coding: utf-8 -*-

from django.contrib import admin
from ot_logbook.models import Subcategory, Category, Location, Equipment, EquipmentData, Activity, ActivityData, UserData, Settings

class ActivityAdmin(admin.ModelAdmin):
    list_display = ('datetime', 'category', 'subcat', 'location')

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'subcategory')

admin.site.register(Subcategory)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Location)
admin.site.register(Equipment)
admin.site.register(EquipmentData)
admin.site.register(Activity, ActivityAdmin)
admin.site.register(ActivityData)
admin.site.register(UserData)
admin.site.register(Settings)
