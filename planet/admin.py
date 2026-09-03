from django.contrib import admin
from .models import Planet, Post

# Register your models here.

class PlanetAdmin(admin.ModelAdmin):
    list_display = ("firstname", "lastname", "dob",)

class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'description', 'content', 'image', 'date']
    list_filter = ['date']
    search_fields = ['title']

admin.site.register(Planet, PlanetAdmin)
admin.site.register(Post, PostAdmin)