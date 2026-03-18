from django.contrib import admin

from .models import TastingRecord


@admin.register(TastingRecord)
class TastingRecordAdmin(admin.ModelAdmin):
    list_display = ["__str__", "rating", "location", "date"]
    list_filter = ["rating"]
    search_fields = ["items__name", "notes", "location", "participants"]
    date_hierarchy = "date"
    ordering = ["-date"]
    filter_horizontal = ["items"]
