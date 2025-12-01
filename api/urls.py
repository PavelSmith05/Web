from django.urls import path

from . import views

urlpatterns = [
    path("grades/", views.grade_list, name="api_grade_list"),
    path("grades/<int:pk>/", views.grade_detail, name="api_grade_detail"),
    path("cart/", views.cart_summary, name="api_cart_summary"),
    # Authentication endpoints
    path("auth/login/", views.api_login, name="api_login"),
    path("auth/logout/", views.api_logout, name="api_logout"),
    path("auth/register/", views.api_register, name="api_register"),
    path("auth/me/", views.api_user_me, name="api_user_me"),
]

