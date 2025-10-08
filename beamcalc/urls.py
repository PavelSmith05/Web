from django.urls import path
from flexural.views import grade_list, grade_detail, calculation_detail, add_to_calculation, delete_calculation, delete_calculation_item

urlpatterns = [
    path("", grade_list, name="grade_list"),
    path("grade/<int:grade_id>/", grade_detail, name="grade_detail"),
    path("beam-calculation/<int:calc_id>/", calculation_detail, name="calculation_detail"),
    path("calculation/add/<int:grade_id>/", add_to_calculation, name="calc_add"),
    path("calculation/<int:calc_id>/delete/", delete_calculation, name="calc_delete"),
    path("calculation/<int:calc_id>/item/<int:item_id>/delete/", delete_calculation_item, name="calc_item_delete"),
]
