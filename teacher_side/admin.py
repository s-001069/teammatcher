from django.contrib import admin
from .models import TeamNameTemplate, CSVGeneration


@admin.register(TeamNameTemplate)
class TeamNameTemplateAdmin(admin.ModelAdmin):
    list_display = ('name', 'team_count', 'is_default', 'created_at')
    list_filter = ('is_default', 'created_at')
    search_fields = ('name',)
    
    def team_count(self, obj):
        return len(obj.team_names)
    team_count.short_description = 'Number of Teams'


@admin.register(CSVGeneration)
class CSVGenerationAdmin(admin.ModelAdmin):
    list_display = ('generated_at', 'student_count', 'team_size', 'template_used')
    list_filter = ('generated_at', 'template_used')
    readonly_fields = ('generated_at', 'csv_data', 'team_size', 'template_used', 'student_count')
    
    def has_add_permission(self, request):
        return False

