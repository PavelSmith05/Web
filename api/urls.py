from django.urls import path

from . import views

urlpatterns = [
    path("grades/", views.grade_list, name="api_grade_list"),
    path("grades/<int:pk>/", views.grade_detail, name="api_grade_detail"),
    path("cart/", views.cart_summary, name="api_cart_summary"),
]

