from django.contrib import admin
from .models import Animal, Photo

class PhotoInline(admin.TabularInline):
    model = Photo

class AnimalAdmin(admin.ModelAdmin):
    list_display = ('name', 'species', 'breed', 'gender', 'age', 'user', 'device')
    search_fields = ['name', 'species', 'breed', 'gender', 'user__username']
    inlines = [PhotoInline]

admin.site.register(Animal, AnimalAdmin)
admin.site.register(Photo)
