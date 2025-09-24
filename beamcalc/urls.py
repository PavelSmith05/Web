from django.urls import path
from flexural.views import grade_list, grade_detail, calculation_detail

urlpatterns = [
    path("", grade_list, name="grade_list"),
    path("grade/<int:grade_id>/", grade_detail, name="grade_detail"),
    path("calculation/<int:calc_id>/", calculation_detail, name="calculation_detail"),
]
