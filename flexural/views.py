from django.conf import settings
from django.http import Http404, HttpResponseNotAllowed
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import AnonymousUser
from django.contrib.auth.decorators import login_required
from django.db import connection

from .models import ConcreteGrade, FlexuralCalculation, FlexuralCalculationItem
from .order_dict import build_calculation_dict
from .formulas import BeamGeometry, compute_max_load_kN

MINIO_BASE = getattr(settings, "MINIO_PUBLIC_BASE_URL", "http://localhost:9000/beam-images/")

def _user_draft(request):
    user = request.user
    if isinstance(user, AnonymousUser) or not user.is_authenticated:
        return None
    return (
        FlexuralCalculation.objects
        .filter(creator=user, status=FlexuralCalculation.Status.DRAFT)
        .first()
    )

def grade_list(request):
    # Support new explicit search parameter name 'grade_search' while remaining backward compatible with legacy 'q'
    grade_search = request.GET.get("grade_search")
    if grade_search is None:  # fallback to old param
        grade_search = request.GET.get("q", "")
    grade_search = grade_search.strip()

    grades_qs = ConcreteGrade.objects.filter(status=ConcreteGrade.Status.ACTIVE)
    if grade_search:
        grades_qs = grades_qs.filter(name__icontains=grade_search) | grades_qs.filter(grade_code__icontains=grade_search)
    grades = list(grades_qs.order_by("id"))

    calc = _user_draft(request)
    cart_count = calc.items.count() if calc else 0

    calc_dict = build_calculation_dict(calc, MINIO_BASE) if calc else None
    context = {
        "grades": grades,
        "grade_search": grade_search,
        "calc": calc,
        "calc_dict": calc_dict,
        "cart_count": cart_count,
        "MINIO_PUBLIC_BASE_URL": MINIO_BASE,
    }
    return render(request, "flexural/grade_list.html", context)

def grade_detail(request, grade_id: int):
    grade = get_object_or_404(ConcreteGrade, pk=grade_id, status=ConcreteGrade.Status.ACTIVE)
    calc = _user_draft(request)
    calc_dict = build_calculation_dict(calc, MINIO_BASE) if calc else None
    context = {
        "grade": grade,
        "calc": calc,
        "calc_dict": calc_dict,
        "MINIO_PUBLIC_BASE_URL": MINIO_BASE,
    }
    return render(request, "flexural/grade_detail.html", context)

def calculation_detail(request, calc_id: int):
    calc = get_object_or_404(FlexuralCalculation, pk=calc_id)
    if calc.status == FlexuralCalculation.Status.DELETED:
        raise Http404()

    per_item_results: dict[int, float] = {}

    if request.method == "POST":
        # Из формы приходят размеры балки (мм для ширины/высоты, длина в метрах?)
        # Теперь все три габарита в мм. Длину храним в модели по-прежнему в метрах, поэтому конвертация.
        def _parse_int(name: str, fallback: int) -> int:
            try:
                return int(request.POST.get(name, fallback))
            except ValueError:
                return fallback
        def _parse_float(name: str, fallback: float) -> float:
            try:
                return float(request.POST.get(name, fallback))
            except ValueError:
                return fallback

        new_height = _parse_int("beam_height_mm", calc.beam_height_mm)
        new_width = _parse_int("beam_width_mm", calc.beam_width_mm)
        # длина в форме теперь beam_length_mm
        current_length_mm = int(float(calc.beam_length_m) * 1000)
        new_length_mm = _parse_int("beam_length_mm", current_length_mm)
        new_length_m = new_length_mm / 1000 if new_length_mm > 0 else float(calc.beam_length_m)

        update_fields = []
        if new_height != calc.beam_height_mm:
            calc.beam_height_mm = new_height
            update_fields.append("beam_height_mm")
        if new_width != calc.beam_width_mm:
            calc.beam_width_mm = new_width
            update_fields.append("beam_width_mm")
        if new_length_m != float(calc.beam_length_m):
            calc.beam_length_m = new_length_m
            update_fields.append("beam_length_m")
        if update_fields:
            calc.save(update_fields=update_fields)

        geom = BeamGeometry(length_mm=int(float(calc.beam_length_m) * 1000), width_mm=calc.beam_width_mm, height_mm=calc.beam_height_mm)
        # Рассчитываем для каждой позиции индивидуально (используем compressive_strength_mpa)
        for it in calc.items.select_related("grade"):
            per_item_results[it.id] = compute_max_load_kN(it.grade.compressive_strength_mpa, geom)

    calc_dict = build_calculation_dict(calc, MINIO_BASE)
    context = {
        "calc": calc,
        "calc_dict": calc_dict,
        "grades": list(ConcreteGrade.objects.filter(status=ConcreteGrade.Status.ACTIVE)),
        "MINIO_PUBLIC_BASE_URL": MINIO_BASE,
        "per_item_results": per_item_results,
        "beam_length_mm": int(float(calc.beam_length_m) * 1000),
    }
    return render(request, "flexural/calculation_detail.html", context)

@login_required
def add_to_calculation(request, grade_id: int):
    if request.method != "POST":
        return HttpResponseNotAllowed(["POST"])
    grade = get_object_or_404(ConcreteGrade, pk=grade_id, status=ConcreteGrade.Status.ACTIVE)
    calc = (
        FlexuralCalculation.objects
        .filter(creator=request.user, status=FlexuralCalculation.Status.DRAFT)
        .first()
    )
    if not calc:
        calc = FlexuralCalculation.objects.create(
            creator=request.user,
            status=FlexuralCalculation.Status.DRAFT,
            beam_length_m=1,
            beam_width_mm=100,
            beam_height_mm=100,
        )
    item = calc.items.filter(grade=grade).first()
    if not item:
        calc.items.create(grade=grade, quantity=1)
    else:
        # Нормализуем прежние данные если вдруг quantity > 1
        if item.quantity != 1:
            item.quantity = 1
            item.save(update_fields=["quantity"])
    # Redirect back to originating page (next) if safe and internal
    next_url = request.POST.get("next", "")
    if next_url and next_url.startswith("/") and "://" not in next_url:
        return redirect(next_url)
    return redirect("grade_list")

@login_required
def delete_calculation(request, calc_id: int):
    if request.method != "POST":
        return HttpResponseNotAllowed(["POST"])
    with connection.cursor() as cur:
        cur.execute(
            "UPDATE flexural_calculation SET status = %s, completed_at = completed_at WHERE id = %s AND creator_id = %s AND status <> %s",
            [FlexuralCalculation.Status.DELETED, calc_id, request.user.id, FlexuralCalculation.Status.DELETED]
        )
    # Redirect explicitly to home page after deletion per updated requirement
    return redirect("/")

@login_required
def delete_calculation_item(request, calc_id: int, item_id: int):
    if request.method != "POST":
        return HttpResponseNotAllowed(["POST"])
    calc = get_object_or_404(FlexuralCalculation, pk=calc_id, creator=request.user)
    if calc.status != FlexuralCalculation.Status.DRAFT:
        # silently ignore / or could return 405
        return redirect("calculation_detail", calc_id=calc.pk)
    item = get_object_or_404(FlexuralCalculationItem, pk=item_id, calculation=calc)
    item.delete()
    return redirect("calculation_detail", calc_id=calc.pk)
