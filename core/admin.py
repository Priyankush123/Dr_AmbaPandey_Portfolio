from django.contrib import admin
from .models import Visitor, Paper, AccessLog, AcademicSection

admin.site.register(Visitor)
admin.site.register(Paper)
admin.site.register(AccessLog)

@admin.register(AcademicSection)
class AcademicSectionAdmin(admin.ModelAdmin):
    list_display = ("section_type", "title", "year")
    list_filter = ("section_type",)
    search_fields = ("title", "description")
