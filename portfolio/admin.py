from django.contrib import admin
from .models import Technology, Project

@admin.register(Technology)
class TechnologyAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at')
    list_filter = ('technologies', 'created_at')
    search_fields = ('title', 'description')
    filter_horizontal = ('technologies',)
    readonly_fields = ('created_at',)
