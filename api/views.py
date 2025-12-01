from __future__ import annotations

from typing import Any, Dict, Optional

from django.conf import settings
from django.db import models
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_GET
from flexural.models import ConcreteGrade


def _parse_int(value: Optional[str]) -> Optional[int]:
    if value in (None, ""):
        return None
    try:
        return int(value)
    except (TypeError, ValueError):
        return None


def _grade_payload(grade: ConcreteGrade) -> Dict[str, Any]:
    image_key = grade.image_key or ""
    base_url = getattr(settings, "MINIO_PUBLIC_BASE_URL", "")
    image_url = f"{base_url}{image_key}" if image_key else None
    return {
        "id": grade.id,
        "grade_code": grade.grade_code,
        "name": grade.name,
        "description": grade.description,
        "compressive_strength_mpa": grade.compressive_strength_mpa,
        "price_per_m3_rub": grade.price_per_m3_rub,
        "image_key": grade.image_key,
        "image_url": image_url,
        "status": grade.status,
    }


@require_GET
def grade_list(request):
    """
    Возвращает список марок бетона с фильтрацией по названию и диапазону прочности.
    Параметры:
      - grade_search: подстрока для name/grade_code (регистронезависимо)
      - strength_min / strength_max: числовой диапазон compressive_strength_mpa
    """
    grade_search = (request.GET.get("grade_search") or "").strip()
    strength_min = _parse_int(request.GET.get("strength_min"))
    strength_max = _parse_int(request.GET.get("strength_max"))
    status_param = request.GET.get("status") or "active"

    qs = ConcreteGrade.objects.all()
    if status_param != "all":
        qs = qs.filter(status=ConcreteGrade.Status.ACTIVE)

    if grade_search:
        qs = qs.filter(
            models.Q(name__icontains=grade_search)
            | models.Q(grade_code__icontains=grade_search)
        )
    if strength_min is not None:
        qs = qs.filter(compressive_strength_mpa__gte=strength_min)
    if strength_max is not None:
        qs = qs.filter(compressive_strength_mpa__lte=strength_max)

    grades = [_grade_payload(grade) for grade in qs.order_by("id")]
    return JsonResponse(grades, safe=False)


@require_GET
def grade_detail(request, pk: int):
    grade = get_object_or_404(
        ConcreteGrade.objects.all(), pk=pk, status=ConcreteGrade.Status.ACTIVE
    )
    return JsonResponse(_grade_payload(grade))


@require_GET
def cart_summary(request):
    """
    По требованиям ЛР5 метод возвращает заглушку (0, -1), без ошибок авторизации.
    """
    # Даже если расчёты существуют, на этапе ЛР5 фронтенду достаточно фиксированных значений.
    return JsonResponse({"id": -1, "count": 0})


# ============================================================================
# Authentication API endpoints (для тестирования в Insomnia)
# ============================================================================

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import json


@csrf_exempt
@require_http_methods(["POST"])
def api_login(request):
    """
    POST /api/auth/login/
    Body: {"username": "...", "password": "..."}
    """
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON"}, status=400)
    
    username = data.get("username")
    password = data.get("password")
    
    if not username or not password:
        return JsonResponse({"error": "Username and password required"}, status=400)
    
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return JsonResponse({
            "success": True,
            "user": {
                "id": user.id,
                "username": user.username,
                "email": user.email,
            }
        })
    else:
        return JsonResponse({"error": "Invalid credentials"}, status=401)


@csrf_exempt
@require_http_methods(["POST"])
def api_logout(request):
    """
    POST /api/auth/logout/
    """
    logout(request)
    return JsonResponse({"success": True})


@csrf_exempt
@require_http_methods(["POST"])
def api_register(request):
    """
    POST /api/auth/register/
    Body: {"username": "...", "password": "...", "email": "..."}
    """
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON"}, status=400)
    
    username = data.get("username")
    password = data.get("password")
    email = data.get("email", "")
    
    if not username or not password:
        return JsonResponse({"error": "Username and password required"}, status=400)
    
    if User.objects.filter(username=username).exists():
        return JsonResponse({"error": "Username already exists"}, status=400)
    
    user = User.objects.create_user(username=username, password=password, email=email)
    login(request, user)
    
    return JsonResponse({
        "success": True,
        "user": {
            "id": user.id,
            "username": user.username,
            "email": user.email,
        }
    }, status=201)


@require_GET
def api_user_me(request):
    """
    GET /api/auth/me/
    """
    if request.user.is_authenticated:
        return JsonResponse({
            "id": request.user.id,
            "username": request.user.username,
            "email": request.user.email,
        })
    else:
        return JsonResponse({"error": "Not authenticated"}, status=401)


