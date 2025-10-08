from django import template

register = template.Library()

@register.filter
def comma(value):
    """Заменяет десятичную точку на запятую в строковом представлении.
    Если значение не приводится к строке нормально, возвращает исходное.
    """
    try:
        s = f"{float(value):.2f}"
    except (TypeError, ValueError):
        return value
    return s.replace('.', ',')

@register.filter(name="dict_get")
def dict_get(d, key):
    """Возвращает d[key] если возможно, иначе None.
    Поддерживает использование в шаблонах: {{ mydict|dict_get:obj.id }}"""
    try:
        return d.get(key)
    except Exception:
        return None
