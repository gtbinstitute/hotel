from django.contrib import admin

# Register your models here.
from .models import *


@admin.register(RoomCategory)
class RoomCategoryAdmin(admin.ModelAdmin):
    list_display = ['categoryname', 'features', 'id', 'Image']


@admin.register(RoomCategoryDetails)
class RoomDetailsAdmin(admin.ModelAdmin):
    list_display = ['roomcategoryid', 'roomoptions', 'roomprice']
