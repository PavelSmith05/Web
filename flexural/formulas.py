"""Формулы расчётов для балки.

Содержит упрощённую формулу максимальной сосредоточенной нагрузки P_max (кН)
по данным габаритов балки и прочности бетона.

P_max(kN) = (2/3) * f_c * b * h^2 / (L * 1_000_000)

где:
  f_c  – расчётная прочность (МПа = Н/мм²)
  b    – ширина балки (мм)
  h    – высота балки (мм)
  L    – длина пролёта (м)

Это учебная демонстрационная формула.
"""
from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class BeamGeometry:
    length_mm: int
    width_mm: int
    height_mm: int


def compute_max_load_kN(strength_mpa: float, geom: BeamGeometry, strength_factor: float | None = None) -> float:
    """Возвращает максимальную (условную) нагрузку в кН. Все размеры в мм.

    Формула в мм:
      Исходно L в метрах. Заменяем L (м) на (L_mm / 1000).
      P = (2/3)*f*b*h^2 / ( (L_mm/1000) * 1_000_000 ) = (2/3)*f*b*h^2 / (L_mm * 1000)
    """
    if geom.length_mm <= 0 or geom.width_mm <= 0 or geom.height_mm <= 0:
        return 0.0
    f_eff = strength_mpa * (strength_factor if strength_factor else 1.0)
    return (2.0 / 3.0) * f_eff * geom.width_mm * (geom.height_mm ** 2) / (geom.length_mm * 1000)
