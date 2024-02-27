from django.contrib import admin
from .models import Project, Developer, FAQ

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('version', 'description')

@admin.register(Developer)
class DeveloperAdmin(admin.ModelAdmin):
    list_display = ('name', 'github_profile')

@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ('question', 'answer')
