from django.contrib import admin
from .models import ConcreteGrade, FlexuralCalculation, FlexuralCalculationItem

@admin.register(ConcreteGrade)
class ConcreteGradeAdmin(admin.ModelAdmin):
    list_display = ("id", "grade_code", "name", "status", "compressive_strength_mpa", "price_per_m3_rub")
    list_filter = ("status",)
    search_fields = ("grade_code", "name")
    ordering = ("id",)

class FlexuralCalculationItemInline(admin.TabularInline):
    model = FlexuralCalculationItem
    extra = 0
    raw_id_fields = ("grade",)

@admin.register(FlexuralCalculation)
class FlexuralCalculationAdmin(admin.ModelAdmin):
    list_display = ("id", "status", "creator", "created_at", "formed_at", "completed_at", "moderator",
                    "beam_length_m", "beam_width_mm", "beam_height_mm", "result_max_load_kN")
    list_filter = ("status", "creator", "moderator")
    search_fields = ("id", "creator__username")
    readonly_fields = ("created_at",)
    inlines = [FlexuralCalculationItemInline]
    ordering = ("-id",)

@admin.register(FlexuralCalculationItem)
class FlexuralCalculationItemAdmin(admin.ModelAdmin):
    list_display = ("id", "calculation", "grade", "quantity", "order_index", "is_primary")
    list_filter = ("is_primary",)
    raw_id_fields = ("calculation", "grade")
    ordering = ("calculation", "order_index")