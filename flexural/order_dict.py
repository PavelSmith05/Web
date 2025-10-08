from __future__ import annotations
from typing import Any, Dict, List

from .models import FlexuralCalculation


def build_calculation_dict(calc: FlexuralCalculation, minio_base: str) -> Dict[str, Any]:
    """
    Собирает «Словарь заявки»: поля самой заявки + все позиции м-м в одном dict.
    Никаких запросов вне этой функции не делать.
    """
    items = list(
        calc.items.select_related("grade").order_by("order_index", "id")
    )

    items_payload: List[Dict[str, Any]] = []
    for it in items:
        g = it.grade
        img_key = g.image_key or ""
        items_payload.append({
            "grade_id": g.id,
            "grade_code": g.grade_code,
            "grade_name": g.name,
            "description": g.description,
            "strength_factor": getattr(g, "strength_factor", None),
            "compressive_strength_mpa": g.compressive_strength_mpa,
            "image_key": img_key,
            "image_url": f"{minio_base}{img_key}" if img_key else None,
            # quantity убран как ненужный
            "order_index": it.order_index,
            "is_primary": it.is_primary,
            "comment": it.comment,
        })

    payload: Dict[str, Any] = {
        "id": calc.id,
        "status": calc.status,
        "created_at": calc.created_at.isoformat() if calc.created_at else None,
        "creator_id": calc.creator_id,
        "formed_at": calc.formed_at.isoformat() if calc.formed_at else None,
        "completed_at": calc.completed_at.isoformat() if calc.completed_at else None,
        "moderator_id": calc.moderator_id,
        "beam_length_m": float(calc.beam_length_m),
        "beam_length_mm": int(float(calc.beam_length_m) * 1000),
        "beam_width_mm": calc.beam_width_mm,
        "beam_height_mm": calc.beam_height_mm,
        "result_max_load_kN": float(calc.result_max_load_kN) if calc.result_max_load_kN is not None else None,
        "items": items_payload,
        "items_count": len(items_payload),
    }
    return payload
