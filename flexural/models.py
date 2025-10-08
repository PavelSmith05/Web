from django.conf import settings
from django.db import models
from django.db.models import Q

class ConcreteGrade(models.Model):
    class Status(models.TextChoices):
        ACTIVE = "active", "active"
        DELETED = "deleted", "deleted"

    grade_code = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=50)
    description = models.TextField()
    compressive_strength_mpa = models.IntegerField()
    price_per_m3_rub = models.IntegerField()
    image_key = models.CharField(max_length=100, blank=True, null=True)
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.ACTIVE)

    class Meta:
        db_table = "concrete_grade"
        indexes = [
            models.Index(fields=["grade_code"]),
            models.Index(fields=["status"]),
        ]

    def __str__(self) -> str:
        return f"{self.name} ({self.grade_code})"


class FlexuralCalculation(models.Model):
    class Status(models.TextChoices):
        DRAFT = "draft", "черновик"
        DELETED = "deleted", "удалён"
        FORMED = "formed", "сформирован"
        COMPLETED = "completed", "завершён"
        REJECTED = "rejected", "отклонён"

    status = models.CharField(max_length=10, choices=Status.choices, default=Status.DRAFT)
    created_at = models.DateTimeField(auto_now_add=True)
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="beam_calculations_created")
    formed_at = models.DateTimeField(blank=True, null=True)
    completed_at = models.DateTimeField(blank=True, null=True)
    moderator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, blank=True, null=True, related_name="beam_calculations_moderated")

    beam_length_m = models.DecimalField(max_digits=6, decimal_places=2)
    beam_width_mm = models.IntegerField()
    beam_height_mm = models.IntegerField()
    result_max_load_kN = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)

    class Meta:
        db_table = "flexural_calculation"
        indexes = [models.Index(fields=["status"])]
        constraints = [
            models.UniqueConstraint(
                fields=["creator"],
                condition=Q(status="draft"),
                name="uniq_draft_calculation_per_user",
            ),
        ]

    def __str__(self) -> str:
        return f"Calc #{self.pk} ({self.get_status_display()})"


class FlexuralCalculationItem(models.Model):
    calculation = models.ForeignKey(FlexuralCalculation, on_delete=models.PROTECT, related_name="items")
    grade = models.ForeignKey(ConcreteGrade, on_delete=models.PROTECT, related_name="calculation_items")
    quantity = models.IntegerField(default=1)
    order_index = models.IntegerField(default=1)
    is_primary = models.BooleanField(default=False)
    comment = models.CharField(max_length=255, blank=True, default="")

    class Meta:
        db_table = "flexural_calculation_item"
        constraints = [
            models.UniqueConstraint(fields=["calculation", "grade"], name="uniq_calc_grade"),
        ]
        indexes = [models.Index(fields=["order_index"])]

    def __str__(self) -> str:
        return f"Item(calc={self.calculation_id}, grade={self.grade_id})"