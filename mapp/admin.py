from django.contrib import admin
from . models import *
# Register your models here.
@admin.register(Main_User_Table)
class Main_User_Table_Admin(admin.ModelAdmin):
  list_display  = [f.name for f in Main_User_Table._meta.fields]


@admin.register(Premium_User_Table)
class Premium_User_Table_Admin(admin.ModelAdmin):
  list_display  = [f.name for f in Premium_User_Table._meta.fields]

@admin.register(Area)
class Area_Admin(admin.ModelAdmin):
  list_display  = [f.name for f in Area._meta.fields]

@admin.register(Village)
class Village_Admin(admin.ModelAdmin):
  list_display  = [f.name for f in Village._meta.fields]