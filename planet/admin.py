from django.contrib import admin
from .models import Planet

# Register your models here.

class PlanetAdmin(admin.ModelAdmin):
  list_display = ("firstname", "lastname", "dob",)
  
admin.site.register(Planet, PlanetAdmin)