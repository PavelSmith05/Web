from django.shortcuts import render
from django.http import Http404
from django.conf import settings
from .data import CONCRETE_GRADES, CALCULATIONS

MINIO_BASE = getattr(settings, "MINIO_PUBLIC_BASE_URL", "http://localhost:9000/beam-images/")


def grade_list(request):
    q = request.GET.get("q", "").strip()
    grades = CONCRETE_GRADES
    if q:
        q_lower = q.lower()
        grades = [g for g in CONCRETE_GRADES if q_lower in g["grade_code"].lower() or q_lower in g["name"].lower()]
    calc = CALCULATIONS.get(1)
    cart_count = len(calc["selected_grades"]) if calc else 0
    context = {"grades": grades, "q": q, "calc": calc, "cart_count": cart_count, "MINIO_PUBLIC_BASE_URL": MINIO_BASE}
    return render(request, "flexural/grade_list.html", context)


def grade_detail(request, grade_id: int):
    grade = next((g for g in CONCRETE_GRADES if g["id"] == grade_id), None)
    if grade is None:
        raise Http404()
    calc = CALCULATIONS.get(1)
    context = {"grade": grade, "calc": calc, "MINIO_PUBLIC_BASE_URL": MINIO_BASE}
    return render(request, "flexural/grade_detail.html", context)


def calculation_detail(request, calc_id: int):
    calc = CALCULATIONS.get(calc_id)
    if calc is None:
        raise Http404()
    context = {"calc": calc, "grades": CONCRETE_GRADES, "MINIO_PUBLIC_BASE_URL": MINIO_BASE}
    return render(request, "flexural/calculation_detail.html", context)
